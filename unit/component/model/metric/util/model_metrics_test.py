import unittest
import pandas as pd
from component.model.metric.util.model_metrics import calculate_metrics

class calculate_metrics_test(unittest.TestCase):
    def setUp(self):
        y_true_values = [100, 200, 200]
        y_pred_values = [100, 150., 300.]
        self.y_true = pd.Series(y_true_values)
        self.y_pred = pd.Series(y_pred_values)
        self.error_APE_y = [0, 33.33, 50]
        self.error_percent_x = [33.33, 66.66, 100]

    def test_return_metrics(self):
        metrics = calculate_metrics(self.y_true, self.y_pred, self.error_APE_y, self.error_percent_x)
        self.maxDiff = None
        expected_metrics = {'Mean Absolute Error (MW)': '50', 'Max Over Forecasting Error (MW)': '100','Max Under Forecasting Error (MW)': '50', 
        'Root Mean Squared Error (MW)': '64', 'Mean Absolute Percent Error (%)': '25.0', 
        'Max Absolute Percent Error (%)': '50.0', 'Max Under Forecasting Percent Error (%)': '25.0', 
         'Max Over Forecasting Percent Error (%)':  '50.0', '90% Threshold Absolute Percentage Error (%)': '45.0'}
        self.assertDictEqual(metrics, expected_metrics)