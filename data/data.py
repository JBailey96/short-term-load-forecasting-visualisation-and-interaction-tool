import pandas as pd
import json
from user_parameters import csv_file_name

load_data = pd.read_csv(f"./data/load_data/{csv_file_name}.csv", parse_dates=['Date'])

try:
    with open(f"./data/load_data/{csv_file_name}_config.json") as f:
            load_data_config_dict = json.load(f)
except FileNotFoundError:
    load_data_config_dict = {'models': {}}