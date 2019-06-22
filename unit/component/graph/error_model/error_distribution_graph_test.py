import unittest
from datetime import datetime
import pandas as pd
from component.graph.error_model.error_distribution_graph import update
from numpy.testing import assert_array_equal
from mock import patch

class update_error_distribution_graph_test(unittest.TestCase):
    def setUp(self):
        d = {'Date': [datetime(1969, 12, 30), datetime(1969, 12, 31), datetime(1970, 1, 1)], 'Load': [1, 2, 3], 'Day': ['Tuesday', 'Wednesday', 'Thursday']}
        self.load_data = pd.DataFrame(data=d)

    def test_single_model_update(self):
        load_graph = [{'props': {'figure': {'data': [{'y': [1],'name':'Actual Load', 'x':[datetime(1970, 1, 1)]},
        {'y': [3], 'x':[datetime(1970, 1, 1)], 'name':'model1', 'marker':{'color': 'red'}}]}}}]
        models = [dict(model_name='model1', displacement_value=48,
                           displacement_unit='Half Hours')]
        test_data_start_date = None
        test_data_end_date = None
        highlight_variable = 'None'
        highlight_value = 'None'
        load_data = []
        output = update(load_data, load_graph, models, test_data_start_date, test_data_end_date, highlight_variable, highlight_value)
        self.assertEqual(len(output[0].figure['data']), 1)
        self.assertEqual(output[0].figure['layout']['xaxis']['automargin'], True)
        self.assertEqual(output[0].figure['layout']['xaxis']['title'], 'Absolute Percentage Error (%)')
        self.assertEqual(output[0].figure['layout']['showlegend'], True)

    @patch('component.graph.error_model.util.error_model_graph_util.model_colors', {'red' : {'test': 'blue'}})
    def test_single_model_with_test_data_update(self):
        load_graph = [{'props': {'figure': {'data': [{'y': [1],'name':'Actual Load', 'x':[datetime(1970, 1, 1)]},
        {'y': [3], 'x':[datetime(1970, 1, 1)], 'name':'model1', 'marker':{'color': 'red'}}]}}}]
        models = [dict(model_name='model1', model_type='displacement', displacement_value=48,
                           displacement_unit='Half Hours')]
        test_data_start_date = '1969-12-31'
        test_data_end_date = '1970-01-01'
        highlight_variable = 'None'
        highlight_value = 'None'
        output = update(self.load_data, load_graph, models, test_data_start_date, test_data_end_date, highlight_variable, highlight_value)
        self.assertEqual(len(output[0].figure['data']), 2)
        self.assertEqual(output[0].figure['data'][0]['marker']['color'], 'red')
        self.assertEqual(output[0].figure['data'][0]['name'], 'model1 (Visualised)')
        self.assertEqual(output[0].figure['data'][1]['marker']['color'], 'blue')
        self.assertEqual(output[0].figure['data'][1]['name'], 'model1 (Test)')
        assert_array_equal(output[0].figure['data'][1]['text'], ['1970-01-01 00:00:00', '1969-12-31 00:00:00'])


    @patch('component.graph.error_model.util.error_model_graph_util.model_colors', {'red' : {'test': 'blue'}, 'green': {'test': 'black'}})
    @patch('component.graph.error_model.util.error_model_graph_util.regression_model.predict')
    def test_multiple_model_with_test_data_update(self, regression_prediction_function):
        regression_prediction_function.return_value = [50]
        load_graph = [{'props': {'figure': {'data': [{'y': [1],'name':'Actual Load', 'x':[datetime(1970, 1, 1)]},
        {'y': [3], 'x':[datetime(1970, 1, 1)], 'name':'model1', 'marker':{'color': 'red'}},
        {'y': [5], 'x':[datetime(1970, 1, 1)], 'name':'model2', 'marker':{'color': 'green'}}]}}}]
        models = [dict(model_name='model1', model_type='displacement', displacement_value=48,
                           displacement_unit='Half Hours'), dict(model_name='model2', model_type='regression', model_color='green', coefficients=[111.0], intercept=0,
                       x_columns=["Temperature"], corrected_column=None)]
        test_data_start_date = '1969-12-31'
        test_data_end_date = '1970-01-01'
        highlight_variable = 'None'
        highlight_value = 'None'
        output = update(self.load_data, load_graph, models, test_data_start_date, test_data_end_date, highlight_variable, highlight_value)
        self.assertEqual(len(output[0].figure['data']), 4)
        self.assertEqual(output[0].figure['data'][0]['marker']['color'], 'red')
        self.assertEqual(output[0].figure['data'][0]['name'], 'model1 (Visualised)')
        self.assertEqual(output[0].figure['data'][1]['marker']['color'], 'blue')
        self.assertEqual(output[0].figure['data'][1]['name'], 'model1 (Test)')
        assert_array_equal(output[0].figure['data'][1]['text'], ['1970-01-01 00:00:00', '1969-12-31 00:00:00'])
        self.assertEqual(output[0].figure['data'][2]['marker']['color'], 'green')
        self.assertEqual(output[0].figure['data'][2]['name'], 'model2 (Visualised)')
        self.assertEqual(output[0].figure['data'][3]['marker']['color'], 'black')
        self.assertEqual(output[0].figure['data'][3]['name'], 'model2 (Test)')

    def test_single_model_highlighted_update(self):
        load_graph = [{'props': {'figure': {'data': [{'y': [1],'name':'Actual Load', 'x':[datetime(1970, 1, 1)]},
        {'y': [1],'name':'Highlighted Load', 'x':[datetime(1970, 1, 1)], 'text':[datetime(1970, 1, 1)]},
        {'y': [3], 'x':[datetime(1970, 1, 1)], 'name':'model1', 'marker': {'color': 'red'}}]}}}]
        models = [dict(model_name='model1', displacement_value=48,
                           displacement_unit='Half Hours')]
        test_data_start_date = None
        test_data_end_date = None
        highlight_variable = 'Highlight Variable'
        highlight_value = 'Highlight Value'
        load_data = []
        output = update(load_data, load_graph, models, test_data_start_date, test_data_end_date, highlight_variable, highlight_value)
        self.assertEqual(len(output[0].figure['data']), 2)
        self.assertEqual(output[0].figure['data'][1]['name'], 'Highlighted')
        assert_array_equal(output[0].figure['data'][1]['text'], ['1970-01-01 00:00:00'])

    def test_single_model_highlighted_update_empty(self):
        load_graph = [{'props': {'figure': {'data': [{'y': [1],'name':'Actual Load', 'x':[datetime(1970, 1, 1)]},
        {'y': [1],'name':'Highlighted Load', 'x':[None], 'text':[None]},
        {'y': [3], 'x':[datetime(1970, 1, 1)], 'name':'model1', 'marker': {'color': 'red'}}]}}}]
        models = [dict(model_name='model1', displacement_value=48,
                           displacement_unit='Half Hours')]
        test_data_start_date = None
        test_data_end_date = None
        highlight_variable = 'Highlight Variable'
        highlight_value = 'Highlight Value'
        load_data = []
        output = update(load_data, load_graph, models, test_data_start_date, test_data_end_date, highlight_variable, highlight_value)
        self.assertEqual(len(output[0].figure['data']), 1)
        self.assertEqual(output[0].figure['data'][0]['name'], 'model1 (Visualised)')


    @patch('component.graph.error_model.util.error_model_graph_util.model_colors', {'red' : {'test': 'blue'}})
    def test_single_model_highlighted_with_test_data_update(self):
        load_graph = [{'props': {'figure': {'data': [{'y': [1],'name':'Actual Load', 'x':[datetime(1970, 1, 1)]},
        {'y': [1],'name':'Highlighted Load', 'x':[datetime(1970, 1, 1)], 'text':[datetime(1970, 1, 1)]},
        {'y': [3], 'x':[datetime(1970, 1, 1)], 'name':'model1', 'marker': {'color': 'red'}}]}}}]
        models = [dict(model_name='model1', displacement_value=48, model_type='displacement',
                           displacement_unit='Half Hours')]
        test_data_start_date = '1969-12-31'
        test_data_end_date = '1970-01-01'
        highlight_variable = 'Day'
        highlight_value = 'Wednesday'
        output = update(self.load_data, load_graph, models, test_data_start_date, test_data_end_date, highlight_variable, highlight_value)
        self.assertEqual(len(output[0].figure['data']), 3)
        self.assertEqual(output[0].figure['data'][2]['name'], 'Highlighted')
        assert_array_equal(output[0].figure['data'][0]['text'], ['1970-01-01 00:00:00'])
        assert_array_equal(output[0].figure['data'][1]['text'], ['1970-01-01 00:00:00', '1969-12-31 00:00:00'])
        assert_array_equal(output[0].figure['data'][2]['text'], ['1970-01-01 00:00:00', '1969-12-31 00:00:00'])

    def test_multiple_model_update(self):
        load_graph = [{'props': {'figure': {'data': [{'y': [1],'name':'Actual Load', 'x':[datetime(1970, 1, 1)]},
        {'y': [3], 'x':[datetime(1970, 1, 1)], 'marker':{'color':'red'}, 'name':'model1'}, 
        {'y': [10], 'x':[datetime(1970, 1, 1)], 'marker':{'color': 'red'},
         'name':'model2'}]}}}]
        models = [dict(model_name='model1', displacement_value=48,
                           displacement_unit='Half Hours'), dict(model_name='model2', displacement_value=96,
                           displacement_unit='Hours')]
        test_data_start_date = None
        test_data_end_date = None
        highlight_variable = 'None'
        highlight_value = 'None'
        load_data = []
        output = update(load_data, load_graph, models, test_data_start_date, test_data_end_date, highlight_variable, highlight_value)
        self.assertEqual(len(output[0].figure['data']), 2)
        self.assertEqual(output[0].figure['layout']['xaxis']['automargin'], True)
        self.assertEqual(output[0].figure['layout']['xaxis']['title'], 'Absolute Percentage Error (%)')

    def test_multiple_model_highlighted_update(self):
        load_graph = [{'props': {'figure': {'data': [{'y': [1, 2],'name':'Actual Load', 'x':[datetime(1970, 1, 1), datetime(1970, 1, 2)]},
        {'y': [1, None],'name':'Highlighted Load', 'x':[datetime(1970, 1, 1)], 'text':[datetime(1970, 1, 1)]}, {'y': [3, 4], 'x':[datetime(1970, 1, 1), datetime(1970, 1, 2)], 'name':'model1', 'marker':{'color':'red'}}, 
        {'y': [5, 6], 'x':[datetime(1970, 1, 1), datetime(1970, 1, 2)], 'name':'model2', 'marker':{'color':'red'}}]}}}]
        models = [dict(model_name='model1', displacement_value=48,
                           displacement_unit='Half Hours'), dict(model_name='model2', displacement_value=96,
                           displacement_unit='Hours')]
        test_data_start_date = None
        test_data_end_date = None
        highlight_variable = 'Highlight Variable'
        highlight_value = 'Highlight Value'
        load_data = []
        output = update(load_data, load_graph, models, test_data_start_date, test_data_end_date, highlight_variable, highlight_value)
        self.assertEqual(len(output[0].figure['data']), 3)
        self.assertEqual(output[0].figure['data'][2]['name'], 'Highlighted')
        assert_array_equal(output[0].figure['data'][2]['text'], ['1970-01-01 00:00:00', '1970-01-01 00:00:00'])
    
    def test_no_models_update(self):
        load_graph = [{'props': {'figure': {'data': [{'y': [1],'name':'Actual Load', 'x':[datetime(1970, 1, 1)]}]}}}]
        models = []
        test_data_start_date = None
        test_data_end_date = None
        highlight_variable = 'None'
        highlight_value = 'None'
        load_data = []
        output = update(load_data, load_graph, models, test_data_start_date, test_data_end_date, highlight_variable, highlight_value)
        self.assertEqual(output, [])

    def test_no_models_highlighted_update(self):
        load_graph = [{'props': {'figure': {'data': [{'y': [1],'name':'Actual Load', 'x':[datetime(1970, 1, 1)]},
        {'y': [1],'name':'Highlighted Load', 'x':[datetime(1970, 1, 1)]}]}}}]
        models = []
        test_data_start_date = None
        test_data_end_date = None
        highlight_variable = 'Highlight Variable'
        highlight_value = 'Highlight Value'
        load_data = []
        output = update(load_data, load_graph, models, test_data_start_date, test_data_end_date, highlight_variable, highlight_value)
        self.assertEqual(output, [])


    