import dash_core_components as dcc
from component.graph.visualise_model.util.visualise_model_graph_util import add_visualised_graph
from datetime import datetime

#returns the generated load visualisation graph
def update(load_data, start_date, end_date, models, characteristics_y_axis_selection, highlight_variable, highlight_value):
    children = []
    style = calculate_style(models, characteristics_y_axis_selection) #calculate layout style for load graph
    x_axis_layout = calculate_x_axis_layout(characteristics_y_axis_selection) #calculate the x axis layout for load graph
    children.append(dcc.Graph(id=f'load-data-graph-{datetime.now()}', figure=add_visualised_graph(
            load_data, start_date, end_date, models, x_axis_layout, highlight_variable=highlight_variable,
            highlight_value=highlight_value), style=style))
    return children

# returns the modified height of the graph dependent on the characteristics graph being visible and/or models added
def calculate_style(models, characteristics_y_axis_selection):
    if (characteristics_y_axis_selection == 'None') and (len(models) == 0): #no characteristic chosen and no models added
        height = '80vh'
    elif (characteristics_y_axis_selection == 'None') and (len(models)): # no characteristic chosen and models added
        height = '60vh'
    elif (characteristics_y_axis_selection != 'None') and (len(models)) :#characteristic chosen and models added
        height = '30vh'
    else: 
        height = '40vh' #characteristics chosen and no models added
    style = {'height': height, 'width': '98vw'}
    return style

# returns the x axis layout of the graph dependent on whether a characteristics graph visible
def calculate_x_axis_layout(characteristics_y_axis_selection):
    if (characteristics_y_axis_selection == 'None'): #if characteristics not chosen
        x_axis_layout = dict(title='Date', tickformat='%a %Y-%m-%d %H:%M', automargin=True)
    else:
        x_axis_layout = dict(showticklabels=False) #do not show an x axis if characteristics chosen - share with the characteristics graph
    return x_axis_layout