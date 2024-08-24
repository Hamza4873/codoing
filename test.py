def create_group(group_name):
    url = f"{DATABRICKS_INSTANCE}/api/2.0/groups/create"
    headers = {"Authorization": f"Bearer {DATABRICKS_TOKEN}"}
    payload = {"group_name": group_name}
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()