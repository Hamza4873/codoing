import pandas as pd
import json

def flatten_dict(d, parent_key='', sep='.'):
    """
    Fully flatten a nested dictionary, ensuring that all nested levels are flattened.
    Handles lists and JSON strings by recursively flattening them as well.
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
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        
        # Handle if value is a nested dictionary
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        
        # Handle if value is a list
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, dict):
                    # Flatten dictionaries inside lists
                    items.extend(flatten_dict(item, f"{new_key}[{i}]", sep=sep).items())
                else:
                    items.append((f"{new_key}[{i}]", item))
        
        # Handle if value is a JSON string (convert to dict if possible)
        elif isinstance(v, str):
            try:
                # Attempt to load the string as JSON and flatten if it's valid
                json_obj = json.loads(v)
                if isinstance(json_obj, dict):
                    items.extend(flatten_dict(json_obj, new_key, sep=sep).items())
                else:
                    items.append((new_key, v))
            except (json.JSONDecodeError, TypeError):
                # If it's not a valid JSON string, just append the value
                items.append((new_key, v))
        
        else:
            items.append((new_key, v))
    
    return dict(items)

def parse_nested_fields(api_response):
    """
    Parses the given API response and returns a DataFrame based on the user's choice of fields, 
    including fully flattened fields with all breadcrumb levels.
    
    Parameters:
    - api_response: A dictionary or list of dictionaries representing the API response.

    Returns:
    - A pandas DataFrame containing the selected fields.
    """
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
    all_fields = list(all_fields)
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
    including nested fields, into a DataFrame.

    Parameters:
    - api_output: A dictionary or list of dictionaries from the API.

    Returns:
    - None: Prints the DataFrame.
    """
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
    # Simulated API output containing nested objects and lists
    example_api_output = [
        {
            "file_hash": "123abc", 
            "detection_ratio": "20/60", 
            "scan_date": "2024-01-01",
            "metadata": {
                "scanners": [
                    {"name": "scanner1", "status": "clean"},
                    {"name": "scanner2", "status": "infected"}
                ],
                "size": 1024
            }
        },
        {
            "file_hash": "456def", 
            "detection_ratio": "5/60", 
            "scan_date": "2024-01-02",
            "metadata": {
                "scanners": [
                    {"name": "scanner1", "status": "clean"},
                    {"name": "scanner2", "status": "infected"}
                ],
                "size": 2048
            }
        }
    ]
    
    # Process the simulated API output
    process_api_output(example_api_output)