import unittest
import pandas as pd
from mock import patch
from component.graph_control.characteristics_selection import get_options
from data.data import load_data

class GetOptionsTest(unittest.TestCase):
    load_data_with_columns = pd.DataFrame(columns=['Column1', 'Column2'])
    load_data_no_columns = pd.DataFrame()

    @patch('component.graph_control.characteristics_selection.load_data', load_data_with_columns)
    def test_return_options_load_data_with_columns(self):
        expected_options = [{'label': 'None', 'value': 'None'}, {'label': 'Column1', 'value':'Column1'},
        {'label':'Column2', 'value':'Column2'}]
        actual_options = get_options()
        self.assertEqual(actual_options, expected_options)
    
    @patch('component.graph_control.characteristics_selection.load_data', load_data_no_columns)
    def test_return_options_load_data_no_columns(self):
        expected_options = [{'label': 'None', 'value': 'None'}]
        actual_options = get_options()
        self.assertEqual(actual_options, expected_options)