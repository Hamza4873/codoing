def flatten_dict(d, parent_key=''):
    flat_dict = {}
    for key, value in d.items():
        new_key = f"{parent_key}_{key}" if parent_key else key

        if isinstance(value, dict):
            # Recursive call to handle sub-dictionary
            flat_dict.update(flatten_dict(value, new_key))
        elif isinstance(value, list):
            # Handle list of dictionaries or other elements
            for index, item in enumerate(value):
                if isinstance(item, dict):
                    flat_dict.update(flatten_dict(item, f"{new_key}_{index}"))
                else:
                    flat_dict[f"{new_key}_{index}"] = item
        else:
            flat_dict[new_key] = value

    return flat_dict

# Example usage:
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

# Flatten the dictionary
flattened_dict = flatten_dict(original_dict)
print(flattened_dict)