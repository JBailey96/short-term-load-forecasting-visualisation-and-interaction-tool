from data.data import load_data_config_dict

def process_regression_models(load_data_config_dict):
    models = load_data_config_dict['models']
    
    models_dict = {}
    for model_name, model in models.items():
        model_dict = {}
        variables = []
        correction_variable = None
        description = ''
        training = {}
        
        if 'variables' in model:
            variables.extend(model['variables'].keys())
        if 'differential variables' in model:
            variables.extend(model['differential variables'].keys())
        if 'correction variable' in model:
            correction_variable = list(model['correction variable'].keys())[0]
        if 'description' in model:
            description = model['description']
        if 'training' in model:
            training = model['training']
            
        model_dict = dict(variables=variables, correction_variable=correction_variable,
        description=description, training=training)
        models_dict[model_name] = model_dict
    return models_dict

regression_models = process_regression_models(load_data_config_dict)