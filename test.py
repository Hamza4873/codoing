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
    try:
        data = json.loads(api_output)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format provided.")

    # If it's a list of dictionaries, we flatten each dictionary
    if isinstance(data, list):
        flat_data = [flatten_json(item) for item in data]
    # If it's a single dictionary, we just flatten it
    elif isinstance(data, dict):
        flat_data = [flatten_json(data)]
    else:
        raise ValueError("API output must be a JSON object or list of JSON objects.")

    df = pd.DataFrame(flat_data)
    return df

# Function to create Databricks multiselect widget
def create_multiselect_widget(df):
    columns = df.columns.tolist()
    dbutils.widgets.multiselect("selected_columns", "", columns, "Select Columns")

# Function to display selected columns in a DataFrame
def display_selected_columns(df):
    selected_columns = dbutils.widgets.get("selected_columns").split(',')
    if selected_columns:
        filtered_df = df[selected_columns]
        display(filtered_df)
    else:
        print("No columns selected.")

# Example usage
api_output = input("Paste your API output data in JSON format (can be a list or a single JSON object): ")

df = parse_api_output(api_output)

# Create the widget to select columns
create_multiselect_widget(df)

# After selecting columns, execute this to show the selected data
display_selected_columns(df)