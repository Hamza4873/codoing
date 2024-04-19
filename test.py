import requests

class DomainToolsClient:
    def __init__(self, username, api_key):
        self.base_url = "https://api.domaintools.com"
        self.username = username
        self.api_key = api_key

    def whois_lookup(self, domain):
        """Perform a WHOIS lookup for a given domain."""
        url = f"{self.base_url}/v1/{domain}/whois"
        params = {'api_username': self.username, 'api_key': self.api_key}
        return self._make_request(url, params)

    def reverse_whois(self, query):
        """Perform a reverse WHOIS lookup based on search terms."""
        url = f"{self.base_url}/v1/reverse-whois"
        params = {'query': query, 'api_username': self.username, 'api_key': self.api_key}
        return self._make_request(url, params)

    def reverse_ip(self, ip):
        """Find all domains hosted on a specific IP address."""
        url = f"{self.base_url}/v1/{ip}/reverse-ip"
        params = {'api_username': self.username, 'api_key': self.api_key}
        return self._make_request(url, params)

    def phisheye(self, term, days):
        """Monitor for domain names that mimic brand-related terms."""
        url = f"{self.base_url}/v1/phisheye"
        params = {'term': term, 'days': days, 'api_username': self.username, 'api_key': self.api_key}
        return self._make_request(url, params)

    def domain_profile(self, domain):
        """Get detailed profile information for a domain."""
        url = f"{self.base_url}/v1/{domain}/profile"
        params = {'api_username': self.username, 'api_key': self.api_key}
        return self._make_request(url, params)

    def hosting_history(self, domain):
        """Get hosting history for a domain."""
        url = f"{self.base_url}/v1/{domain}/hosting-history"
        params = {'api_username': self.username, 'api_key': self.api_key}
        return self._make_request(url, params)

    def brand_monitor(self, brand):
        """Monitor new domain registrations that are similar to the brand."""
        url = f"{self.base_url}/v1/brand-monitor"
        params = {'brand': brand, 'api_username': self.username, 'api_key': self.api_key}
        return self._make_request(url, params)

    def domain_risk_score(self, domain):
        """Get risk score assessment for a domain."""
        url = f"{self.base_url}/v1/{domain}/risk-score"
        params = {'api_username': self.username, 'api_key': self.api_key}
        return self._make_request(url, params)

    def _make_request(self, url, params):
        """Helper method to make API requests."""
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return response.status_code, response.text

# Usage example
username = 'your_username'
api_key = 'your_api_key'
client = DomainToolsClient(username, api_key)

# Example calls to new methods
print(client.domain_profile("example.com"))
print(client.hosting_history("example.com"))
print(client.brand_monitor("examplebrand"))
print(client.domain_risk_score("example.com"))