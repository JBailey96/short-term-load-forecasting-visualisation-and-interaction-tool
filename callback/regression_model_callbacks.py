from app import app
from dash.dependencies import Input, Output, State
from component.model.regression import regression_model_variables_list, regression_model_description, regression_model_name_input, regression_training_data_date_picker_day_range

# updates the list of input variables dependent on the user's selection of a linear regression model
@app.callback(
    Output('regression-variable-list', 'children'),
    [Input('regression-model-selection', 'value')])
def update_model_variable_list(model_selection):
    return regression_model_variables_list.get_model_variables_list(model_selection)

# updates the description of the linear regression model dependent on the user's selection of a linear regression model
@app.callback(
    Output('description-content', 'children'),
    [Input('regression-model-selection', 'value')])
def update_model_description(model_selection):
    return regression_model_description.get_model_description(model_selection)

# updates the name of the linear regression model dependent on the user's selection of a linear regression model
@app.callback(
    Output('regression-model-name', 'value'),
    [Input('regression-model-selection', 'value')])
def update_model_name_input(model_selection):
    return regression_model_name_input.set_default_model_name(model_selection)

# updates the date of the set start date of the date picker dependent on the user's selection of a linear regression model
@app.callback(
    Output('training-data-date-picker-day-range', 'start_date'),
    [Input('regression-model-selection', 'value')],
    [State('training-data-date-picker-day-range', 'start_date')])
def update_start_date(model_selection, start_date):
    return regression_training_data_date_picker_day_range.update_date(model_selection, start_date, 'start_date')

# updates the date of the set end date of the date picker dependent on the user's selection of a linear regression model
@app.callback(
    Output('training-data-date-picker-day-range', 'end_date'),
    [Input('regression-model-selection', 'value')],
    [State('training-data-date-picker-day-range', 'end_date')])
def update_end_date(model_selection, end_date):
    return regression_training_data_date_picker_day_range.update_date(model_selection, end_date, 'end_date')
