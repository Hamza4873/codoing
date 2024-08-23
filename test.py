import requests

class ShodanClient:
    def __init__(self, api_key):
        """
        Initialize the Shodan client with an API key.
        
        :param api_key: Shodan API key
        """
        self.api_key = api_key
        self.base_url = "https://api.shodan.io"

    def get_ip_report(self, ip_address):
        """
        Fetch information about a specific IP address.
        
        :param ip_address: The IP address to search for.
        """
        url = f"{self.base_url}/shodan/host/{ip_address}?key={self.api_key}"
        response = requests.get(url)
        return response.json()

    def get_domain_report(self, domain):
        """
        Get information about a specific domain from Shodan.
        
        :param domain: The domain to search for.
        """
        url = f"{self.base_url}/dns/domain/{domain}?key={self.api_key}"
        response = requests.get(url)
        return response.json()

    def get_search(self, query):
        """
        Perform a search on Shodan.
        
        :param query: Search query (e.g., 'apache', 'nginx', etc.).
        """
        url = f"{self.base_url}/shodan/host/search?key={self.api_key}&query={query}"
        response = requests.get(url)
        return response.json()

    def get_scan_report(self, scan_id):
        """
        Get the results of a Shodan scan.
        
        :param scan_id: The scan ID to retrieve results for.
        """
        url = f"{self.base_url}/shodan/scan/{scan_id}?key={self.api_key}"
        response = requests.get(url)
        return response.json()

class ThreatStreamClient:
    def __init__(self, api_username, api_key):
        """
        Initialize the ThreatStream client with an API username and API key.
        
        :param api_username: ThreatStream API username
        :param api_key: ThreatStream API key
        """
        self.api_username = api_username
        self.api_key = api_key
        self.base_url = "https://api.threatstream.com/api/v2"

    def get_ip_report(self, ip_address):
        """
        Fetch threat intelligence for a specific IP address.
        
        :param ip_address: The IP address to search for.
        """
        url = f"{self.base_url}/intelligence/?username={self.api_username}&api_key={self.api_key}&value={ip_address}&type=ip"
        response = requests.get(url)
        return response.json()

    def get_domain_report(self, domain):
        """
        Get threat intelligence for a specific domain from ThreatStream.
        
        :param domain: The domain to search for.
        """
        url = f"{self.base_url}/intelligence/?username={self.api_username}&api_key={self.api_key}&value={domain}&type=domain"
        response = requests.get(url)
        return response.json()

    def get_search(self, query):
        """
        Perform a search on ThreatStream for any indicator type (IP, domain, file hash).
        
        :param query: The search query to find any indicators of interest.
        """
        url = f"{self.base_url}/intelligence/?username={self.api_username}&api_key={self.api_key}&value={query}"
        response = requests.get(url)
        return response.json()

    def get_threat_report(self, report_id):
        """
        Fetch a specific threat report by its ID.
        
        :param report_id: The report ID to retrieve.
        """
        url = f"{self.base_url}/reports/{report_id}/?username={self.api_username}&api_key={self.api_key}"
        response = requests.get(url)
        return response.json()
