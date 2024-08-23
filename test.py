# From this:
response = requests.get(url, headers=headers, params=params)

# To this:
file_content = response.json().get("content")
if file_content:
    decoded_content = base64.b64decode(file_content)
    with open(local_file_path, "wb") as f:
        f.write(decoded_content)
    print(f"Exported {workspace_file_path} to {local_file_path}")
else:
    raise Exception(f"No content found for {workspace_file_path}")