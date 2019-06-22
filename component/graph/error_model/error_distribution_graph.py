import dash_core_components as dcc
from component.graph.error_model.util.error_model_graph_util import add_error_graph
from datetime import datetime

#returns the generated error distribution graph
def update(load_data, load_graph, models, test_data_start_date, test_data_end_date, highlight_variable, highlight_value):
    children = []
    if (len(models)):
            x_axis_layout = dict(title='Absolute Percentage Error (%)', automargin=True) #sets the x axis label
            children.append(dcc.Graph(id=f'error-graph-{datetime.now()}', figure=add_error_graph(load_data, load_graph, models, test_data_start_date, test_data_end_date, 
            highlight_variable, highlight_value, x_axis_layout))) #adds graph to div child
    return children