# import unittest
# from mock import patch
# from datetime import datetime
# import pandas as pd

# class MinMaxDate(unittest.TestCase):
#     d = {'Date': [datetime(2018, 1, 1, 0), datetime(2018, 1, 1, 1), datetime(2018, 1, 2, 0), datetime(2018, 1, 3, 0),
#                       datetime(2018, 1, 3, 0)], 'Load': [111, 222, 333, 444, 555]}
#     load_data = pd.DataFrame(data=d)

#     @patch('data.util.data_characteristics.load_data', load_data)
#     def test_min_date_returned(self):
#         expected_min_date = '2018-01-01'
#         from data.util.data_characteristics import min_date
#         actual_min_date = min_date
#         self.assertEqual(actual_min_date, expected_min_date)


