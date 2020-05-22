from typing import Dict, List

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Output, Input

from components.charts import get_figure, chart_panel
from components.controls import control_panel
from components.header import header_panel
from constants.html_ids import CHART_SELECTOR, SCENARIO_SELECTOR, DATE_SELECTOR, CHART_OUTPUT, \
    ERRORBAR_TOGGLER
from data import dataloader

dash_app = dash.Dash(__name__)
# This must be named application to work within elastic beanstalk without
# extra configuration
application = dash_app.server

# df is the dataframe containing all of the data predicted and real
# control_options is a dictionary of control to possible values
df, control_options = dataloader.get_data()  # type: pd.DataFrame, Dict

# The top level layout of the application.
# Since we are using regular container, row, column css
# this should stay a container, while children should be rows
# at the top most level and contain at least one column.
dash_app.layout = html.Div(
    className='container', children=[
        header_panel(),
        control_panel(control_options),
        chart_panel()
    ]
)


@dash_app.callback(Output(CHART_OUTPUT, 'children'),
                   [Input(CHART_SELECTOR, 'value'),
                    Input(SCENARIO_SELECTOR, 'value'),
                    Input(DATE_SELECTOR, 'value'),
                    Input(ERRORBAR_TOGGLER, 'value')])
def display_graphs(selected_charts: List[str],
                   selected_scenarios: List[str],
                   selected_date: str,
                   show_errorbars: List[str]) -> List[dcc.Graph]:
    """
    Dash callback function. This will be called anytime one of the inputs are changed, and update
    the output.
    :param selected_charts: The charts currently selected for display. Can be None. If specified
    must exist within df.
    :param selected_scenarios: The selected scenarios to display on each chart. Can be None. If
    specified must exist within df.
    :param selected_date: The date the predicted data was generated. Cannot be None, must exist
    within df.
    :param show_errorbars: Whether or not to display error bars on the charts. Cannot be None, can
    be empty.
    :return: A list of graphs for each selected chart. Can be empty, never None.
    """
    graphs = []
    if selected_charts is not None:
        for selected_chart in selected_charts:
            graphs.append(dcc.Graph(
                figure=get_figure(df,
                                  selected_chart,
                                  selected_scenarios,
                                  selected_date,
                                  show_errorbars)))
    return graphs


if __name__ == '__main__':
    dash_app.run_server(debug=True)
