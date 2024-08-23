import pandas as pd
import json

# Function to flatten nested dictionaries
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

# Function to parse API output into a DataFrame
def parse_api_output(api_output):
    # If it's a list of dictionaries, flatten each dictionary
    if isinstance(api_output, list):
        flat_data = [flatten_json(item) for item in api_output]
    # If it's a single dictionary, flatten it
    elif isinstance(api_output, dict):
        flat_data = [flatten_json(api_output)]
    else:
        raise ValueError("API output must be a list or a dictionary.")

    df = pd.DataFrame(flat_data)
    return df

# Function to create Databricks multiselect widget
def create_multiselect_widget(df):
    columns = df.columns.tolist()
    dbutils.widgets.multiselect("selected_columns", "", columns, "Select Columns")

# Function to display selected columns in a DataFrame
def display_selected_columns(df):
    selected_columns = dbutils.widgets.get("selected_columns").split(',')
    
    # Check if any columns are selected, and if not, select all columns by default
    if selected_columns == ['']:
        selected_columns = df.columns.tolist()
        
    filtered_df = df[selected_columns]
    display(filtered_df)

# Example API response (replace this with your actual data)
api_output = [
    {"id": 1, "name": "John", "info": {"age": 30, "city": "New York"}},
    {"id": 2, "name": "Jane", "info": {"age": 25, "city": "Los Angeles"}}
]

# Parse the API output into a DataFrame
df = parse_api_output(api_output)

# Create the widget to select columns
create_multiselect_widget(df)

# After selecting columns, execute this to show the selected data
display_selected_columns(df)