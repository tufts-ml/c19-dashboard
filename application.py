# -*- coding: utf-8 -*-
from typing import List

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plot
from components.charts import chart_panel
from components.controls import control_panel
from components.header import header_panel

dash_app = dash.Dash(__name__)
dash_app.config.suppress_callback_exceptions = True
application = dash_app.server

plot_dicts = plot.main()
plot_options = plot_dicts[0].keys()

dash_app.layout = html.Div(
    className='container', children=[
        header_panel(),
        control_panel(plot_options, len(plot_dicts)),
        chart_panel(),   
    ]
)


@dash_app.callback(Output('output', 'children'), [Input('chart_selector', 'value'),
                                                  Input('scenario_selector', 'value')])
def display_graphs(selected_charts: List, selected_scenario: int) -> List:
    plot_dict = plot_dicts[selected_scenario]
    graphs = []
    if selected_charts is not None:
        for value in selected_charts:
            curr_plt = plot_dict[value]

            graphs.append(dcc.Graph(id=value+'-fig')) #figure=plot_dict[value]))
            graphs.append(dcc.RangeSlider(
                                id=value+'-slider',
                                min=0,
                                max=len(curr_plt['mid_plt_x']),
                                step=None,
                                marks={
                                    0: '0 days',
                                    7: '1 week',
                                    14: '2 weeks',
                                    40: '40 days'
                                },
                                value=[0, 7]
                            )
                        )
        return graphs

@dash_app.callback(Output('Patients Presenting at Hospital-fig', 'figure'), 
                    [Input('Patients Presenting at Hospital-slider', 'value'),
                     Input('scenario_selector', 'value')])
def update_patients_presenting(selected_range, selected_scenario):
    p_df = plot_dicts[selected_scenario]['Patients Presenting at Hospital']
    return update_graph(p_df, selected_range)

@dash_app.callback(Output('Patients in General Ward-fig', 'figure'), 
                    [Input('Patients in General Ward-slider', 'value'),
                     Input('scenario_selector', 'value')])
def update_patients_gen(selected_range, selected_scenario):
    p_df = plot_dicts[selected_scenario]['Patients in General Ward']
    return update_graph(p_df, selected_range)

@dash_app.callback(Output('Patients in ICU (but not on Ventilator)-fig', 'figure'), 
                    [Input('Patients in ICU (but not on Ventilator)-slider', 'value'),
                     Input('scenario_selector', 'value')])
def update_patients_no_vent_icu(selected_range, selected_scenario):
    p_df = plot_dicts[selected_scenario]['Patients in ICU (but not on Ventilator)']
    return update_graph(p_df, selected_range)

@dash_app.callback(Output('Patients on Ventilator in ICU-fig', 'figure'), 
                    [Input('Patients on Ventilator in ICU-slider', 'value'),
                     Input('scenario_selector', 'value')])
def update_patients_vent_icu(selected_range, selected_scenario):
    p_df = plot_dicts[selected_scenario]['Patients on Ventilator in ICU']
    return update_graph(p_df, selected_range)

@dash_app.callback(Output('Patients that Die Each Day-fig', 'figure'), 
                    [Input('Patients that Die Each Day-slider', 'value'),
                     Input('scenario_selector', 'value')])
def update_patients_die(selected_range, selected_scenario):
    p_df = plot_dicts[selected_scenario]['Patients that Die Each Day']
    return update_graph(p_df, selected_range)

@dash_app.callback(Output('Patients Added to General Ward each day-fig', 'figure'), 
                    [Input('Patients Added to General Ward each day-slider', 'value'),
                     Input('scenario_selector', 'value')])
def update_patients_added_gen(selected_range, selected_scenario):
    p_df = plot_dicts[selected_scenario]['Patients Added to General Ward each day']
    return update_graph(p_df, selected_range)

@dash_app.callback(Output('Patients Added to ICU (but not on vent) each day-fig', 'figure'), 
                    [Input('Patients Added to ICU (but not on vent) each day-slider', 'value'),
                     Input('scenario_selector', 'value')])
def update_patients_added_no_vent_icu(selected_range, selected_scenario):
    p_df = plot_dicts[selected_scenario]['Patients Added to ICU (but not on vent) each day']
    return update_graph(p_df, selected_range)

@dash_app.callback(Output('Patients Added on Ventilator in ICU each day-fig', 'figure'), 
                    [Input('Patients Added on Ventilator in ICU each day-slider', 'value'),
                     Input('scenario_selector', 'value')])
def update_patients_added_vent_icu(selected_range, selected_scenario):
    p_df = plot_dicts[selected_scenario]['Patients Added on Ventilator in ICU each day']
    return update_graph(p_df, selected_range)
 
@dash_app.callback(Output('Patients Discharged from General Ward each day-fig', 'figure'), 
                    [Input('Patients Discharged from General Ward each day-slider', 'value'),
                     Input('scenario_selector', 'value')])
def update_patients_discharged_gen(selected_range, selected_scenario):
    p_df = plot_dicts[selected_scenario]['Patients Discharged from General Ward each day']
    return update_graph(p_df, selected_range)
 
@dash_app.callback(Output('Patients Discharged from ICU (but not on vent) each day-fig', 'figure'), 
                    [Input('Patients Discharged from ICU (but not on vent) each day-slider', 'value'),
                     Input('scenario_selector', 'value')])
def update_patients_discharged_no_vent_icu(selected_range, selected_scenario):
    p_df = plot_dicts[selected_scenario]['Patients Discharged from ICU (but not on vent) each day']
    return update_graph(p_df, selected_range)

@dash_app.callback(Output('Patients Discharged from On Ventilator In ICU each day-fig', 'figure'), 
                    [Input('Patients Discharged from On Ventilator In ICU each dayl-slider', 'value'),
                     Input('scenario_selector', 'value')])
def update_patients_discharged_vent_icu(selected_range, selected_scenario):
    p_df = plot_dicts[selected_scenario]['Patients Discharged from On Ventilator In ICU each day']
    return update_graph(p_df, selected_range)

@dash_app.callback(Output('Patients discharged from Presenting each day (fully recovered)-fig', 'figure'), 
                    [Input('Patients discharged from Presenting each day (fully recovered)-slider', 'value'),
                     Input('scenario_selector', 'value')])
def update_patients_discharged_presenting(selected_range, selected_scenario):
    p_df = plot_dicts[selected_scenario]['Patients discharged from Presenting each day (fully recovered)']
    return update_graph(p_df, selected_range)

@dash_app.callback(Output('Patients added to Presenting each day-fig', 'figure'), 
                    [Input('Patients added to Presenting each day-slider', 'value'),
                     Input('scenario_selector', 'value')])
def update_patients_added_presenting(selected_range, selected_scenario):
    p_df = plot_dicts[selected_scenario]['Patients added to Presenting each day']
    return update_graph(p_df, selected_range)

 
def update_graph(plot_df, sel_range): 
    lower_x_filtered = plot_df['lower_plt_x'].iloc[sel_range[0]:sel_range[1]]
    lower_y_filtered = plot_df['lower_plt_y'].iloc[sel_range[0]:sel_range[1]]
    upper_x_filtered = plot_df['upper_plt_x'].iloc[sel_range[0]:sel_range[1]]
    upper_y_filtered = plot_df['upper_plt_y'].iloc[sel_range[0]:sel_range[1]]
    mid_x_filtered = plot_df['mid_plt_x'].iloc[sel_range[0]:sel_range[1]]
    mid_y_filtered = plot_df['mid_plt_y'].iloc[sel_range[0]:sel_range[1]]
    
    traces = []
    traces.append(dict(
            x=lower_x_filtered,
            y=lower_y_filtered,
            fill=plot_df['lower_plt_fill'],
            mode=plot_df['lower_plt_mode'],
            line =plot_df['lower_plt_line'],
            name=plot_df['lower_plt_name']
        ))
    traces.append(dict(
            x=upper_x_filtered,
            y=upper_y_filtered,
            fill=plot_df['upper_plt_fill'],
            fillcolor=plot_df['upper_plt_fillcolor'],
            mode=plot_df['upper_plt_mode'],
            line =plot_df['upper_plt_line'],
            name=plot_df['upper_plt_name']
        ))
    traces.append(dict(
            x=mid_x_filtered,
            y=mid_y_filtered,
            fill=plot_df['mid_plt_fill'],
            fillcolor=plot_df['mid_plt_fillcolor'],
            line =plot_df['mid_plt_line'],
            name=plot_df['mid_plt_name']
        ))
                        
    return {
        'data': traces,
        'layout': dict(
            title=plot_df['plt_title'],
            xaxis_tickformat=plot_df['plt_xaxis_tickformat'],
            xaxis_tickangle=plot_df['plt_xaxis_tickangle'],
            yaxis_title=plot_df['plt_yaxis_title'],
            font=plot_df['plt_font'],
            hovermode=plot_df['plt_hovermode'],
            showlegend=plot_df['plt_showlegend'],
            plot_bgcolor=plot_df['plt_plot_bgcolor'],
            xaxis_linecolor=plot_df['plt_xaxis_linecolor'],
            yaxis_linecolor=plot_df['plt_yaxis_linecolor'],
        )
    }


if __name__ == '__main__':
    dash_app.run_server(debug=False)
