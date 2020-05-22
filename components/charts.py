from typing import List, Tuple, Dict

import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from matplotlib import cm

from constants.column_keys import IS_PREDICTION, SCENARIO, DATE_GENERATED, TIMESTEP_FORMATTED, \
    PERCENTILE
from constants.display_config import TIME_STEP_FORMAT
from constants.html_ids import CHART_OUTPUT

tab10 = cm.get_cmap('tab10')


def chart_panel() -> html.Div:
    """
    Creates the chart panel of dashboard.
    :return: The chart panel. Never None.
    """
    return html.Div(className='row', children=[html.Div(id=CHART_OUTPUT, className='column')])


def split_dataframe_into_predicted_and_real(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Splits the dataframe into predicted and real dataframes.
    :param df: The dataframe to split. Cannot be None.
    :return: The split dataframe. Never None.
    """
    predicted_df = df[df[IS_PREDICTION] == True]
    real_df = df[df[IS_PREDICTION] == False]
    return predicted_df, real_df


def split_dataframe_into_selected_scenarios(df: pd.DataFrame,
                                            selected_scenarios: List[str]) -> List[pd.DataFrame]:
    """
    Splits the dataframe into a dataframe per selected scenario.
    :param df: The dataframe to split. Cannot be None.
    :param selected_scenarios: The selected scenarios. Cannot be None.
    :return: The list of dataframes. Never None.
    """
    dfs = []
    for scenario in selected_scenarios:
        dfs.append(df[df[SCENARIO] == scenario])
    return dfs


def prepare_data(df: pd.DataFrame,
                 selected_date: str,
                 selected_scenarios: List[str],
                 show_errorbars: List[str]) -> Tuple[List[pd.DataFrame],
                                                     pd.DataFrame,
                                                     List[float],
                                                     bool]:
    """
    Prepare the data by performing necessary filtering, and organization.
    :param df: The data to be filtered. Cannot be None.
    :param selected_date: The date to filter the df by. Cannot be None.
    :param selected_scenarios: The scenarios used to filter and then split the dataframe.
    :param show_errorbars: Whether or not to display error bars on the charts. Cannot be None, can
    be empty.
    :return: The filtered, and split by scenario, prediction dfs, the real df, and the percentiles.
    """
    predicted_df, real_df = split_dataframe_into_predicted_and_real(df)
    predicted_df = predicted_df[predicted_df[DATE_GENERATED] == selected_date]

    percentiles = sorted(predicted_df[PERCENTILE].unique())

    selected_scenario_predicted_dfs = split_dataframe_into_selected_scenarios(predicted_df,
                                                                              selected_scenarios)
    show_errorbars = True if len(show_errorbars) > 0 and show_errorbars[0] == 'True' else False

    return selected_scenario_predicted_dfs, real_df, percentiles, show_errorbars


def get_figure(all_data_df: pd.DataFrame,
               y_column_name: str,
               selected_scenarios: List[str],
               selected_date: str,
               show_errorbars: List[str]) -> Dict[str, Dict]:
    """
    Get the figure that matches the column name, selected scenarios, and selected date.
    :param all_data_df: All of the unfiltered data. Cannot be None.
    :param y_column_name: The column of the dataframe that should make the y axis. Cannot be None.
    :param selected_scenarios: The list of selected scenarios. Cannot be None, can be Empty.
    :param selected_date: The generated date selected, cannot be None.
    :param show_errorbars: Whether or not to display error bars on the charts. Cannot be None, can
    be empty.
    :return: The figure.
    """
    selected_scenario_predicted_dfs, real_df, percentiles, show_errorbars = prepare_data(
        all_data_df, selected_date, selected_scenarios, show_errorbars)

    return create_figure(selected_scenario_predicted_dfs,
                         real_df,
                         percentiles,
                         y_column_name,
                         show_errorbars)


def create_figure(selected_scenario_predicted_dfs: List[pd.DataFrame],
                  real_df: pd.DataFrame,
                  percentiles: List[float],
                  y_column_name: str,
                  show_errorbars: bool) -> Dict[str, Dict]:
    """
    Creates the actual figures.
    :param selected_scenario_predicted_dfs: Separate prediction dfs for each scenario. Cannot be
    None.
    :param real_df: A df containing the real data. Never None.
    :param percentiles: The confidence percentiles to plot. Never None.
    :param y_column_name: The column of the dataframe that should make the y axis. Cannot be None.
    :param show_errorbars: Whether or not to display error bars. Cannot be None.
    :return: The figure. Never None, can have no data.
    """
    fig = go.Figure()

    if y_column_name in real_df.columns:
        fig.add_trace(go.Scatter(
            x=real_df[TIMESTEP_FORMATTED],
            y=real_df[y_column_name],
            name=str('actual_data'),
            mode='lines',
            line=dict(color='black')
        ))

    for idx, predicted_df in enumerate(selected_scenario_predicted_dfs):
        raw_color = tab10.colors[idx % 10]
        color = convert_color(raw_color)
        fill_color = convert_color(raw_color, .2)
        for percentile in percentiles:
            if not show_errorbars and not np.isclose(percentile, 50.0):
                continue

            percentile_predicted_df = predicted_df[predicted_df[PERCENTILE] == percentile]

            fill = 'tonexty'
            width = 0
            if np.isclose(percentile, 2.5) or not show_errorbars:
                fill = 'none'
            if np.isclose(percentile, 50.0):
                width = 2

            fig.add_trace(go.Scatter(
                x=percentile_predicted_df[TIMESTEP_FORMATTED],
                y=percentile_predicted_df[y_column_name],
                fill=fill,
                fillcolor=fill_color,
                mode='lines',
                line=dict(color=color, width=width),
                name='%ile: '.format(str(float(percentile)))))

            fig.update_layout(
                title=y_column_name,
                xaxis_tickformat=TIME_STEP_FORMAT,
                xaxis_tickangle=-45,
                yaxis_title='Patient Count',
                font=dict(
                    size=12,
                    color='#464646'
                ),
                hovermode='x unified',
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_linecolor='#464646',
                yaxis_linecolor='#464646',
                xaxis=dict(
                    rangeslider=dict(
                        visible=True
                    ),
                    type='date'
                )
            )

    return fig


def convert_color(color_tup: Tuple[float, float, float], opacity: float = 1.0):
    """
    Converts a tuple of color floats to an rgba string.
    :param color_tup: A tuple containing the rba float values. Cannot be None or empty.
    :param opacity: The opacity, default of 1. Cannot be None or negative.
    :return: The rgba string. Never None.
    """
    return 'rgba({}, {}, {}, {})'.format(color_tup[0], color_tup[1], color_tup[2], opacity)
