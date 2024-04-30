import pandas as pd
import numpy as np

def create_flat_dataframe(data):
    # Helper function to flatten the dictionary
    def flatten_data(y):
        out = {}

        def flatten(x, name=''):
            if isinstance(x, dict):
                for a in x:
                    flatten(x[a], name + a + '_')
            elif isinstance(x, list):
                for i, a in enumerate(x):
                    flatten(a, name + str(i) + '_')
            else:
                out[name[:-1]] = x

        flatten(y)
        return out

    # Flattening each item in the data list and creating a list of dictionaries
    my_list = [flatten_data(d) for d in data['data']]

    # Creating DataFrame from the list of dictionaries
    df = pd.DataFrame(my_list)

    # Ensuring all columns from the first item are present in the DataFrame
    if my_list:
        keylist = list(my_list[0].keys())
        for key in keylist:
            if key not in df.columns:
                df[key] = np.nan

    return df

# Example usage
data = {
    'data': [
        {'key1': 'value1', 'key2': {'subkey1': 'subvalue1'}},
        {'key1': 'value2', 'key3': ['listitem1', 'listitem2']}
    ]
}

# Call the function with the example data
df = create_flat_dataframe(data)
print(df)