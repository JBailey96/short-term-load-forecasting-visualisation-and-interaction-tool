import dash_html_components as html
from component.model.metric.util import model_metrics
from component.model.displacement import displacement_model
from component.model.regression import regression_model
import pandas as pd
from component.graph.error_model.util.error_model_graph_util import create_model_error_data

#generates the html table component containing the visualised and test data metric values for each forecasting model
def generate_table_html(models, visualised_data_metrics, test_data_metrics):
    return [html.Table(generate_table_rows(models, visualised_data_metrics, test_data_metrics),
                       style={'border': '1px solid black', 'border-collapse': 'collapse'})]

#generates the rows of the metrics table
def generate_table_rows(models, visualised_data_metrics, test_data_metrics):
    rows = []

    #if there is test data metrics: set flag to true, false otherwise.
    if test_data_metrics:
        is_test_metrics = True
    else: 
        is_test_metrics = False

    #generates the labelling row for 'Metrics' and each model names
    rows.append(html.Tr(generate_labelling_header_row(models, is_test_metrics)))

    #generates the columns for visualised and test data for each model
    rows.append(generate_visualised_test_headers(models, is_test_metrics))

    #append the metric values for each model
    for key in visualised_data_metrics[0]:
        rows.append(html.Tr(generate_metrics_rows(
            key, visualised_data_metrics, test_data_metrics, is_test_metrics)))
    return rows

#generates a header row for split visualised and test data columns for each model
def generate_visualised_test_headers(models, test_metrics):
    rows = []
    rows.append(html.Th()) #blank row below 'Metrics'
    for _ in range(0, len(models)): #iterate over every model
        rows.append(html.Td('Visualised', style={'border': '1px solid black'}))
        if (test_metrics): #if there is test data selected then add header label for test data values
            rows.append(html.Td('Test Data', style={
                        'border': '1px solid black'}))
    return html.Tr(rows)

#generates rows of metric values for each model
def generate_metrics_rows(key, metrics, test_data_metrics, is_test_metrics):
    row = [
        html.Th(key, style={'border': '1px solid black', 'textAlign': 'left'})]

    for metrics_index in range(0, len(metrics)): #iterate through all the metrics
        metric = metrics[metrics_index]
        row.append(html.Td(metric[key], style={'border': '1px solid black'}))
        if (is_test_metrics):
            test_data_metric = test_data_metrics[metrics_index]
            row.append(html.Td(test_data_metric[key], style={
                       'border': '1px solid black'}))
    return row

#generates header row for labelling 'Metrics' and each model
def generate_labelling_header_row(models, is_test_metrics):
    row = [html.Th('Metrics',  style={
                   'border': '1px solid black', 'textAlign': 'left'})] #Metrics column label

    #if there is test data selected to calculate metrics for then there is 2 subcolumns for visualised and test data
    if (is_test_metrics): 
        num_cols = '2'
    else:
        num_cols = '1'

    for model in models: #iterate through each model
        row.append(html.Th(model['model_name'], colSpan=num_cols, style={
                   'border': '1px solid black'}))
    return row

#updates the metric values in the table
def update_values(load_graph, models, load_data, test_data_start_date, test_data_end_date, error_distribution_graph):
    #checks that there are added models - this could be changed to check if the models are visualised rather than added
    if (len(models)):
        models_plotted = True
    else:
        models_plotted = False

    #if there are added models, then generate the graph
    if models_plotted:
        #generate visualised metrics
        visualised_data_metrics = get_visualised_metrics(
            load_graph, error_distribution_graph, test_data_start_date, test_data_end_date)
        #generate test data metrics
        test_data_metrics = get_test_data_metrics(
            load_data, models, test_data_start_date, test_data_end_date)
        #generate table
        return generate_table_html(models, visualised_data_metrics, test_data_metrics)

# generate metrics for the test data selected
def get_test_data_metrics(load_data, models, test_data_start_date, test_data_end_date):
    test_data_metrics = []

    if (test_data_start_date == None or test_data_end_date == None): #if there is no test data selected, return no metrics
        return test_data_metrics
    test_data = load_data[(load_data.Date >= test_data_start_date)
                          & (load_data.Date <= test_data_end_date)]
    y_true = test_data['Load']
    for model in models: #iterate through all load forecasting models
        model_type = model['model_type']
        #predict logic for each type of load forecasting model
        if (model_type == 'displacement'):
            predicted_load_data = displacement_model.predict(
                load_data, test_data_start_date, test_data_end_date, model)
            y_pred = predicted_load_data['Load']
        elif (model_type == 'regression'):
            y_pred = regression_model.predict(
                load_data, test_data_start_date, test_data_end_date, model)

        model_error_df = pd.DataFrame() #model structure containing the error data used to calculate error distribution metrics
        model_error_df = create_model_error_data(
            model_error_df, y_true, y_pred)
        test_data_metrics.append(model_metrics.calculate_metrics(
            y_true, y_pred, model_error_df['APE'], model_error_df['Percentage']))
    return test_data_metrics

# generate metrics for the visualised data
def get_visualised_metrics(load_graph, error_distribution_graph, test_data_start_date, test_data_end_date):
    # get the visualised graph data
    load_graph_figure = load_graph[0]['props']['figure']
    # get the error distribution graph data
    error_graph_figure = error_distribution_graph[0]['props']['figure']
    actual_load_y = load_graph_figure['data'][0]['y']

    metrics = []

    #sets flag true if there is a highlighted data in the load visualisation graph, false otherwise
    if (load_graph_figure['data'][1]['name'] == 'Highlighted Load'):
        is_highlighted_load_graph = True
    else:
        is_highlighted_load_graph = False

    #sets start index of the models to be 2 if there ii highlighted data in the load visualisation graph and have to
    #decrement 2 from the error distribution graph as there is highlighted data and no actual load data
    if (is_highlighted_load_graph):
        start_index_load_graph = 2
        decrement_error = 2
    else:
        start_index_load_graph = 1
        decrement_error = 1

    #sets flag true if there is test data selected, false otherwise
    if (test_data_start_date == None or test_data_end_date == None):
        is_test_data = False
    else:
        is_test_data = True

    step = 0 # step for incrementing the graph figure
    #iterate through all the model forecasts in the load visualisation graph
    for i in range(start_index_load_graph, len(load_graph_figure['data'])):
        plotted_model = load_graph_figure['data'][i] #load visualisation forecast
        plotted_model_error = error_graph_figure['data'][i+step-decrement_error] #error visualisation error values for the visualised model
        predicted_load_y = plotted_model['y']
        # APE is x in error distribution graph, but y when calculating metrics
        error_APE_y = plotted_model_error['x']
        # Cumulative percentage y, but x in metrics
        error_percent_x = plotted_model_error['y']
        metrics.append(model_metrics.calculate_metrics(
            actual_load_y, predicted_load_y, error_APE_y, error_percent_x))
        if (is_test_data): #increment to skip the test data error data points in the error graph visualisation
            step += 1
    return metrics

#hides the table if there is no models, returns the style if there is models
def update_metrics_container_style(models):
    if (len(models)):
        return {'text-align': 'center'}
    return {'display': 'none'}
