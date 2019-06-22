from app import app
from dash.dependencies import Input, Output, State
from component.graph_control import date_highlight_value_selection

#updates the list of highlight values depending on the highlighted variable chosen
@app.callback(
    Output('date-highlight-value-selection', 'options'),
    [Input('date-highlight-variable-selection', 'value')])
def update_highlight_values_options(highlight_variable):
    return date_highlight_value_selection.get_options(highlight_variable)