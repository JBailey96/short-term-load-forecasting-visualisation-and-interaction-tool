import plotly.graph_objs as go
from datetime import datetime, timedelta
import dash_core_components as dcc
import pandas as pd

# generates data trace points for the graph
def generate_traces(x, y, trace_name, text=[], color=None, line_width=1, marker_size=0.5, mode='markers+lines'):
    trace_style_dict = dict(
        x=x,
        y=y,
        mode=mode,
        marker={
            'symbol': 'circle',
            'size': marker_size,
            'line': {'width': 0}
        },
        line={
            'width': line_width
        },
        name=trace_name,
        text=text if text else x,
        hoverinfo='text+y')

    if color != None: #if a color is specified for the graph
        trace_style_dict['marker']['color'] = color #set marker trace colour

    trace0 = go.Scattergl(trace_style_dict)
    data = [trace0]
    return data

# creates a layout for the graph and encapsulates the data and layout to return a plotly graph object in a dict structure
def generate_graph(data, x_axis_layout, y_axis, margin_top=0, show_legend=None):
    layout_dict = dict(
        xaxis=x_axis_layout,
        yaxis={'title': f'{y_axis}'},
        hovermode='closest',
        legend=dict(x=1, y=0.9),
        margin=go.layout.Margin(
            t=margin_top,
            b=0
        ))

    if show_legend != None: #if the legend being hidden or not is specified
        layout_dict['showlegend'] = show_legend #set whether legend is visible

    return {
        'data': data,
        'layout':
            go.Layout(
                layout_dict
            )
    }

# returns x and y axis if the data entry is specified as being highlighted
def get_highlighted_entries_dataframe(row, highlight_variable, highlight_value, y_axis):
    if highlight_variable == 'Holiday' and highlight_value == 'All' and row['Holiday'] != 'Non-Holiday':
        return row['Date'], row[y_axis]
    elif highlight_variable == 'Day' and highlight_value == 'Weekend' and row['Is_Weekend'] == True:
        return row['Date'], row[y_axis]
    elif highlight_variable == 'Day' and highlight_value == 'Workday' and row['Is_Weekend'] == False:
        return row['Date'], row[y_axis]
    elif row[highlight_variable] == highlight_value:
        return row['Date'], row[y_axis]
    return None, None
