from component.model.metric.util.model_metrics import absolute_percentage_error
from datetime import datetime
from component.graph.util.graph_util import generate_graph, generate_traces
from component.graph.util.graph_colors import highlight_color
import dash_core_components as dcc
import pandas as pd
from component.model.displacement import displacement_model
from component.model.regression import regression_model
from component.graph.util.graph_colors import model_colors
from component.graph.util.graph_util import get_highlighted_entries_dataframe
from state.model.model_state import get_model_by_name

# adds the error distribution graph to the div container
def add_error_graph(load_data, load_graph, models, test_data_start_date, test_data_end_date, highlight_variable, highlight_value, x_axis_layout):
    load_graph_figure = load_graph[0]['props']['figure'] #the visualised graph data points

    traces = generate_model_error_traces(load_data, load_graph_figure, models,
                                         test_data_start_date, test_data_end_date, highlight_variable, highlight_value)
    return generate_graph(traces, x_axis_layout,
                          'Cumulative Percentage (%)', margin_top=20, show_legend=True)

#generate the APE error datapoints used in the error visualisation graph
def generate_model_error_traces(load_data, graph_figure, models, test_data_start_date, test_data_end_date, highlight_variable, highlight_value):
    actual_load_y = graph_figure['data'][0]['y']
    # if there is highlighted data points, models index >= 2
    if (graph_figure['data'][1]['name'] == 'Highlighted Load'):
        start_index = 2
        highlighted_dates = graph_figure['data'][1]['x']  # list of dates that are highlighted in the visualised models graph
    else:
        start_index = 1
        highlighted_dates = [] #no highlighted dates in the model visualisation graph

    if (test_data_start_date == None or test_data_end_date == None): #if there is test data chosen, need to visualise this
        is_test_data = False
    else:
        is_test_data = True

    model_error_traces = [] #list of traces to plot
    highlighted_data_points = pd.DataFrame(
        columns=['APE', 'Percentage', 'Text']) # structure to contain the highlighted data error points to superimpose onto the graph
    for i in range(start_index, len(graph_figure['data'])): #iterate through all model visualisation points on graph
        plotted_model = graph_figure['data'][i] #the model forecast plotted in the load visualisation graph
        model_error_traces, highlighted_data_points = generate_visualised_error_traces(
            plotted_model, actual_load_y, model_error_traces, highlighted_dates, highlighted_data_points)
        if (is_test_data == True): #test data is chosen, generate test data model error visualisation points
            model_error_traces, highlighted_data_points = generate_test_error_traces(
                plotted_model, models, load_data, test_data_start_date, test_data_end_date, highlight_variable, highlight_value, model_error_traces, highlighted_data_points)
    if (len(highlighted_data_points)): #if there is highlighted points generate their superimposed traces
        highlighted_traces = generate_traces(highlighted_data_points['APE'], highlighted_data_points['Percentage'], 'Highlighted', highlighted_data_points['Text'].tolist(),
                                             color=highlight_color, marker_size=4, mode='markers')
        model_error_traces.extend(highlighted_traces)
    return model_error_traces

# returns the model error data points for the visualised load data, and data points to highlight
def generate_visualised_error_traces(plotted_model, actual_load_y, model_error_traces, highlighted_dates, highlighted_data_points):
    #structure to hold all values needed to generate error data points
    model_error_data = create_model_error_data_visualised(
        plotted_model['x'], plotted_model['y'], actual_load_y, highlighted_dates)
    legend_name = f"{plotted_model['name']} (Visualised)"
    model_color = plotted_model['marker']['color']
    model_error_traces, highlighted_data_points = generate_error_traces(model_error_traces, model_error_data,
                                               legend_name, model_color, highlighted_data_points)
    return model_error_traces, highlighted_data_points

# returns the model error data points for the test load data, and data points to highlight
def generate_test_error_traces(plotted_model, models, load_data, test_data_start_date, test_data_end_date, highlight_variable, highlight_value, model_error_traces, highlighted_data_points):
    model = get_model_by_name(models, plotted_model['name']) #get the model object to get the color of the model
    #structure to hold all values needed to generate error data points
    test_model_error_data = create_model_error_data_test(
        load_data, model, test_data_start_date, test_data_end_date, highlight_variable, highlight_value) 
    legend_name = f"{plotted_model['name']} (Test)"
    model_color = model_colors[plotted_model['marker']['color']]['test']
    model_error_traces, highlighted_data_points = generate_error_traces(model_error_traces, test_model_error_data,
                                               legend_name, model_color, highlighted_data_points)
    return model_error_traces, highlighted_data_points

# generates the model error traces and adds to the list of highlighted data points to superimpose
def generate_error_traces(model_error_traces, model_error_data, legend_name, model_color, highlighted_data_points):
    error_traces = generate_traces(model_error_data['APE'], model_error_data['Percentage'], legend_name, model_error_data['Text'].tolist(),
                                   color=model_color, marker_size=1.5, mode='lines+markers', line_width=2)
    model_error_traces.extend(error_traces)
    highlighted_data_points = highlighted_data_points.append(
        model_error_data[model_error_data['Highlight'] == True], sort=False)
    return model_error_traces, highlighted_data_points

# creates a structure to contain the values needed to generate error traces for the model
def create_model_error_data_visualised(x, predicted_load_y, actual_load_y, highlighted_dates):
    model = pd.DataFrame()
    model['Text'] = x  # FYI this needs to be transformed to new hover data
    model['Highlight'] = model.apply(lambda row: is_highlight_data(
        row['Text'], highlighted_dates), axis=1)
    model = create_model_error_data(model, actual_load_y, predicted_load_y)
    return model

# calculates model forecast error performance over the test data and creates a structure containing the data
# to generate model error traces
def create_model_error_data_test(load_data, model, test_data_start_date, test_data_end_date, highlight_variable, highlight_value):
    #generates model forecast dependent on the model type
    if (model['model_type'] == 'displacement'):
        predicted_load_data = displacement_model.predict(load_data, test_data_start_date, test_data_end_date, model)
        y_pred = predicted_load_data['Load']
    elif (model['model_type'] == 'regression'):
        y_pred = regression_model.predict(
        load_data, test_data_start_date, test_data_end_date, model)
    
    test_data = load_data[(load_data.Date >= test_data_start_date)
                          & (load_data.Date <= test_data_end_date)]
    y_true = test_data['Load']

    highlighted_load_data = pd.DataFrame(columns=['Date'])
    if (highlight_variable != 'None' and highlight_value != 'None'): #there is highlighted data chosen
        highlighted_load_data['Date'], highlighted_load_data['y_axis'] = zip(#get highlighted data entries
            *test_data.apply(lambda row: get_highlighted_entries_dataframe(row, highlight_variable, highlight_value, 'Load'), axis=1))
    model_error_df = pd.DataFrame()
    model_error_df = create_model_error_data_visualised(
        test_data['Date'], y_pred, y_true, highlighted_load_data['Date'].tolist()) #generate model error data traces
    return model_error_df

# adds to the model structure by calculating the x and y values of the error graph
def create_model_error_data(model, actual_load_y, predicted_load_y):
    model['APE'] = absolute_percentage_error(
        actual_load_y, predicted_load_y)    

    model = model.sort_values(by=['APE'])

    num_model_points = len(model)
    model['Index'] = range(1, num_model_points+1)

    model['Percentage'] = model.apply(lambda row: calculate_cumulative_percentage(
        row['Index'], num_model_points), axis=1)

    return model

# calculates cumulative percentage - y value for error distribution graph
def calculate_cumulative_percentage(index, num_points):
    percent_of_data = (index/num_points) * 100
    return percent_of_data

# returns whether the date of the model plot is highlighted in the visualised load graph
def is_highlight_data(date, highlighted_dates):
    if date in highlighted_dates: 
        return True
    return False
