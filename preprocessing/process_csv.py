import pandas as pd
import process_csv_util
import process_config_util
import json
import time

csv_file_name = input('(Required) Enter the file name of the CSV file:')
load_data = pd.read_csv(f'{csv_file_name}.csv', parse_dates=['Date'])
print('Supported country, provinces and state names can be found in table listed at https://pypi.org/project/holidays/.')
country = input('(Required) Enter the country of origin of the load data.  e.g NorthernIreland : ')
prov = input('(Optional) Enter the province. e.g AG (for Switzerland): ')
state = input('(Optional) Enter the state. e.g TX (for UnitedStates): ')
t = time.process_time()
load_data = process_csv_util.add_year(load_data)
load_data = process_csv_util.add_month(load_data)
load_data = process_csv_util.add_season(load_data)
load_data = process_csv_util.add_day(load_data)
load_data = process_csv_util.add_is_weekend(load_data)
load_data = process_csv_util.add_holiday(load_data, country, prov, state)
load_data = process_csv_util.add_day_of_year(load_data)

elapsed_time_process_date_variables = time.process_time() - t
json_config_file_name = input('(Optional) Enter the file name of the JSON configuration file:')

if (json_config_file_name):
    with open(f'{json_config_file_name}.json') as f:
            config_dict = json.load(f)
    load_data = process_config_util.process_config(config_dict, load_data)

t = time.process_time()
elapsed_time_process_config = time.process_time() - t

load_data.to_csv(f'{csv_file_name}_processed.csv', index=False)
elapsed_time_total = elapsed_time_process_date_variables + elapsed_time_process_config
print(f'Finished. {csv_file_name}_processed.csv created.')
print(f'Time taken: {elapsed_time_total}s.')