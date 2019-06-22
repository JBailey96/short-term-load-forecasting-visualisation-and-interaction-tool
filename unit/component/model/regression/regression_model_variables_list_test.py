import unittest
from component.model.regression.regression_model_variables_list import get_model_variables_list
from mock import patch


class GetModelVariablesList(unittest.TestCase):
    regression_models = {'Test Model': {'variables': ['Temperature Last Day', 'Wind Speed Difference Last Day'],
                                        'correction_variable': 'Load Last Day'},
                         'Test Model 2': {'variables': ['Humidity Difference Last Day'], 'correction_variable': None},
                         'Test Model 3': {'variables': ['Wind Speed Difference Last Day', 'Temperature Last Week'], 'correction_variable': None}}

    @patch('component.model.regression.regression_model_variables_list.regression_models', regression_models)
    def test_return_variables(self):
        model_name = 'Test Model 2'
        expected_model_variables = 'Humidity Difference Last Day'
        actual_model_variables = get_model_variables_list(model_name)
        self.assertEqual(actual_model_variables, expected_model_variables)

    @patch('component.model.regression.regression_model_variables_list.regression_models', regression_models)
    def test_return_multiple_variables(self):
        model_name = 'Test Model 3'
        expected_model_variables = 'Wind Speed Difference Last Day, Temperature Last Week'
        actual_model_variables = get_model_variables_list(model_name)
        self.assertEqual(actual_model_variables, expected_model_variables)

    @patch('component.model.regression.regression_model_variables_list.regression_models', regression_models)
    def test_return_variables_with_correction(self):
        model_name = 'Test Model'
        expected_model_variables = 'Load Last Day (Correction), Temperature Last Day, Wind Speed Difference Last Day'
        actual_model_variables = get_model_variables_list(model_name)
        self.assertEqual(actual_model_variables, expected_model_variables)

    def test_return_no_variables(self):
        model_name = 'None'
        expected_model_variables = ''
        actual_model_variables = get_model_variables_list(model_name)
        self.assertEqual(actual_model_variables, expected_model_variables)
