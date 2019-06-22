import unittest
from datetime import datetime
import pandas as pd
from component.graph.error_model.util.error_model_graph_util import generate_model_error_traces
from numpy.testing import assert_array_equal


class generate_model_error_traces_test(unittest.TestCase):
    def test_return_model_traces(self):
        load_graph = {'data': [{'y': [10, 5, 20, 5],'name':'Actual Load', 'x':[datetime(1970, 1, 1),
        datetime(1970, 1, 2), datetime(1970, 1, 3), datetime(1970, 1, 4)]},
        {'y': [5, 10, 20, 20], 'x':[datetime(1970, 1, 1),
        datetime(1970, 1, 2), datetime(1970, 1, 3), datetime(1970, 1, 4)], 'name':'model1', 'marker': {'color': 'red'}}]}
        models = [dict(model_name='model1', displacement_value=0,
                           displacement_unit='Half Hours')]
        test_data_start_date = None
        test_data_end_date = None
        highlight_variable = 'None'
        highlight_value = 'None'
        load_data = []
        output = generate_model_error_traces(load_data, load_graph, models, test_data_start_date, test_data_end_date, highlight_variable, highlight_value)
        self.assertEqual(len(output), 1)
        assert_array_equal(output[0]['x'], [0., 50., 100., 300.])
        assert_array_equal(output[0]['y'], [25., 50., 75., 100.])
        assert_array_equal(output[0]['text'], ['1970-01-03 00:00:00', '1970-01-01 00:00:00',
       '1970-01-02 00:00:00', '1970-01-04 00:00:00'])