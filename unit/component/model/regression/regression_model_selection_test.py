import unittest
from component.model.regression.regression_model_selection import get_options
from mock import patch


class GetOptionsTest(unittest.TestCase):
    regression_models = {'Test Model': {'variables': ['Temperature Last Day', 'Wind Speed Difference Last Day'],
                                        'correction_variable': 'Load Last Day'},
                         'Test Model 2': {'variables': ['Humidity Difference Last Day'], 'correction_variable': None},
                         'Test Model 3': {'variables': ['Temperature Last Week'], 'correction_variable': None}}

    @patch('component.model.regression.regression_model_selection.regression_models', regression_models)
    def test_get_options(self):
        expected_options = [{'label': 'Test Model', 'value': 'Test Model'},
                            {'label': 'Test Model 2', 'value': 'Test Model 2'},
                            {'label': 'Test Model 3', 'value': 'Test Model 3'}]
        actual_options = get_options()
        self.assertEqual(actual_options, expected_options)

    @patch('component.model.regression.regression_model_selection.regression_models', {})
    def test_no_options_returned(self):
        expected_options = []
        actual_options = get_options()
        self.assertEqual(actual_options, expected_options)
