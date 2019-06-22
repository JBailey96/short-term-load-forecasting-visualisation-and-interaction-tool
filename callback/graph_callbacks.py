from app import app
from data.data import load_data
from dash.dependencies import Input, Output, State
from component.graph.visualise_model import load_graph, characteristics_graph
from component.graph.error_model import error_distribution_graph
import json

#updates the load graph visualisation with the user interactible elements as input and the model state
@app.callback(
    Output('load-graph', 'children'),
    [Input('date-picker-day-range', 'start_date'),
     Input('date-picker-day-range', 'end_date'),
     Input('models', 'children'),
     Input('characteristics-selection', 'value'),
     Input('date-highlight-value-selection', 'value'),
     Input('date-highlight-variable-selection', 'value')])
def update_load_graph(start_date, end_date, models, characteristics_y_axis_selection, highlight_value, highlight_variable):
    return load_graph.update(load_data, start_date, end_date, json.loads(models), characteristics_y_axis_selection, highlight_variable, highlight_value)

#updates the characteristics graph visualisation with the user interactible elements as input and the model state
@app.callback(
    Output('characteristics-graph', 'children'),
    [Input('date-picker-day-range', 'start_date'),
     Input('date-picker-day-range', 'end_date'),
     Input('models', 'children'),
     Input('characteristics-selection', 'value'),
     Input('date-highlight-value-selection', 'value'),
     Input('date-highlight-variable-selection', 'value')])
def update_characteristics_graph(start_date, end_date, models, characteristics_y_axis_selection, highlight_value, highlight_variable):
    return characteristics_graph.update(load_data, start_date, end_date, json.loads(models), characteristics_y_axis_selection, highlight_variable, highlight_value)

#updates the load graph visualisation with the user interactible elements as input, 
# model state and data from the load graph visualisation
@app.callback(
    Output('error-distribution-graph', 'children'),
    [Input('load-graph', 'children'),
     Input('models', 'children'),
     Input('test-data-date-picker-day-range', 'start_date'),
     Input('test-data-date-picker-day-range', 'end_date'),
     Input('date-highlight-value-selection', 'value'),
     Input('date-highlight-variable-selection', 'value')])
def update_error_distribution_graph(load_graph, models, test_data_start_date, test_data_end_date, highlight_value, highlight_variable):
    return error_distribution_graph.update(load_data, load_graph, json.loads(models), test_data_start_date, test_data_end_date, highlight_variable, highlight_value)
