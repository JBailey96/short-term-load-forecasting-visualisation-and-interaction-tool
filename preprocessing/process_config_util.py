from datetime import timedelta, datetime
import pandas as pd
from enum import Enum

# the types of variables a linear regression can include in its construction
class VariableType(Enum):
    VARIABLE = 1
    DIFFERENTIAL = 2,
    CORRECTION = 3

# processes the model configuration - adding the unique variable columns to the dataset and returning the dataset
def process_config(config_dict, load_data, data_intervals_seconds=1800):
    variables, differential_variables, correction_variables = process_variables(config_dict)
    
    load_data = add_variable_columns(load_data, variables, VariableType.VARIABLE, data_intervals_seconds)
    load_data = add_variable_columns(load_data, differential_variables, VariableType.DIFFERENTIAL, data_intervals_seconds)
    load_data = add_variable_columns(load_data, correction_variables, VariableType.CORRECTION, data_intervals_seconds)
    return load_data

# returns a unique dictionary of the different types of variables in the configuration models
def process_variables(config_dict):
    models = config_dict['models']

    variables = {}
    differential_variables = {}
    correction_variables = {}

    for _, model in models.items():
        if 'variables' in model:
            variables.update(model['variables'])
        if 'differential variables' in model:
            differential_variables.update(model['differential variables'])
        if 'correction variable' in model:
            correction_variables.update(model['correction variable'])

    return variables, differential_variables, correction_variables

# adds the variable column to the load dataset
def add_variable_columns(load_data, variables, variable_type, data_intervals_seconds):
    for variable_name, variable in variables.items():
        if variable_name in load_data: #dataset already contains the variable
            continue
        column = variable['column']
        displacement_value = variable['displacement_value']
        displacement_unit = variable['displacement_unit']

        displaced_data = predict(
            load_data, displacement_value, displacement_unit, data_intervals_seconds)

        if variable_type == VariableType.VARIABLE:
            load_data[variable_name] = displaced_data[column]
        elif variable_type == VariableType.DIFFERENTIAL:
            load_data[variable_name] = load_data[column] - displaced_data[column]
        elif variable_type == VariableType.CORRECTION:
            load_data[variable_name] = displaced_data[column]
            correction_difference_column_name = f'{variable_name} Difference From Derived'
            load_data[correction_difference_column_name] = displaced_data[column] - load_data[column]
    
    return load_data

# returns a displaced load dataset by the defiend displacement_value and displacement_unit
def predict(load_data, displacement_value, displacement_unit, data_intervals_seconds):
    min_date = load_data['Date'].min()
    max_date = load_data['Date'].max()

    start_date = calculate_date(
        min_date, displacement_value, displacement_unit)
    end_date = calculate_date(max_date, displacement_value, displacement_unit)

    load_data = correct_displacement_start_date_not_in_data(
        load_data, start_date, data_intervals_seconds)
    time_displaced_load_data = load_data[(
        load_data.Date >= start_date) & (load_data.Date <= end_date)]
    return time_displaced_load_data

# calculate what the new date will be when a date is displaced by a displacement_value and displacement_unit
def calculate_date(date, displacement_value, displacement_unit):
    minute_map = {
        'Half Hours': 30,
        'Hours': 60,
        'Days': 1440,
        'Weeks': 10080,
        'Months': 40320,
        'Years': 524160
    }
    displacement_minutes = minute_map.get(displacement_unit)
    return date - timedelta(minutes=displacement_minutes*displacement_value)

# handles the start date of the displaced load dataset being before the minimum date of the load dataset. Additional data is concatenated to the start of the dataset.
def correct_displacement_start_date_not_in_data(load_data, start_date, data_intervals_seconds):
    seconds_difference = (load_data['Date'].min()-start_date).total_seconds()

    if (seconds_difference > 0):
        num_data_entries_to_add = int(
            seconds_difference/data_intervals_seconds)
        dates = [start_date + timedelta(seconds=x*data_intervals_seconds)
                 for x in range(0, num_data_entries_to_add)]
        df = pd.DataFrame()
        df['Date'] = dates
        load_data = pd.concat([df, load_data], ignore_index=True, sort=False)

    return load_data
