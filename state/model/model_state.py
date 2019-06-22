import json
from component.graph.util.graph_colors import model_colors
from component.model.regression import regression_model


#appends the displacement model to the existing model state
def add_displacement(displacement_value, displacement_unit, plotted_models):
    model_color = calculate_model_color(plotted_models)
    model_name = f'{displacement_value*-1} {displacement_unit}'
    model_type = 'displacement'
    plotted_models.append(dict(model_name=model_name, model_type=model_type,
                               model_color=model_color, displacement_value=displacement_value,
                               displacement_unit=displacement_unit))
    return plotted_models

#appends the linear regression model to the existing model state
def add_regression(load_data, regression_models, plotted_models, model_choice, training_start_date, training_end_date, regression_model_name):
    model_color = calculate_model_color(plotted_models)
    model = regression_models[model_choice]
    model_fit = regression_model.fit_to_training(
        load_data, model, training_start_date, training_end_date)
    model_name = regression_model_name
    model_type = 'regression'
    coefficients = model_fit['coefficients']
    intercept = model_fit['intercept']
    x_columns = model['variables']
    corrected_column = model['correction_variable']

    plotted_models.append(dict(model_name=model_name, model_type=model_type, model_color=model_color, coefficients=coefficients, intercept=intercept,
                               x_columns=x_columns, corrected_column=corrected_column))
    return plotted_models

#returns the colour of an added model - a colour that has not been used by another model
def calculate_model_color(plotted_models):
    colors = []
    for model in plotted_models:
        m_color = model['model_color']
        colors.append(m_color)
    for color in model_colors:
        if color not in colors:
            return color # model colour is not used by any other model
    return model_colors[len(plotted_models) % len(model_colors)] #model colours are all taken - then the least used model colour is chosen again

#remove a model by using the model name key
def remove_model(plotted_models, remove_model_selection):
    for model in plotted_models:
        model_name = model['model_name']
        if (model_name == remove_model_selection):
            plotted_models.remove(model)
            break
    return plotted_models

#the interface to the model state logic - handles all the different flows that occur when using models.
def update(load_data, regression_models, add_displacement_timestamp, add_regression_timestamp, remove_model_timestamp, displacement_value,
           displacement_unit, plotted_models, remove_model_selection, regression_model_choice, training_start_date,
           training_end_date, regression_model_name):
    if (plotted_models != []):
        plotted_models = json.loads(plotted_models)

    add_displacement_timestamp = int(add_displacement_timestamp)
    remove_model_timestamp = int(remove_model_timestamp)
    add_regression_timestamp = int(add_regression_timestamp)

    max_timestamp = max(add_displacement_timestamp,
                        remove_model_timestamp, add_regression_timestamp)
    if remove_model_timestamp == max_timestamp:
        plotted_models = remove_model(plotted_models, remove_model_selection)
    elif add_displacement_timestamp == max_timestamp:
        plotted_models = add_displacement(
            displacement_value, displacement_unit, plotted_models)
    elif add_regression_timestamp == max_timestamp:
        plotted_models = add_regression(load_data, regression_models, plotted_models,
                                        regression_model_choice, training_start_date, training_end_date, regression_model_name)

    return json.dumps(plotted_models)

#returns the model dictionary item by using the model name key value to search the models dictionary
def get_model_by_name(models, model_name):
    for model in models:
        if (model['model_name'] == model_name):
            return model
    return None
