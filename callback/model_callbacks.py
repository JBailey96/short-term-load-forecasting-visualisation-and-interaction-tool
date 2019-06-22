from app import app
from dash.dependencies import Input, Output, State
from state.model import model_state
from component.model import model_selection
from data.data import load_data
from data.util.data_regression_models import regression_models

#updates the list of models added with the model construction input elements as state, 
# and the add model buttons as input to call the callback
@app.callback(
    Output('models', 'children'),
    [Input('plot-displacement-button', 'n_clicks_timestamp'),
     Input('plot-regression-button', 'n_clicks_timestamp'),
     Input('remove-model-button', 'n_clicks_timestamp')],
    [State('displacement', 'value'),
     State('displacement-unit', 'value'),
     State('models', 'children'),
     State('remove-model-selection', 'value'),
     State('regression-model-selection', 'value'),
     State('training-data-date-picker-day-range', 'start_date'),
     State('training-data-date-picker-day-range', 'end_date'),
      State('regression-model-name', 'value')])
def update_model_state(add_displacement_timestamp, add_regression_timestamp, remove_model_timestamp, displacement_value, displacement_unit, plotted_models, remove_model_selection,
                       regression_model_choice, training_start_date, training_end_date, regression_model_name):
    return model_state.update(load_data, regression_models, add_displacement_timestamp, add_regression_timestamp, remove_model_timestamp, displacement_value,
                              displacement_unit, plotted_models, remove_model_selection, regression_model_choice, training_start_date,
                              training_end_date, regression_model_name)

# updates the list of models the user can select to remove
@app.callback(
    Output('remove-model-selection', 'options'),
    [Input('models', 'children')]
)
def update_model_selection_options(models):
    return model_selection.update(models)
