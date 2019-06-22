from data.util.data_regression_models import regression_models


def update_date(model_selection, previous_date, date_type):
    date = previous_date
    if (model_selection == 'None'):
        return date
    
    model = regression_models[model_selection]
    if (model['training']):
        training = model['training']
        date = training[date_type]

    return date