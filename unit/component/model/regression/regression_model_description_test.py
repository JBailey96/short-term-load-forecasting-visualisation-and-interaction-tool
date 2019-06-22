import unittest
from component.model.regression.regression_model_description import get_model_description
from mock import patch


class GetModelDescription(unittest.TestCase):
    regression_models = {'Test Model': {'variables': ['Temperature Last Day', 'Wind Speed Difference Last Day'],
                                        'correction_variable': 'Load Last Day', 'description': 'ABC123'},
                         'Test Model 2': {'variables': ['Humidity Difference Last Day'], 'correction_variable': None, 'description': ''},
                         'Test Model 3': {'variables': ['Wind Speed Difference Last Day', 'Temperature Last Week'], 'correction_variable': None,
                         'description': ''}}

    @patch('component.model.regression.regression_model_description.regression_models', regression_models)
    def test_return_description(self):
        model_name = 'Test Model'
        expected_model_description = 'ABC123'
        actual_model_description = get_model_description(model_name)
        self.assertEqual(actual_model_description, expected_model_description)

    def test_return_empty_description(self):
        model_name = 'None'
        expected_model_description = ''
        actual_model_description = get_model_description(model_name)
        self.assertEqual(actual_model_description, expected_model_description)