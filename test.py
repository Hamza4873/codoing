def extract_keys(d, all_keys=[]):
    for key, value in d.items():
        all_keys.append(key)  # Add the current key to the list
        if isinstance(value, dict):
            # Recursive call to handle sub-dictionary
            extract_keys(value, all_keys)
        elif isinstance(value, list):
            # Iterate over each item in the list if it's a dictionary
            for item in value:
                if isinstance(item, dict):
                    extract_keys(item, all_keys)

    return all_keys

# Example dictionary
original_dict = {
    'object': {
        'subobject': [
            {'key1': 'value1'},
            {'key2': 'value2'}
        ],
        'another_sub': {'key3': 'value3'}
    },
    'second_object': {
        'subobject': [
            {'key4': 'value4'}
        ]
    },
    'direct_key': 'direct_value'
}

# Extract all keys
keys_list = extract_keys(original_dict)
print(keys_list)