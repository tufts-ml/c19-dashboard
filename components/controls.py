from typing import Set, Union, Dict
import pandas as pd

import dash_core_components as dcc
import dash_html_components as html


def control_panel(plot_options: Set, num_scenarios: int, df) -> html.Div:
    return html.Div(id='control_panel', className='row',
                    children=[html.Div(className='column',
                                       children=[chart_selector(plot_options),
                                                 scenario_selector(num_scenarios),
                                                 time_range_selector(df)])])


def chart_selector(plot_options: Set) -> html.Div:
    return html.Div(id='chart_selector_div', children=[
        html.H4(children='Add or remove charts:'),
        dcc.Dropdown(id='chart_selector',
                     options=[{'label': name, 'value': name} for name in plot_options],
                     multi=True)
    ])


def scenario_selector(num_scenarios: int) -> html.Div:
    options = [{'label': 'Scenario {}'.format(i), 'value': i} for i in range(num_scenarios)]

    return selector_div("Select a scenario", dcc.RadioItems(
            id='scenario_selector',
            className='u-pull-right',
            options=options,
            value=0,
            labelStyle={'display': 'inline-block'}
    ))


def time_range_selector(df: pd.DataFrame) -> html.Div:
    dates_in_unix_seconds = (df['timestep_formatted'] -
                             pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
    step_size_in_unix_seconds = dates_in_unix_seconds.iloc[1] - dates_in_unix_seconds.iloc[0]
    min_date_in_unix_seconds = dates_in_unix_seconds.min()
    max_date_in_unix_seconds = dates_in_unix_seconds.max()
    time_range_marks = generate_time_range_marks(min_date_in_unix_seconds,
                                                 max_date_in_unix_seconds,
                                                 step_size_in_unix_seconds)

    return selector_div('Time Range', dcc.RangeSlider(
                id='time-range-slider',
                min=min_date_in_unix_seconds,
                max=max_date_in_unix_seconds,
                value=[min_date_in_unix_seconds, max_date_in_unix_seconds],
                marks=time_range_marks,
                included=False))


def selector_div(label: str, selector: Union[dcc.Dropdown, dcc.Slider]) -> html.Div:
    return html.Div(className='row', children=[
        html.Div(className="one-third column", children=[html.Label(label)]),
        html.Div(className="two-thirds column", children=[selector])
    ])


def generate_time_range_marks(min_date_in_unix_seconds: int,
                              max_date_in_unix_seconds: int,
                              step_size_in_unix_seconds: int) -> Dict[int, str]:
    # We always have at least one mark, so set this to the number of marks you want
    # minus one
    num_marks = 4

    num_steps = (max_date_in_unix_seconds - min_date_in_unix_seconds) // step_size_in_unix_seconds
    steps_per_mark = num_steps // num_marks
    time_range_marks = {}
    for i in range(min_date_in_unix_seconds,
                   max_date_in_unix_seconds+1,
                   steps_per_mark * step_size_in_unix_seconds):
        time_range_marks[i] = pd.Timestamp(i, unit='s').strftime('%m-%d')
    return time_range_marks
