from datetime import datetime
from sklearn.linear_model import LinearRegression
import numpy as np

#fitting the linear regression model to the training dataset, returning a list of coefficients and an intercept. 
def fit_to_training(load_data, model, training_start_date, training_end_date, y_column='Load'):
    training_start_date = datetime.strptime(training_start_date, "%Y-%m-%d")
    training_end_date = datetime.strptime(training_end_date, "%Y-%m-%d")
    
    x_columns = model['variables']
    corrected_column = model['correction_variable']

    training_load_data_df = load_data[(load_data['Date'] >= training_start_date) & (load_data['Date'] <= training_end_date)]
    
    if (corrected_column == None):
        y_train = training_load_data_df[y_column]
    else:
        y_train = training_load_data_df[f'{corrected_column} Difference From Derived']
    
    x_train = training_load_data_df[x_columns]

    regressor = LinearRegression()
    regressor.fit(x_train, y_train)
    
    
    model_fit = {'coefficients': regressor.coef_.tolist(), 'intercept': regressor.intercept_.tolist()}
    return model_fit

# produces predicted load values for the given range of dataset using the model input variables with the trained linear regression model
def predict(load_data, start_date, end_date, model, y_column='Load'):
    coefficients = model['coefficients']
    intercept = model['intercept']
    x_columns = model['x_columns']
    corrected_column = model['corrected_column']
    
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    test_data_df = load_data[(load_data['Date'] >= start_date) & (load_data['Date'] <= end_date)]
    
    x_test = test_data_df[x_columns]

    regressor = LinearRegression()
    regressor.coef_ = np.array(coefficients)
    regressor.intercept_ = np.array(intercept)

    try:
        y_pred = regressor.predict(x_test)
    except Exception as predict_error:
        raise predict_error
        
    if (corrected_column != None):
        y_pred = test_data_df[corrected_column] - y_pred
    
    return y_pred.tolist()