import dash_core_components as dcc
from component.graph.visualise_model.util.visualise_model_graph_util import add_visualised_graph
from datetime import datetime

#returns the generated characteristics graph
def update(load_data, start_date, end_date, models, characteristics_y_axis_selection, highlight_variable, highlight_value):
    children = []
    style = calculate_style(models) #calculates the layout style for the characteristics graph
    if (characteristics_y_axis_selection != 'None'):  # if a y axis value is chosen to compare 
        x_axis_layout={'title':'Date', 'tickformat':'%a %Y-%m-%d %H:%M', 'automargin': True} #format of x axis
        children.append(dcc.Graph(id=f'characteristics-graph-{datetime.now()}', figure=add_visualised_graph(
            load_data, start_date, end_date, models, x_axis_layout, characteristics_y_axis_selection, highlight_variable=highlight_variable, highlight_value=highlight_value), style=style))
    return children

#returns the style of the characteristics graph dependent on whether models are plotted or not
def calculate_style(models):
    if (len(models)):  # models are superimposed, need to adjust height for metrics table
        height = '30vh' # reduce height of model, allowing vertical space for the metrics table
    else:
        height = '40vh'

    style = {'height': height, 'width': '98vw'}
    return style
