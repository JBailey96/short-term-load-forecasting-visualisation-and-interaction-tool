from app import app
from data.data import load_data
from dash.dependencies import Input, Output, State
from component.model.metric import model_metrics_table
import json

# Updates the model metrics table with the data required to compare the actual visualised load forecast
# with the model(s) load forecasts using the load visualisition data points as input. The test data
# input component values and list of models are also inputs to calculate model performance over test data.
@app.callback(
    Output('visualised-metrics-table', 'children'),
    [Input('load-graph', 'children'),
    Input('models', 'children'),
    Input('test-data-date-picker-day-range', 'start_date'),
    Input('test-data-date-picker-day-range', 'end_date'),
    Input('error-distribution-graph', 'children')])
def update_metrics_table(load_data_graph, models, test_data_start_date, test_data_end_date, error_distribution_graph):
    return model_metrics_table.update_values(load_data_graph, json.loads(models), load_data, test_data_start_date, test_data_end_date, error_distribution_graph)

# returns a style to unhide the model metrics table if there are models, hidden otherwise.
@app.callback(
    Output('metrics-table-container', 'style'),
    [Input('models', 'children')]
)
def update_metrics_table_container_style(models):
    return model_metrics_table.update_metrics_container_style(json.loads(models))