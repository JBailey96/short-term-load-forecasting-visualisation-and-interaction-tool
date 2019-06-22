import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from math import sqrt

#returns a dictionary of metrics that calculate the error performance of the model forecasted load values with the actual load values.
def calculate_metrics(y_true, y_pred, error_APE_y, error_percent_x):
    mae = f"{int(mean_absolute_error(y_true, y_pred))}"
    mape = f"{round(mean_absolute_percentage_error(y_true, y_pred), 2)}"

    max_over_forecast_error = f"{int(maximum_over_forecasting_error(y_true, y_pred))}"
    max_absolute_forecast_error_percent = f"{round(maximum_absolute_forecasting_percent_error(y_true, y_pred), 2)}"

    max_under_forecast_error = f"{int(maximum_under_forecasting_error(y_true, y_pred))}"
    max_under_forecast_error_percent = f"{round(maximum_under_forecasting_percent_error(y_true, y_pred), 2)}"

    root_mean_squared_error = f"{int(sqrt(mean_squared_error(y_true, y_pred)))}"

    max_over_forecasting_percent_error = f"{round(maximum_over_forecasting_percent_error(y_true, y_pred),2)}"
    
    ninety_percent_absolute_percentage_error = f"{round(linear_interpolated_absolute_percentage_error(90, error_APE_y, error_percent_x)[0],2)}"
    
    metrics = {'Mean Absolute Error (MW)': mae, 'Max Over Forecasting Error (MW)': max_over_forecast_error,  'Max Under Forecasting Error (MW)': max_under_forecast_error, 
      'Root Mean Squared Error (MW)': root_mean_squared_error, 'Mean Absolute Percent Error (%)': mape, 'Max Absolute Percent Error (%)': max_absolute_forecast_error_percent, 
      'Max Under Forecasting Percent Error (%)': max_under_forecast_error_percent, 'Max Over Forecasting Percent Error (%)': max_over_forecasting_percent_error,
      '90% Threshold Absolute Percentage Error (%)': ninety_percent_absolute_percentage_error}
    return metrics

def mean_absolute_percentage_error(y_true, y_pred): 
    return np.mean(absolute_percentage_error(y_true, y_pred))

def absolute_percentage_error(y_true, y_pred): 
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.abs((y_true - y_pred) / y_true) * 100

def maximum_over_forecasting_error(y_true, y_pred):
    maxdiff = 0
    for true, pred in zip(y_true, y_pred):
        difference = pred - true
        if (difference > maxdiff):
            maxdiff = difference
    return maxdiff

def maximum_absolute_forecasting_percent_error(y_true, y_pred):
    maxdiff = 0
    for true, pred in zip(y_true, y_pred):
        difference = abs(((true - pred) / true) * 100)
        if (difference > maxdiff):
            maxdiff = difference
    return maxdiff

def maximum_over_forecasting_percent_error(y_true, y_pred):
    mindiff = 0
    for true, pred in zip(y_true, y_pred):
        difference = ((true - pred) / true) * 100
        if (mindiff > difference):
            mindiff = difference
    return abs(mindiff)

def maximum_under_forecasting_error(y_true, y_pred):
    maxdiff = 0
    for true, pred in zip(y_true, y_pred):
        difference = true - pred
        if (difference > maxdiff):
            maxdiff = difference
    return maxdiff

def maximum_under_forecasting_percent_error(y_true, y_pred):
    maxdiff = 0
    for true, pred in zip(y_true, y_pred):
        difference = ((true - pred) / true) * 100
        if (difference > maxdiff):
            maxdiff = difference
    return maxdiff

#returns the specified percent value threshold of what the absolute percentage error y is given the list of APEs
def linear_interpolated_absolute_percentage_error(APE, error_APE_y, error_percent_x):
    return np.interp([APE],error_percent_x, error_APE_y)