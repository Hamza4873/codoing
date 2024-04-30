def rearrange_dict(d, parent_key=''):
    # Function to recursively rearrange the dictionary
    items = []
    new_dict = {}
    
    for key, value in d.items():
        new_key = f"{parent_key}_{key}" if parent_key else key
        if isinstance(value, dict):
            # Recursive call to handle sub-dictionary
            new_dict.update(rearrange_dict(value, new_key))
        else:
            # Collect items to be added later to ensure subdictionaries come first
            items.append((new_key, value))
    
    # Add non-dictionary items at the end of the current scope
    new_dict.update(items)
    
    return new_dict

# Example usage:
original_dict = {
    'object': {
        'subobject': {'key1': 'value1'},
        'another_sub': {'key2': 'value2'}
    },
    'second_object': {
        'subobject': {'key3': 'value3'}
    }
}

# Rearrange the dictionary
rearranged_dict = rearrange_dict(original_dict)
print(rearranged_dict)