import functools
import os
from typing import List

import requests
from requests import Response

import synapse_wiki as sw

API_BASE_URL = "https://api.synapse.wiki/v0/api"


def ensure_200_response(func):
    # we need functools.wraps here to
    # 1. preserve the function name -- otherwise it will be "wrapper"
    # 2. preserve the function signature -- otherwise it will be (*args, **kwargs)
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        if response.status_code != 200:
            raise Exception(
                f"Request failed with status code {response.status_code}. Message: {response.text}"
            )
        return response

    return wrapper


class AuthenticationError(ValueError):
    """Exception raised for authentication failures."""

    def __init__(self, message="Authentication failed"):
        self.message = message
        super().__init__(self.message)


def default_api_key() -> str:
    if sw.api_key is not None:
        return sw.api_key
    elif os.environ.get("SYNAPSE_API_KEY") is not None:
        return os.environ.get("SYNAPSE_API_KEY")
    else:
        raise AuthenticationError(
            "No API key provided. You can set your API key in code using 'sw.api_key = <API-KEY>', or you can set the environment variable SYNAPSE_API_KEY=<API-KEY>)."
        )


def request_headers(api_key: str) -> str:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


@ensure_200_response
def create_collection(collection_name: str):
    api_key = default_api_key()
    headers = request_headers(api_key)

    response = requests.post(
        f"{API_BASE_URL}/create_collection",
        headers=headers,
        json={"collection": collection_name},
    )

    return response.json()


@ensure_200_response
def list_collections():
    api_key = default_api_key()
    headers = request_headers(api_key)

    response = requests.get(
        f"{API_BASE_URL}/list_collections",
        headers=headers,
        json={
            "verbose": False,
        },
    )
    if response.status_code != 200:
        raise Exception(
            f"Request failed with status code {response.status_code}. Message: {response.text}"
        )

    return response.json()


@ensure_200_response
def query(collection_name: str, query_string: str, max_results: int = 5) -> Response:
    api_key = default_api_key()
    headers = request_headers(api_key)

    if 1 > max_results or max_results > 20:
        raise Exception(
            f"'max_results' must be between 1 and 20. Currently set to {max_results}"
        )

    return requests.post(
        f"{API_BASE_URL}/query",
        headers=headers,
        json={
            "collections": [collection_name],
            "query": query_string,
            "max_results": max_results,
        },
    )


def ingest(collection_name: str, urls: List[str]) -> Response:
    api_key = default_api_key()
    headers = request_headers(api_key)
    response = requests.post(
        f"{API_BASE_URL}/ingest",
        headers=headers,
        json={"urls": urls, "collection": collection_name},
    )
    return response
