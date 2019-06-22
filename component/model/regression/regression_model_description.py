from data.util.data_regression_models import regression_models

def get_model_description(model_name):
    description_string = ''
    if (model_name == 'None'):
        return description_string
    
    description_string = regression_models[model_name]['description']
    
    return description_string
