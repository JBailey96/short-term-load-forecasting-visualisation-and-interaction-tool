import unittest
import json
from data.util.data_regression_models import process_regression_models


class ProcessRegressionModels(unittest.TestCase):
    def test_return_one_model(self):
        with open('unit/preprocessing/json/one_model_config.json') as f:
            config_dict = json.load(f)
        models = process_regression_models(config_dict)
        expected_models = {'Test Model': {'variables': ['Temperature Last Day', 'Wind Speed Difference Last Day'],
                                          'correction_variable': 'Load Last Day',  'description': 'ABCDEFG', 'training': {'start_date': '2015-01-01',
                                                                                                                          'end_date': '2016-01-01'}}}
        self.assertEqual(models, expected_models)

    def test_return_multiple_models(self):
        with open('unit/preprocessing/json/multiple_model_config.json') as f:
            config_dict = json.load(f)
        models = process_regression_models(config_dict)
        expected_models = {'Test Model': {'variables': ['Temperature Last Day', 'Wind Speed Difference Last Day'],
                                          'correction_variable': 'Load Last Day', 'description': '', 'training': {}},
                           'Test Model 2': {'variables': ['Humidity Difference Last Day'], 'correction_variable': None, 'description': '', 'training': {}},
                           'Test Model 3': {'variables': ['Temperature Last Week'], 'correction_variable': None, 'description': 'ABCDEFG',
                                            'training': {'start_date': '2015-01-01',
                                                         'end_date': '2016-01-01'}}}
        self.assertEqual(models, expected_models)

    def test_return_no_models(self):
        config_dict = {'models': {}}
        models = process_regression_models(config_dict)
        expected_models = {}
        self.assertEqual(models, expected_models)
