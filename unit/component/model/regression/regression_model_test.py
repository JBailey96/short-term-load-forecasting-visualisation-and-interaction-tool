import unittest
from datetime import datetime
import pandas as pd
from component.model.regression.regression_model import fit_to_training, predict
from mock import patch


class FitToTrainingTest(unittest.TestCase):
    def setUp(self):
        d = {'Date': [datetime(2018, 1, 1, 0), datetime(2018, 1, 1, 1), datetime(2018, 1, 2, 0), datetime(2018, 1, 3, 0),
                      datetime(2018, 1, 3, 0)], 'Load': [111, 222, 333, 444, 555], 'Temperature': [1, 2, 3, 4, 5],
             'Load Last Week': [222, 444, 666, 888, 1110], 'Load Last Week Difference From Derived': [111, 222, 333, 444, 555]}
        self.load_data = pd.DataFrame(data=d)

    def test_return_fitted_coefficient_and_intercept(self):
        training_start_date = '2018-01-02'
        training_end_date = '2018-01-03'
        model = {'variables': ['Temperature'], 'correction_variable': None}
        expected_output = {'coefficients': [111.0], 'intercept': 0}
        output = fit_to_training(
            self.load_data, model, training_start_date, training_end_date)
        self.assertEqual(len(output['coefficients']), 1)
        self.assertEqual(
            round(output['coefficients'][0], 0), expected_output['coefficients'][0])
        self.assertEqual(round(output['intercept'], 0),
                         expected_output['intercept'])

    def test_return_multiple_fitted_coefficient_and_intercept(self):
        training_start_date = '2018-01-02'
        training_end_date = '2018-01-03'
        model = {'variables': ['Temperature',
                               'Load Last Week'], 'correction_variable': None}
        expected_output = {'coefficients': [0, 0.5], 'intercept': 0}
        output = fit_to_training(
            self.load_data, model, training_start_date, training_end_date)
        self.assertEqual(len(output['coefficients']), 2)
        self.assertEqual(
            round(output['coefficients'][0], 0), expected_output['coefficients'][0])
        self.assertEqual(
            round(output['coefficients'][1], 1), expected_output['coefficients'][1])
        self.assertEqual(round(output['intercept'], 0),
                         expected_output['intercept'])

    def test_return_corrected_load_coefficients_and_intercept(self):
        training_start_date = '2018-01-02'
        training_end_date = '2018-01-03'
        model = {'variables': ['Temperature'],
                 'correction_variable': 'Load Last Week'}
        expected_output = {'coefficients': [111], 'intercept': 0}
        output = fit_to_training(
            self.load_data, model, training_start_date, training_end_date)
        self.assertEqual(len(output['coefficients']), 1)
        self.assertEqual(
            round(output['coefficients'][0], 0), expected_output['coefficients'][0])
        self.assertEqual(round(output['intercept'], 0),
                         expected_output['intercept'])


class PredictTest(unittest.TestCase):
    def setUp(self):
        d = {'Date': [datetime(2018, 1, 1, 0), datetime(2018, 1, 1, 1), datetime(2018, 1, 2, 0), datetime(2018, 1, 3, 0),
                      datetime(2018, 1, 3, 0)], 'Load': [111, 222, 333, 444, 555], 'Temperature': [1, 2, 3, 4, 5],
             'Load Last Week': [222, 444, 666, 888, 1110], 'Load Last Week Difference From Derived': [111, 222, 333, 444, 555]}
        self.load_data = pd.DataFrame(data=d)

    def test_predict_load(self):
        model = dict(coefficients=[5.0], intercept=20, x_columns=[
                     'Temperature'], corrected_column=None)
        start_date = '2018-01-01'
        end_date = '2018-01-02'
        expected_output = [25, 30, 35]
        output = predict(self.load_data, start_date, end_date,
                         model)
        self.assertEqual(expected_output, output)

    def test_predict_load_multiple_coefficients(self):
        model = dict(coefficients=[5.0, 1.0], intercept=100, x_columns=[
                     'Temperature', 'Load Last Week'], corrected_column=None)
        start_date = '2018-01-02'
        end_date = '2018-01-03'
        expected_output = [781, 1008, 1235]
        output = predict(self.load_data, start_date, end_date,
                         model)
        self.assertEqual(expected_output, output)

    def test_predict_load_with_corrected_column(self):
        model = dict(coefficients=[5.0], intercept=20, x_columns=[
                     'Temperature'], corrected_column='Load Last Week')
        start_date = '2018-01-01'
        end_date = '2018-01-02'
        expected_output = [197, 414, 631]
        output = predict(self.load_data, start_date, end_date, model)
        self.assertEqual(expected_output, output)

    def test_predict_error_start_date_exceeds_end_date(self):
        model = dict(coefficients=[5.0], intercept=20, x_columns=[
                     'Temperature'], corrected_column='Load Last Week')
        start_date = '2018-01-20' #bad start date
        end_date = '2018-01-02'
        self.assertRaises(Exception, predict, self.load_data, start_date, end_date, model)

    def test_predict_error_end_date_before_start_date(self):
        model = dict(coefficients=[5.0], intercept=20, x_columns=[
                     'Temperature'], corrected_column='Load Last Week')
        start_date = '2018-01-01'
        end_date = '2017-01-01' #bad end date
        self.assertRaises(Exception, predict, self.load_data, start_date, end_date, model)
