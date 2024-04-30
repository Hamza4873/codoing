import pandas as pd
import json

# Sample JSON data
json_data = '''
[
    {
        "Data": {"subdata": "stuff1"},
        "Data2": "stuff",
        "Data3": [{"subdata": "moreStuff1"}]
    },
    {
        "Data": "stuff",
        "Data2": {"subdata": "stuff2"},
        "Data3": [{"subdata": "moreStuff2"}]
    },
    {
        "Data": "stuff",
        "Data2": "stuff"
        // No Data3 in this dictionary
    }
]
'''

def normalize_json_to_dataframe(data, keys):
    data = json.loads(data)

    # Function to normalize data for a given key
    def normalize_and_create(data, key):
        temp_df = pd.json_normalize(data)
        if key in temp_df.columns and isinstance(temp_df[key].dropna().iloc[0], (dict, list)):
            # Extract subdata if it's structured
            return pd.json_normalize(data, record_path=[key], errors='ignore').add_prefix(f"{key}_")
        else:
            # Directly extract as is or fill missing
            return temp_df.get(key).apply(lambda x: {'subdata': x} if not isinstance(x, (dict, list)) else x).pipe(lambda df: pd.json_normalize(df).add_prefix(f"{key}_"))

    data_frames = []

    for key in keys:
        # Check if any item has the key, else create a placeholder column
        if any(key in d for d in data):
            sub_df = normalize_and_create(data, key)
        else:
            sub_df = pd.DataFrame({f"{key}_subdata": [pd.NA]*len(data)})  # Create a column filled with NA

        data_frames.append(sub_df)

    # Merge all DataFrames on their index
    final_df = pd.concat(data_frames, axis=1)
    return final_df

# Specify the keys as a variable
keys = ['Data', 'Data2', 'Data3']
df = normalize_json_to_dataframe(json_data, keys)
print(df)