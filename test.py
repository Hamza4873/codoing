import requests

BASE_URL = "https://api.threatstream.com/api/v2"
API_KEY = "your_api_key_here"
HEADERS = {"X-Api-Key": API_KEY, "Content-Type": "application/json"}

def get_search_indicators_v2(indicator_type, value):
    """Search for indicators based on type and value."""
    url = f"{BASE_URL}/indicators/"
    params = {"indicator_type": indicator_type, "value": value}
    response = requests.get(url, params=params, headers=HEADERS)
    return response.json()

# Example: Search for indicators of type "ip" with value "1.2.3.4"
print(get_search_indicators_v2("ip", "1.2.3.4"))

def get_indicator_details_v2(indicator_id):
    """Get details of a specific indicator."""
    url = f"{BASE_URL}/indicators/{indicator_id}/"
    response = requests.get(url, headers=HEADERS)
    return response.json()

# Example: Get details of indicator with ID "123456"
print(get_indicator_details_v2("123456"))

def get_search_threats_v2(tags):
    """Search for threats based on tags."""
    url = f"{BASE_URL}/threats/"
    params = {"tags": tags}
    response = requests.get(url, params=params, headers=HEADERS)
    return response.json()

# Example: Search for threats with tags "malware"
print(get_search_threats_v2("malware"))

def get_threat_details_v2(threat_id):
    """Get details of a specific threat."""
    url = f"{BASE_URL}/threats/{threat_id}/"
    response = requests.get(url, headers=HEADERS)
    return response.json()

# Example: Get details of threat with ID "789012"
print(get_threat_details_v2("789012"))

def get_search_reports_v2(tags):
    """Search for reports based on tags."""
    url = f"{BASE_URL}/reports/"
    params = {"tags": tags}
    response = requests.get(url, params=params, headers=HEADERS)
    return response.json()

# Example: Search for reports with tags "phishing"
print(get_search_reports_v2("phishing"))

def get_report_details_v2(report_id):
    """Get details of a specific report."""
    url = f"{BASE_URL}/reports/{report_id}/"
    response = requests.get(url, headers=HEADERS)
    return response.json()

# Example: Get details of report with ID "345678"
print(get_report_details_v2("345678"))

def post_submit_indicator_v2(indicator, indicator_type, source):
    """Submit a new indicator."""
    url = f"{BASE_URL}/indicators/"
    data = {"indicator": indicator, "type": indicator_type, "source": source}
    response = requests.post(url, headers=HEADERS, json=data)
    return response.json()

# Example: Submit a new indicator
print(post_submit_indicator_v2("1.2.3.4", "ip", "your_source"))