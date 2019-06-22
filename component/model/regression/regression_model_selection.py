from data.util.data_regression_models import regression_models

def get_options():
    options = []
    for model_name in regression_models.keys():
        options.append({'label': model_name, 'value': model_name})

    return options