import json

#returns a list of forecasting models formatted for a dropdown component
def update(models):
    if (models != []):
        models = json.loads(models)

    options = []
    for model in models:
        options.append(
            {'label': model['model_name'], 'value': model['model_name']})

    return options