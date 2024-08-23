import os
import requests

DATABRICKS_INSTANCE = "https://<databricks-instance>.cloud.databricks.com"
DATABRICKS_TOKEN = "<your-databricks-token>"

headers = {
    "Authorization": f"Bearer {DATABRICKS_TOKEN}"
}

def list_workspace_files(workspace_path):
    url = f"{DATABRICKS_INSTANCE}/api/2.0/workspace/list"
    response = requests.get(url, headers=headers, params={"path": workspace_path})
    
    if response.status_code == 200:
        return response.json().get("objects", [])
    else:
        raise Exception(f"Failed to list workspace files: {response.text}")

def export_file_from_databricks(workspace_file_path, local_file_path, file_format):
    url = f"{DATABRICKS_INSTANCE}/api/2.0/workspace/export"
    params = {
        "path": workspace_file_path,
        "format": file_format
    }
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        with open(local_file_path, "wb") as f:
            f.write(response.content)
        print(f"Exported {workspace_file_path} to {local_file_path}")
    else:
        raise Exception(f"Failed to export file: {response.text}")

def process_files(workspace_dir, local_dir):
    os.makedirs(local_dir, exist_ok=True)
    
    files = list_workspace_files(workspace_dir)
    for file in files:
        workspace_file_path = file["path"]
        file_type = file["object_type"]
        local_file_path = os.path.join(local_dir, os.path.basename(workspace_file_path))

        if file_type == "DIRECTORY":
            print(f"Processing directory: {workspace_file_path}")
            process_files(workspace_file_path, local_file_path)
        elif file_type == "NOTEBOOK":
            if workspace_file_path.endswith(".ipynb"):
                export_file_from_databricks(workspace_file_path, local_file_path + ".ipynb", "JUPYTER")
            elif workspace_file_path.endswith(".py"):
                export_file_from_databricks(workspace_file_path, local_file_path + ".py", "SOURCE")
            elif workspace_file_path.endswith(".yaml") or workspace_file_path.endswith(".yml"):
                export_file_from_databricks(workspace_file_path, local_file_path + ".yaml", "SOURCE")
            else:
                print(f"Skipping non-Python, non-Jupyter, and non-YAML file: {workspace_file_path}")
        else:
            print(f"Skipping unknown file type: {workspace_file_path}")

if __name__ == "__main__":
    workspace_directory = "/Workspace/Users/your-email"
    local_directory = "/path/to/local/directory"
    
    try:
        process_files(workspace_directory, local_directory)
        print("Export complete.")
    except Exception as e:
        print(f"Error during export: {e}")