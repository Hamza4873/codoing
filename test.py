import requests
import vt

# VirusTotal Client
class VirusTotalClient:
    def __init__(self, api_key):
        """Initialize the VirusTotal client with API key"""
        self.client = vt.Client(api_key)

    def get_file_report(self, file_hashes):
        """Fetch file reports from VirusTotal by file hashes."""
        return [self.client.get_object(f"/files/{file_hash}") for file_hash in file_hashes]

    def get_url_report(self, urls):
        """Fetch URL reports from VirusTotal."""
        return [self.client.get_object(f"/urls/{vt.url_id(url)}") for url in urls]

    def get_ip_report(self, ip_address):
        """Fetch an IP report from VirusTotal."""
        return self.client.get_object(f"/ip_addresses/{ip_address}")

    def get_domain_report(self, domain):
        """Fetch a domain report from VirusTotal."""
        return self.client.get_object(f"/domains/{domain}")

    def get_comments(self, resource_id):
        """Get comments on a file, URL, or IP."""
        return self.client.get(f"/comments/{resource_id}")

    def get_search(self, query):
        """
        Perform an intelligent search in VirusTotal.
        Examples of queries: 'domain:example.com', 'ip:8.8.8.8', 'file:123abc...'
        """
        search_results = []
        cursor = None
        while True:
            params = {"query": query}
            if cursor:
                params["cursor"] = cursor

            response = self.client.get("/intelligence/search", params=params)
            search_results.extend(response.get("data", []))

            cursor = response.get("meta", {}).get("cursor")
            if not cursor:
                break  # No more pages
        return search_results

# DomainTools Client
class DomainToolsClient:
    def __init__(self, api_key):
        """Initialize the DomainTools client with API key"""
        self.api_key = api_key
        self.base_url = "https://api.domaintools.com/v1"

    def get_domain_report(self, domains):
        """Fetch domain reports."""
        return [requests.get(f"{self.base_url}/{domain}/iris-investigate", auth=(self.api_key, '')).json() for domain in domains]

    def get_whois(self, domain):
        """Get WHOIS data for a domain."""
        url = f"{self.base_url}/{domain}/whois"
        response = requests.get(url, auth=(self.api_key, ''))
        return response.json()

    def get_pdns(self, domain):
        """Get Passive DNS data for a domain."""
        url = f"{self.base_url}/{domain}/pdns"
        response = requests.get(url, auth=(self.api_key, ''))
        return response.json()

    def get_risk(self, domain):
        """Fetch risk score for a domain."""
        url = f"{self.base_url}/{domain}/risk"
        response = requests.get(url, auth=(self.api_key, ''))
        return response.json()

    def get_associations(self, domain):
        """Fetch domain associations from DomainTools."""
        url = f"{self.base_url}/{domain}/associations"
        response = requests.get(url, auth=(self.api_key, ''))
        return response.json()

    def get_search(self, query):
        """
        Perform a search on DomainTools using the search endpoint.
        Example query: 'example.com', '8.8.8.8', etc.
        """
        search_url = f"{self.base_url}/search?q={query}"
        response = requests.get(search_url, auth=(self.api_key, ''))
        return response.json()

# UrlScan Client
class UrlScanClient:
    def __init__(self, api_key):
        """Initialize the urlscan.io client with API key"""
        self.api_key = api_key
        self.headers = {'API-Key': self.api_key}

    def get_scan_result(self, scan_ids):
        """Fetch scan results using scan IDs."""
        return [requests.get(f"https://urlscan.io/api/v1/result/{scan_id}/", headers=self.headers).json() for scan_id in scan_ids]

    def get_ip_result(self, ip_address):
        """Fetch information on an IP address."""
        result_url = f"https://urlscan.io/api/v1/search/?q=ip:{ip_address}"
        response = requests.get(result_url, headers=self.headers)
        return response.json()

    def get_domain_result(self, domains):
        """Fetch domain information from urlscan.io."""
        return [requests.get(f"https://urlscan.io/api/v1/search/?q=domain:{domain}", headers=self.headers).json() for domain in domains]

    def get_search(self, query):
        """
        Perform a search on Urlscan with a size of 10,000.
        Example query: 'domain:example.com', 'ip:8.8.8.8', etc.
        """
        search_url = f"https://urlscan.io/api/v1/search/?q={query}&size=10000"
        response = requests.get(search_url, headers=self.headers)
        return response.json()