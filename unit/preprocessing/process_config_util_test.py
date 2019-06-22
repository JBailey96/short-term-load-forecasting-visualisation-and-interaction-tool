import unittest
from preprocessing.process_config_util import process_variables, add_variable_columns, correct_displacement_start_date_not_in_data, process_config, VariableType
import json
from datetime import datetime
import pandas as pd
from pandas.testing import assert_frame_equal


num_seconds_day = 86400
num_seconds_half_hour = 1800


class ProcessVariablesTest(unittest.TestCase):
    def test_one_model(self):
        with open('unit/preprocessing/json/one_model_config.json') as f:
            config_dict = json.load(f)
        variables, differential_variables, correction_variables = process_variables(
            config_dict)
        expected_variables = {
            "Temperature Last Day": {
                "column": "Temperature",
                "displacement_unit": "Days",
                "displacement_value": 1
            }
        }
        expected_differential_variables = {
            "Wind Speed Difference Last Day": {
                "column": "Wind speed",
                "displacement_unit": "Days",
                "displacement_value": 1
            }
        }
        expected_correction_variables = {
            "Load Last Day": {
                "column": "Load",
                "displacement_unit": "Days",
                "displacement_value": 1
            }
        }
        self.assertEqual(variables, expected_variables)
        self.assertEqual(differential_variables,
                         expected_differential_variables)
        self.assertEqual(correction_variables, expected_correction_variables)

    def test_multiple_models(self):
        with open('unit/preprocessing/json/multiple_model_config.json') as f:
            config_dict = json.load(f)
        variables, differential_variables, correction_variables = process_variables(
            config_dict)
        expected_variables = {
            "Temperature Last Day": {
                "column": "Temperature",
                "displacement_unit": "Days",
                "displacement_value": 1
            },
            "Temperature Last Week": {
                "column": "Temperature",
                "displacement_unit": "Weeks",
                "displacement_value": 1
            }
        }
        expected_differential_variables = {
            "Wind Speed Difference Last Day": {
                "column": "Wind speed",
                "displacement_unit": "Days",
                "displacement_value": 1
            },
            "Humidity Difference Last Day": {
                "column": "Humidity",
                "displacement_unit": "Days",
                "displacement_value": 1
            }
        }
        expected_correction_variables = {
            "Load Last Day": {
                "column": "Load",
                "displacement_unit": "Days",
                "displacement_value": 1
            }
        }
        self.assertEqual(variables, expected_variables)
        self.assertEqual(differential_variables,
                         expected_differential_variables)
        self.assertEqual(correction_variables, expected_correction_variables)


class AddVariableColumns(unittest.TestCase):
    def setUp(self):
        d = {'Date': [datetime(1969, 12, 30), datetime(
            1969, 12, 31), datetime(1970, 1, 1)], 'Load': [1, 2, 3]}
        self.load_data = pd.DataFrame(data=d)

    def test_add_one_variable_column(self):
        variables = {"Test Variable": {
            "column": "Load",
            "displacement_unit": "Days",
            "displacement_value": 1
        }}

        load_data_with_new_columns = add_variable_columns(
            self.load_data, variables, VariableType.VARIABLE, num_seconds_day)

        expected_d = {'Date': [datetime(1969, 12, 30), datetime(1969, 12, 31), datetime(1970, 1, 1)], 'Load': [1, 2, 3],
                      'Test Variable': [None, 1, 2]}
        expected_load_data = pd.DataFrame(data=expected_d)

        assert_frame_equal(load_data_with_new_columns, expected_load_data)

    def test_add_one_variable_column_with_existing_variable(self):
        variables = {
            "Load": {
                "column": "Load",
                "displacement_unit": "Days",
                "displacement_value": 1
            }}

        load_data_with_new_columns = add_variable_columns(
            self.load_data, variables, VariableType.VARIABLE, num_seconds_day)

        expected_load_data = self.load_data

        assert_frame_equal(load_data_with_new_columns, expected_load_data)

    def test_add_multiple_variable_columns(self):
        variables = {"Test Variable": {
            "column": "Load",
            "displacement_unit": "Days",
            "displacement_value": 1
        },
            "Test Variable 2": {
            "column": "Load",
            "displacement_unit": "Days",
            "displacement_value": 1
        },
        }

        load_data_with_new_columns = add_variable_columns(
            self.load_data, variables, VariableType.VARIABLE, num_seconds_day)

        expected_d = {'Date': [datetime(1969, 12, 30), datetime(1969, 12, 31), datetime(1970, 1, 1)], 'Load': [1, 2, 3],
                      'Test Variable': [None, 1, 2], 'Test Variable 2': [None, 1, 2]}
        expected_load_data = pd.DataFrame(data=expected_d)

        assert_frame_equal(load_data_with_new_columns, expected_load_data)

    def test_add_one_differential_variable_column(self):
        variables = {"Test Differential Variable": {
            "column": "Load",
            "displacement_unit": "Days",
            "displacement_value": 1
        }}

        load_data_with_new_columns = add_variable_columns(
            self.load_data, variables, VariableType.DIFFERENTIAL, num_seconds_day)
        expected_d = {'Date': [datetime(1969, 12, 30), datetime(1969, 12, 31), datetime(1970, 1, 1)], 'Load': [1, 2, 3],
                      'Test Differential Variable': [None, 1, 1]}
        expected_load_data = pd.DataFrame(data=expected_d)

        assert_frame_equal(load_data_with_new_columns, expected_load_data)

    def test_add_one_correction_variable_column(self):
        variables = {"Test Correction Variable": {
            "column": "Load",
            "displacement_unit": "Days",
            "displacement_value": 1
        }}

        load_data_with_new_columns = add_variable_columns(
            self.load_data, variables, VariableType.CORRECTION, num_seconds_day)

        expected_d = {'Date': [datetime(1969, 12, 30), datetime(1969, 12, 31), datetime(1970, 1, 1)], 'Load': [1, 2, 3],
                      'Test Correction Variable': [None, 1, 2], 'Test Correction Variable Difference From Derived': [None, -1, -1]}
        expected_load_data = pd.DataFrame(data=expected_d)

        assert_frame_equal(load_data_with_new_columns, expected_load_data)

    def test_add_one_variable_column_half_hours(self):
        d = {'Date': [datetime(1970, 1, 1, 0, 0), datetime(
            1970, 1, 1, 0, 30), datetime(1970, 1, 1, 1, 0)], 'Load': [1, 2, 3]}
        half_hour_load_data = pd.DataFrame(data=d)

        variables = {"Test Variable": {
            "column": "Load",
            "displacement_unit": "Half Hours",
            "displacement_value": 1
        }}

        load_data_with_new_columns = add_variable_columns(
            half_hour_load_data, variables, VariableType.VARIABLE, num_seconds_half_hour)

        expected_d = {'Date': [datetime(1970, 1, 1, 0, 0), datetime(
            1970, 1, 1, 0, 30), datetime(1970, 1, 1, 1, 0)], 'Load': [1, 2, 3],
            'Test Variable': [None, 1, 2]}
        expected_load_data = pd.DataFrame(data=expected_d)

        assert_frame_equal(load_data_with_new_columns, expected_load_data)


class CorrectDisplacementStartDateNotInData(unittest.TestCase):
    def test_correct_dataframe(self):
        d = {'Date': [datetime(1969, 12, 30),
                      datetime(1970, 1, 1), datetime(1970, 1, 3)], 'Load': [1, 2, 3]}
        load_data = pd.DataFrame(data=d)

        start_date = datetime(1969, 12, 28)
        data_intervals_seconds = num_seconds_day*2

        expected_d = {'Date': [datetime(1969, 12, 28),
                               datetime(1969, 12, 30), datetime(1970, 1, 1), datetime(1970, 1, 3)], 'Load': [None, 1, 2, 3]}
        expected_load_data = pd.DataFrame(data=expected_d)

        output_load_data = correct_displacement_start_date_not_in_data(
            load_data, start_date, data_intervals_seconds)

        assert_frame_equal(output_load_data, expected_load_data)

    def test_do_not_correct(self):
        d = {'Date': [datetime(1970, 1, 1, 12, 0),
                      datetime(1970, 1, 1, 12, 30), datetime(1970, 1, 1, 13, 0)], 'Load': [1, 2, 3]}
        load_data = pd.DataFrame(data=d)

        start_date = datetime(1970, 1, 1, 12, 0)
        data_intervals_seconds = 1800  # 1 half hour

        expected_load_data = load_data

        output_load_data = correct_displacement_start_date_not_in_data(
            load_data, start_date, data_intervals_seconds)

        assert_frame_equal(output_load_data, expected_load_data)


class ProcessConfigTest(unittest.TestCase):
    def setUp(self):
        d = {'Date': [datetime(1969, 12, 30), datetime(
            1969, 12, 31), datetime(1970, 1, 1)], 'Load': [1, 2, 3], 'Temperature': [4, 5, 6], 'Humidity': [7, 8, 9], 'Wind speed': [10, 11, 12]}
        self.load_data = pd.DataFrame(data=d)

    def test_process_one_model_config(self):
        with open('unit/preprocessing/json/one_model_config.json') as f:
            config_dict = json.load(f)
        output_load_data = process_config(
            config_dict, self.load_data, num_seconds_day)
        expected_d = {'Date': [datetime(1969, 12, 30), datetime(
            1969, 12, 31), datetime(1970, 1, 1)], 'Load': [1, 2, 3], 'Temperature': [4, 5, 6], 'Humidity': [7, 8, 9], 'Wind speed': [10, 11, 12],
            'Temperature Last Day': [None, 4, 5], 'Wind Speed Difference Last Day': [None, 1, 1], 'Load Last Day': [None, 1, 2], 'Load Last Day Difference From Derived': [None, -1, -1]}
        expected_load_data = pd.DataFrame(data=expected_d)
        assert_frame_equal(output_load_data, expected_load_data)

    def test_process_multiple_model_config(self):
        with open('unit/preprocessing/json/multiple_model_config.json') as f:
            config_dict = json.load(f)

        expected_d = {'Date': [datetime(1969, 12, 30), datetime(
            1969, 12, 31), datetime(1970, 1, 1)], 'Load': [1, 2, 3], 'Temperature': [4, 5, 6], 'Humidity': [7, 8, 9], 'Wind speed': [10, 11, 12],
            'Temperature Last Day': [None, 4, 5], 'Temperature Last Week': [None, None, None], 'Wind Speed Difference Last Day': [None, 1, 1],  'Humidity Difference Last Day': [None, 1, 1],
            'Load Last Day': [None, 1, 2], 'Load Last Day Difference From Derived': [None, -1, -1]}
        expected_load_data = pd.DataFrame(data=expected_d)
        expected_load_data['Temperature Last Week'] = pd.to_numeric(
            expected_load_data['Temperature Last Week'])

        output_load_data = process_config(
            config_dict, self.load_data, num_seconds_day)
        assert_frame_equal(output_load_data, expected_load_data)

    def test_process_one_model_two_variables_config_existing_column(self):
        with open('unit/preprocessing/json/one_model_config_two_variables.json') as f:
            config_dict = json.load(f)
        load_data = self.load_data.copy(deep=True)
        load_data['Temperature Last Day'] =  [None, 4, 5]
        output_load_data = process_config(
            config_dict, load_data, num_seconds_day)
        expected_d = {'Date': [datetime(1969, 12, 30), datetime(
            1969, 12, 31), datetime(1970, 1, 1)], 'Load': [1, 2, 3], 'Temperature': [4, 5, 6], 'Humidity': [7, 8, 9], 'Wind speed': [10, 11, 12],
            'Temperature Last Day': [None, 4, 5], 'Humidity Last Day': [None, 7, 8]}
        expected_load_data = pd.DataFrame(data=expected_d)
        assert_frame_equal(output_load_data, expected_load_data)