from data.util.data_regression_models import regression_models

def get_model_variables_list(model_name):
    variable_list_string = ''
    if (model_name == 'None'):
        return variable_list_string
    
    model = regression_models[model_name]
    correction_variable = model['correction_variable']
    if (correction_variable):
        correction_variable = model['correction_variable']
        correction_variable = model['correction_variable'] + ' (Correction), '
        variable_list_string = correction_variable

    variables_list = model['variables']
    variable_list_string += (", ".join(variables_list))

    return variable_list_string