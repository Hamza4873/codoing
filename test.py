import pandas as pd

def flatten_dict(d, parent_key='', sep='.'):
    """
    Fully flatten a nested dictionary, ensuring that all nested levels are flattened.
    Concatenates keys using the separator `sep` and includes all breadcrumb levels.
    
    Parameters:
    - d: The dictionary to flatten.
    - parent_key: The base key used for recursion (used internally).
    - sep: The separator used for concatenating keys.
    
    Returns:
    - A fully flattened dictionary with keys showing all levels of breadcrumbs.
    """
    items = []
    for k, v in d.items():
        # Keep all levels of breadcrumbs in the key
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        
        if isinstance(v, dict):
            # Recursively flatten nested dictionaries
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))  # Add flattened key-value pair
    return dict(items)

def combine_dataframes(df1, df2):
    """
    Combine two DataFrames by aligning on their indexes. This is useful if we want to 
    add nested fields to the original DataFrame.
    """
    return pd.concat([df1, df2], axis=1)

def parse_nested_fields(api_response):
    """
    Parses the given API response and returns a DataFrame based on the user's choice of fields, 
    including all breadcrumb levels for nested fields.
    
    Parameters:
    - api_response: A dictionary or list of dictionaries representing the API response.

    Returns:
    - A pandas DataFrame containing the selected fields.
    """
    # Flatten the API response if it's nested
    if isinstance(api_response, dict):
        api_response = [api_response]
    
    # Flatten each entry in the response to handle nested objects
    flat_responses = [flatten_dict(entry) for entry in api_response]
    
    # Get all possible fields (keys) from the flattened response
    all_fields = set()
    for entry in flat_responses:
        all_fields.update(entry.keys())
    
    # Display the available fields to the user
    print("\nAvailable fields:")
    all_fields = list(all_fields)  # Convert set to list for indexing
    for idx, field in enumerate(all_fields):
        print(f"{idx + 1}. {field}")

    # Ask the user which fields they want to include in the DataFrame
    while True:
        try:
            selected_indices = input("\nEnter the numbers of the fields you want to include, separated by commas: ")
            selected_indices = [int(i.strip()) for i in selected_indices.split(',')]
            selected_fields = [all_fields[i - 1] for i in selected_indices]
            break
        except (IndexError, ValueError):
            print("Invalid input. Please enter the numbers corresponding to the fields.")

    # Confirm selected fields with the user
    print(f"\nYou have selected the following fields: {', '.join(selected_fields)}")

    # Extract the selected fields from the API response
    parsed_data = []
    for entry in flat_responses:
        parsed_entry = {field: entry.get(field, None) for field in selected_fields}
        parsed_data.append(parsed_entry)

    # Create a DataFrame with the selected fields
    df = pd.DataFrame(parsed_data)

    return df

def process_api_output(api_output):
    """
    This function processes the API output and allows the user to parse fields, 
    including all breadcrumb levels, into a DataFrame.

    Parameters:
    - api_output: A dictionary or list of dictionaries from the API.

    Returns:
    - None: Prints the DataFrame.
    """
    # Check if the output is valid
    if not isinstance(api_output, (list, dict)):
        print("Invalid API output format. It must be a list or dictionary.")
        return
    
    # Parse fields and create a DataFrame
    df = parse_nested_fields(api_output)
    
    # Display the resulting DataFrame
    print("\nFinal Parsed DataFrame:")
    print(df)

# Example usage with simulated API output containing nested objects
if __name__ == "__main__":
    # Simulate some API output with nested objects
    example_api_output = [
        {
            "file_hash": "123abc", 
            "detection_ratio": "20/60", 
            "scan_date": "2024-01-01",
            "metadata": {
                "scanners": {
                    "total": 60,
                    "detected": 20
                },
                "size": 1024,
                "sub_metadata": {
                    "extra_info": "some info",
                    "details": {
                        "level": 5
                    }
                }
            }
        },
        {
            "file_hash": "456def", 
            "detection_ratio": "5/60", 
            "scan_date": "2024-01-02",
            "metadata": {
                "scanners": {
                    "total": 60,
                    "detected": 5
                },
                "size": 2048
            }
        }
    ]
    
    # Process the simulated API output
    process_api_output(example_api_output)