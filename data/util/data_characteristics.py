from data.data import load_data

min_date = load_data['Date'].min().strftime("%Y-%m-%d")
max_date = load_data['Date'].max().strftime("%Y-%m-%d")

holidays = load_data['Holiday'].unique()
years = load_data['Year'].unique()