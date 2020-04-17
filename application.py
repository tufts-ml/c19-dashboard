# -*- coding: utf-8 -*-
from typing import List, Dict, Set

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State

import plot
from components.charts import chart_panel
from components.controls import control_panel
from components.header import header_panel
from utils import range_can_be_altered, get_dash_time_format_from_unix_timestamp

dash_app = dash.Dash(__name__)
application = dash_app.server

plot_dicts, dfs = plot.main()  # type: List[Dict[str, Dict]], List[pd.DataFrame]
current_scenario: int = 0
plot_options: Set[str] = set(plot_dicts[0].keys())
currently_displayed_plots: Dict[str, Dict] = {}

dash_app.layout = html.Div(
    className='container', children=[
        header_panel(),
        control_panel(plot_options, len(plot_dicts), dfs[0]),
        chart_panel()
    ]
)


@dash_app.callback(Output('output', 'children'),
                   [Input('chart_selector', 'value'),
                    Input('scenario_selector', 'value'),
                    Input('time-range-slider', 'value')],
                   [State('output', 'children')])
def display_graphs(selected_chart_keys: List[str],
                   selected_scenario: int,
                   unix_time_range: List[int],
                   children: List[Dict]) -> List:

    alter_time_ranges(children, unix_time_range)
    if selected_chart_keys is not None:
        remove_deselected_graphs(selected_chart_keys)
        add_selected_graphs(selected_chart_keys, selected_scenario)

    return list(currently_displayed_plots.values())


def alter_time_ranges(plots: List[Dict], unix_time_range: List[int]) -> None:
    if plots:
        for plot in plots:
            if range_can_be_altered(plot):
                time_strings = list(map(get_dash_time_format_from_unix_timestamp, unix_time_range))
                plot['props']['figure']['layout']['xaxis']['range'] = time_strings
                plot['props']['figure']['layout']['xaxis']['autorange'] = False
                currently_displayed_plots[plot['props']['id']] = plot


def remove_deselected_graphs(selected_chart_keys: List[str]) -> None:
    keys_to_remove = []
    for key in currently_displayed_plots.keys():
        if key not in selected_chart_keys:
            keys_to_remove.append(key)
    for key in keys_to_remove:
        del currently_displayed_plots[key]


def add_selected_graphs(selected_chart_keys: List[str], selected_scenario: int,) -> None:
    plot_dict = plot_dicts[selected_scenario]
    for value in selected_chart_keys:
        if value not in currently_displayed_plots:
            currently_displayed_plots[value] = dcc.Graph(id=value, figure=plot_dict[value])


if __name__ == '__main__':
    dash_app.run_server(debug=True)
