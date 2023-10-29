import requests
import synapse_wiki as sw
import typing


API_BASE_URL = "https://api.synapse.wiki/v0/api"

class AuthenticationError(ValueError):
    """Exception raised for authentication failures."""

    def __init__(self, message="Authentication failed"):
        self.message = message
        super().__init__(self.message)

def default_api_key() -> str:
    if sw.api_key is not None:
        return sw.api_key
    else:
        raise AuthenticationError(
            "No API key provided. You can set your API key in code using 'sw.api_key = <API-KEY>', or you can set the environment variable SYNAPSE_API_KEY=<API-KEY>)."
        )
    
def request_headers(api_key: str) -> str:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

def create_collection(collection_name: str):
    api_key = default_api_key()
    headers = request_headers(api_key)
    
    response = requests.post(f"{API_BASE_URL}/create_collection", headers=headers, json={"collection": collection_name})
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}. Message: {response.text}")
    
    return response.json()

def list_collections():
    api_key = default_api_key()
    headers = request_headers(api_key)
    
    response = requests.get(f"{API_BASE_URL}/list_collections", headers=headers)
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}. Message: {response.text}")
    
    return response.json()
    
def fetch(collection_name: str, query: str, max_results: int = 5):
    api_key = default_api_key()
    headers = request_headers(api_key)

    if 1 > max_results or max_results > 20:
        raise Exception(f"\'max_results\' must be between 1 and 20. Currently set to {max_results}")
    
    response = requests.post(
        f"{API_BASE_URL}/fetch", 
        headers=headers, 
        json={
            "collections": [collection_name],
            "query": query,
            "max_results": max_results,
        }
    )

    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}. Message: {response.text}")
    
    return response.json()

    




