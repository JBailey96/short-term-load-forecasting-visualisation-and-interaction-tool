import unittest
import pandas as pd
from component.model.metric.model_metrics_table import update_values, update_metrics_container_style
from unittest.mock import MagicMock
from mock import patch
from datetime import datetime
import json


class update_values_test(unittest.TestCase):

    def setUp(self):
        d = {'Date': [datetime(2018, 1, 1, 0), datetime(2018, 1, 1, 1), datetime(2018, 1, 2, 0), datetime(2018, 1, 3, 0),
                      datetime(2018, 1, 3, 0)], 'Load': [111, 222, 333, 444, 555]}
        self.load_data = pd.DataFrame(data=d)

        model_error_data = {'APE': [], 'Percentage':[]}
        self.model_error_df = pd.DataFrame(data=model_error_data)

    @patch('component.model.metric.util.model_metrics.calculate_metrics')
    def test_return_table_with_visualised_metrics(self, mock_function):
        mock_function.return_value = {'metric1': 1234}
        graph = [{'props': {'figure': {'data': [{'y': [1],'name':'Actual Load'}, {'y': [2], 'name':'model1'},
         {'y': [3], 'name':'model2'}]}}}]
        error_distribution_graph = [{'props': {'figure': {'data': [{'x': [100], 'y': [100], 'name':'model1'},
         {'x': [200],'y': [100], 'name': 'model2'}]}}}]
        load_data = None
        test_data_start_date = None
        test_data_end_date = None
        models = [dict(model_name='model1', displacement_value=48,
                           displacement_unit='Half Hours')]
        output = (str(update_values(graph, models, load_data, test_data_start_date, test_data_end_date, 
        error_distribution_graph)[0]))
        self.assertIn("metric1", output)
        self.assertIn("1234", output)
        self.assertIn("model1", output)
        self.assertNotIn('model2', output)
        self.assertIn("Visualised", output)
        self.assertNotIn("Test Data", output)

    @patch('component.model.metric.util.model_metrics.calculate_metrics')
    def test_return_table_with_visualised_metrics_highlighted_data_error_distribution_graph(self, mock_function):
        mock_function.return_value = {'metric1': 1234}
        graph = [{'props': {'figure': {'data': [{'y': [1],'name':'Actual Load'}, {'y': [2], 'name':'Highlighted Load'},
         {'y': [3], 'name':'model1'}]}}}]
        error_distribution_graph = [{'props': {'figure': {'data': [{'x': [100], 'y': [100], 'name':'model1'},
         {'x': [200],'y': [100], 'name': 'Highlighted'}]}}}]
        load_data = None
        test_data_start_date = None
        test_data_end_date = None
        models = [dict(model_name='model1', displacement_value=48,
                           displacement_unit='Half Hours')]
        output = (str(update_values(graph, models, load_data, test_data_start_date, test_data_end_date, 
        error_distribution_graph)[0]))
        self.assertIn("metric1", output)
        self.assertIn("1234", output)
        self.assertIn("model1", output)
        self.assertNotIn('model2', output)
        self.assertIn("Visualised", output)
        self.assertNotIn("Test Data", output)
    
    @patch('component.model.metric.util.model_metrics.calculate_metrics')
    def test_return_table_with_visualised_metrics_multiple_models(self, mock_function):
        mock_function.return_value = {'metric1': 1234}
        load_graph = [{'props': {'figure': {'data': [{'y': [1], 'name':'Actual Load'}, {'y': [2], 'name':'model1'}, 
        {'y': [3], 'name': 'model2'}]}}}]
        error_distribution_graph = [{'props': {'figure': {'data': [{'x': [100], 'y': [100], 'name':'model1'},
         {'x': [200],'y': [100], 'name': 'model2'}]}}}]
        load_data = None
        test_data_start_date = None
        test_data_end_date = None
        models = [dict(model_name='model1', displacement_value=48,
                           displacement_unit='Half Hours'), dict(model_name='model2', displacement_value=48,
                           displacement_unit='Half Hours')]
        output = (str(update_values(load_graph, models, load_data, test_data_start_date, test_data_end_date, 
        error_distribution_graph)[0]))
        self.assertIn("metric1", output)
        self.assertIn("1234", output)
        self.assertIn("model1", output)
        self.assertIn('model2', output)
        self.assertIn("Visualised", output)
        self.assertNotIn("Test Data", output)

    def test_not_return_visualised_metrics_table(self):
        graph = [{'props': {'figure': {'data': [{'y': [1]}]}}}]
        models = []
        load_data = None
        test_data_start_date = None
        test_data_end_date = None
        error_distribution_graph = []
        output = (str(update_values(graph, models, load_data, test_data_start_date, test_data_end_date, error_distribution_graph)))
        self.assertEqual(output, 'None')
    
    @patch('component.model.displacement.displacement_model.predict')
    @patch('component.model.metric.util.model_metrics.calculate_metrics')
    @patch('component.model.metric.model_metrics_table.create_model_error_data')
    def test_return_table_with_test_data_metrics(self, create_model_error_data_mock_function, metrics_mock_function, displacement_mock_function):
        graph = [{'props': {'figure': {'data': [{'y': [1], 'name':'Actual Load'}, {'y': [2], 'name':'model1'}]}}}]
        error_distribution_graph = [{'props': {'figure': {'data': [{'x': [100], 'y': [100], 'name':'model1'}]}}}]
        metrics_mock_function.return_value = {'metric1': 1234}
        displacement_mock_function.return_value = self.load_data
        create_model_error_data_mock_function.return_value = self.model_error_df
        test_data_start_date = '2018-01-01'
        test_data_end_date = '2018-01-02'
        models = [dict(model_name='model1', displacement_value=10, model_type='displacement',
                           displacement_unit='Half Hours')]
        output = (str(update_values(graph, models, self.load_data, test_data_start_date, test_data_end_date, 
        error_distribution_graph)[0]))
        self.assertIn("metric1", output)
        self.assertIn("1234", output)
        self.assertIn("model1", output)
        self.assertNotIn("model2", output) 
        self.assertIn("Test Data", output)
        self.assertIn("Visualised", output)

        
    
    @patch('component.model.regression.regression_model.predict')
    @patch('component.model.displacement.displacement_model.predict')
    @patch('component.model.metric.util.model_metrics.calculate_metrics')
    @patch('component.model.metric.model_metrics_table.create_model_error_data')
    def test_return_table_with_test_data_metrics_multiple_models(self, create_model_error_data_mock_function, metrics_mock_function, displacement_mock_function, regression_mock_function):
        metrics_mock_function.return_value = {'metric1': 1234}
        displacement_mock_function.return_value = self.load_data
        regression_mock_function.return_value = [5678]
        create_model_error_data_mock_function.return_value = self.model_error_df
        test_data_start_date = '2018-01-01'
        test_data_end_date = '2018-01-02'
        graph = [{'props': {'figure': {'data': [{'y': [1],'name':'Actual Load'}, {'y': [2], 'name':'Highlighted Load'},
         {'y': [3], 'name':'model2'}]}}}]
        error_distribution_graph = [{'props': {'figure': {'data': [{'x': [100], 'y': [100], 'name':'model1'},
         {'x': [200],'y': [100], 'name': 'model2'}, {'x': [200],'y': [100], 'name': 'model3'}]}}}]
        models = [dict(model_name='model1', displacement_value=10, model_type='displacement',
                           displacement_unit='Half Hours'), dict(model_name='model2', displacement_value=10, model_type='displacement',
                           displacement_unit='Hours'), dict(model_name='model3', model_type='regression', model_color='red', coefficients=[111.0], intercept=0,
                       x_columns=["Temperature"], corrected_column=None)]
        output = (str(update_values(graph, models, self.load_data, test_data_start_date, test_data_end_date, 
        error_distribution_graph)[0]))
        self.assertIn("metric1", output)
        self.assertIn("1234", output)
        self.assertIn("model1", output)
        self.assertIn("model2", output)
        self.assertIn("model3", output)
        self.assertIn("Test Data", output)
        self.assertIn("Visualised", output)

    def test_not_return_test_data_metrics_table_no_models(self):
        graph = [{'props': {'figure': {'data': [{'y': [1]}]}}}]
        test_data_start_date = '2018-01-01'
        test_data_end_date = '2018-01-02'
        models = []
        error_distribution_graph = []
        output = (str(update_values(graph, models, self.load_data, test_data_start_date, test_data_end_date, error_distribution_graph)))
        self.assertEqual(output, 'None')

class update_metrics_container_style_test(unittest.TestCase):
    def test_no_models(self):
        models = []
        output = update_metrics_container_style(models)
        self.assertEqual(output, {'display': 'none'})

    def test_model(self):
        models = [dict(model_name='model1', displacement_value=10,
                           displacement_unit='Half Hours')]
        output = update_metrics_container_style(models)
        self.assertEqual(output, {'text-align': 'center'})