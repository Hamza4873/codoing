import pandas as pd
import json

# Function to flatten nested dictionaries and force lists to dictionaries
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], name + a + '_')
        elif isinstance(x, list):
            # Force the list to a dict with index as keys
            x = {str(i): item for i, item in enumerate(x)}
            for a in x:
                flatten(x[a], name + a + '_')
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

# Function to ensure API output is treated as a dictionary
def ensure_dict(api_output):
    if isinstance(api_output, list):
        # Wrap the list inside a dictionary with a key "data"
        return {"data": api_output}
    elif isinstance(api_output, dict):
        return api_output
    else:
        raise ValueError("API output must be a list or a dictionary.")

# Function to parse API output into a DataFrame
def parse_api_output(api_output):
    # Ensure it's treated as a dictionary
    api_output = ensure_dict(api_output)
    
    # Flatten the dictionary and ensure forced dict for nested objects
    flat_data = [flatten_json(api_output)]
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
api_output = {
    "user": {"id": 1, "name": "John", "address": [{"city": "New York"}, {"city": "Los Angeles"}]},
    "details": {"age": 30, "preferences": ["sports", "music"]}
}

# Parse the API output into a DataFrame
df = parse_api_output(api_output)

# Create the widget to select columns
create_multiselect_widget(df)

# After selecting columns, execute this to show the selected data
display_selected_columns(df)