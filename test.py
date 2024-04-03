import requests

class ThreatStreamClient:
    def __init__(self, api_key):
        self.base_url = 'https://api.threatstream.com/api/v2/'
        self.headers = {'Authorization': f'apikey {api_key}'}

    def get_intelligence(self, params=None):
        """Get a list of observables."""
        url = self.base_url + 'intelligence/'
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def get_confidence(self, type, value):
        """Get confidence scores for an observable."""
        url = self.base_url + 'inteldetails/confidence_trend/'
        params = {'type': type, 'value': value}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def get_rules(self, params=None):
        """Get a list of rules."""
        url = self.base_url + 'rule/'
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def search_sandbox(self, query):
        """Search for sandbox submissions."""
        url = self.base_url + 'submit/search/'
        params = {'q': query}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def search_threat_model(self, model_type, params=None):
        """Search for threat model entities."""
        url = self.base_url + 'threat_model_search/'
        params = params or {}
        params['model_type'] = model_type
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

# Example usage
api_key = 'your_api_key'
client = ThreatStreamClient(api_key)

# Get a list of observables
observables = client.get_intelligence()
print(observables)

# Get confidence scores for an observable
confidence_scores = client.get_confidence(type='ip', value='8.8.8.8')
print(confidence_scores)

# Get a list of rules
rules = client.get_rules()
print(rules)

# Search for sandbox submissions
sandbox_results = client.search_sandbox(query='malware')
print(sandbox_results)

# Search for threat model entities (e.g., actors)
threat_model_results = client.search_threat_model(model_type='actor')
print(threat_model_results)