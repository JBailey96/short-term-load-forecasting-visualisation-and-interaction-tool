from app import app
from dash.dependencies import Input, Output, State
from component.graph_control import date_picker_day_range

#Updates the start date of visualisation date picker when uses the increment/decrement panning functionality
@app.callback(
    Output('date-picker-day-range', 'start_date'),
    [Input('increment', 'n_clicks_timestamp'),
     Input('decrement', 'n_clicks_timestamp')],
    [State('date-picker-day-range', 'start_date'),
    State('date-picker-day-range', 'end_date'),
     State('unit-selection', 'value')])
def update_start_date(increment, decrement, start_date, end_date, units):
    return date_picker_day_range.change_date(increment, decrement, start_date, end_date, units)

#Updates the end date of visualisation date picker when uses the increment/decrement panning functionality
@app.callback(
    Output('date-picker-day-range', 'end_date'),
    [Input('increment', 'n_clicks_timestamp'),
     Input('decrement', 'n_clicks_timestamp')],
    [State('date-picker-day-range', 'end_date'),
    State('date-picker-day-range', 'start_date'),
     State('unit-selection', 'value')])
def update_end_date(increment, decrement, end_date, start_date, units):
    return date_picker_day_range.change_date(increment, decrement, end_date, start_date, units)
