from component.graph.util.graph_util import generate_graph, generate_traces, get_highlighted_entries_dataframe
from component.model.displacement import displacement_model
from component.model.regression import regression_model
from component.graph.util.graph_colors import actual_load_color, highlight_color
import pandas as pd

#returns a generated load visualisation graph with the trace datapoints dependent on input values
def add_visualised_graph(load_data, start_date, end_date, models=[], x_axis_layout={'title': 'Date', 'tickformat': '%a %Y-%m-%d %H:%M'},
                         y_axis='Load', highlight_variable='None', highlight_value='None'):

    if start_date == None or end_date == None: #if there is a start and end date of visualised data specified
        return None #div is empty - no graph visible

    #gets all the data points - actual load, highlighted values and model forecast traces to plot onto the graph
    traces = get_visualised_traces(load_data, start_date, end_date, y_axis)
    traces = get_highlighted_traces(
        traces, highlight_variable, highlight_value, load_data, start_date, end_date, y_axis)
    traces = get_model_traces(
        traces, models, load_data, start_date, end_date, y_axis)

    return generate_graph(traces, x_axis_layout, y_axis, show_legend=True)

#returns the visualised load data traces
def get_visualised_traces(load_data, start_date, end_date, y_axis):
    visualised_load_data = load_data[(
        load_data.Date >= start_date) & (load_data.Date <= end_date)]
    visualised_traces = generate_traces(
        visualised_load_data['Date'], visualised_load_data[y_axis], 'Actual Load', color=actual_load_color)
    return visualised_traces

#returns the highlighted load traces superimposed onto the visualised load data traces
def get_highlighted_traces(traces, highlight_variable, highlight_value, load_data, start_date, end_date, y_axis):
    visualised_load_data = load_data[(
        load_data.Date >= start_date) & (load_data.Date <= end_date)]
    if (highlight_variable != 'None' and highlight_value != 'None'): #if there is highlighted data points specified
        highlighted_load_data = pd.DataFrame() #structure to hold data entries that are highlighted 
        highlighted_load_data['Date'], highlighted_load_data['y_axis'] = zip(*visualised_load_data.apply(
            lambda row: get_highlighted_entries_dataframe(row, highlight_variable, highlight_value, y_axis), axis=1))
        highlighted_traces = generate_traces(
            highlighted_load_data['Date'], highlighted_load_data['y_axis'], 'Highlighted Load', color=highlight_color, line_width=2)
        traces.extend(highlighted_traces)
    return traces 

#returns the added load forecasting model's forecast data traces
def get_model_traces(traces, models, load_data, start_date, end_date, y_axis):
    visualised_load_data = load_data[(
        load_data.Date >= start_date) & (load_data.Date <= end_date)]
    for model in models: #iterate through all the forecasting models added
        #get info for generating model forecast data points
        model_name = model['model_name']
        model_color = model['model_color']
        model_type = model['model_type']
        if (model_type == 'displacement'):
            try:
                traces = get_displacement_model_traces(
                    load_data, visualised_load_data, traces, model, model_name, model_color, y_axis, start_date, end_date)
            except:
                continue #cannot build model using the visualised data, skip plotting this model's traces
        # if y_axis is not 'Load' then this is called by characteristics graph, cannot plot model traces
        elif (model_type == 'regression' and y_axis == 'Load'):
            try:
                traces = get_regression_model_traces(
                    load_data, visualised_load_data, traces, model, model_name, model_color, y_axis, start_date, end_date)
            except:
                continue #error with building the linear regression model on visualised data, skip plotting this model's traces
    return traces

# calculates a load forecast for a displacement model
def get_displacement_model_traces(load_data, visualised_load_data, traces, model, model_name, model_color, y_axis, start_date, end_date):
    predicted_load_data = displacement_model.predict(
        load_data, start_date, end_date, model)
    assert (len(visualised_load_data) == len(predicted_load_data)) # prevents plotting a model when not all displaced data is available
    predicted_load_traces = generate_traces(
        visualised_load_data['Date'], predicted_load_data[y_axis], model_name, predicted_load_data['Date'].tolist(), color=model_color)
    traces.extend(predicted_load_traces)
    return traces

#calculates a load forecast for linear regression model
def get_regression_model_traces(load_data, visualised_load_data, traces, model, model_name, model_color, y_axis, start_date, end_date):
    try:
        predicted_load_data = regression_model.predict(
            load_data, start_date, end_date, model, y_axis)
    except Exception as predict_error:
        raise predict_error
    
    predicted_load_traces = generate_traces(
        visualised_load_data['Date'], predicted_load_data, model_name, color=model_color)
    traces.extend(predicted_load_traces)
    return traces
