from typing import Set, Dict

import dash_core_components as dcc
import dash_html_components as html

from constants.column_keys import CHART, SCENARIO, DATE_GENERATED
from constants.html_ids import CHART_SELECTOR, SCENARIO_SELECTOR, DATE_SELECTOR, ERRORBAR_TOGGLER


def control_panel(control_options: Dict) -> html.Div:
    """
    Creates the control panel portion of the dashboard.
    :param control_options: A map from selector to possible selector values. Cannot be None, and
    must contain values under CHART, SCENARIO, and DATA_GENERATED.
    :return: The control panel. Never None.
    """
    return html.Div(id='control_panel_div', className='row',
                    children=[html.Div(className='column',
                                       children=[chart_selector(control_options[CHART]),
                                                 small_controls(control_options[SCENARIO],
                                                                control_options[DATE_GENERATED])])])


def small_controls(scenario_options: Set, date_options: Set) -> html.Div:
    """
    Creates the smaller controls that should not span full width.
    :param scenario_options: The scenarios that can be displayed. Cannot be None, should not be
    empty.
    :param date_options: The dates that can be displayed. Cannot be None, should not be
    empty.
    :return: The div containing small controls. Never None.
    """
    return html.Div(id='small_controls_div', className='row',
                    children=[scenario_selector(scenario_options),
                              date_selector(date_options),
                              errorbar_toggler()])


def chart_selector(chart_options: Set) -> html.Div:
    """
    Creates a selector for the chart to be displayed.
    :param chart_options: The charts that can be displayed. Cannot be None, should not be empty.
    :return: The chart selector. Never None.
    """
    return html.Div(id='chart_selector_div', children=[
        html.H4(children='Add or remove charts:'),
        dcc.Dropdown(id=CHART_SELECTOR,
                     options=[{'label': name, 'value': name} for name in chart_options],
                     multi=True)])


def scenario_selector(scenario_options: Set) -> html.Div:
    """
    Creates a selector for the scenario to be displayed.
    :param scenario_options: The scenarios that can be displayed. Cannot be None, should not be
    empty.
    :return: The scenario selector. Never None.
    """
    return html.Div(id='scenario_selector_div', children=[
        html.H4(children='Add or remove scenarios:'),
        dcc.Dropdown(id=SCENARIO_SELECTOR,
                     options=[{'label': name, 'value': name} for name in scenario_options],
                     multi=True,
                     clearable=False,
                     value=[next(iter(scenario_options))])],
                    className='four columns')


def date_selector(date_options: Set) -> html.Div:
    """
    Creates a selector for the date to be displayed.
    :param date_options: The dates that can be displayed. Cannot be None, should not be
    empty.
    :return: The date selector. Never None.
    """
    return html.Div(id='date_selector_div', children=[
        html.H4(children='Pick date:'),
        dcc.Dropdown(id=DATE_SELECTOR,
                     options=[{'label': name, 'value': name} for name in date_options],
                     clearable=False,
                     value=next(iter(date_options)))],
                    className='four columns')


def errorbar_toggler() -> html.Div:
    """
    Creates a checklist that is used as a toggle for errorbars.
    :return: The errorbar toggler. Never None.
    """
    return html.Div(id='errorbar_toggler_div', children=[
        html.H4(children='Enable error bars:'),
        dcc.Checklist(
            id=ERRORBAR_TOGGLER,
            options=[
                {'label': '', 'value': "True"},
            ],
            value=["True"],
            labelStyle={'display': 'inline-block'}
        )],
                    className='four columns',
                    style={'textAlign': 'center'})
