from data.data import load_data

# from the dataset gets the list of columns in the dataset and returns a list formatted for the dropdown component in the layout
def get_options():
    options = []
    options.append({'label': 'None', 'value': 'None'}) #option to not show a characteristics graph
    
    for column in load_data.columns:
        options.append({'label': column, 'value': column})

    return options