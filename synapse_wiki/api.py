from dataclasses import dataclass
from typing import List

import server_requests


@dataclass
class Result:
    text: str
    url: str
    page_title: str
    relevance_score: float

    def __str__(self):
        if len(self.text) > 50:
            shortened_text = self.text[:50] + "..."
        else:
            shortened_text = self.text
        return f"""
Result(
    url: {self.url}
    page_title: {self.page_title}
    relevance_score: {self.relevance_score}
    text: {shortened_text}
)
"""


class QueryResponse:
    def __init__(self, results: List[Result]):
        self.results = results

    def __iter__(self):
        return iter(self.results)

    def __len__(self):
        return len(self.results)

    def __str__(self):
        return f"QueryResponse({self.__len__()} results)"


@dataclass
class IngestionResponse:
    collection_name: str
    total_urls: int
    num_urls_ingested: int
    num_urls_failed: int


def query(
    collection_name: str, query_string: str, max_results: int = 5
) -> QueryResponse:
    response = server_requests.query(collection_name, query_string, max_results)

    results_dict = response.json()["results"]
    results = [
        Result(
            text=r["text"],
            url=r["url"],
            page_title=r["page_title"],
            relevance_score=r["relevance_score"],
        )
        for r in results_dict
    ]
    return QueryResponse(results=results)


def ingest(collection_name: str, urls: List[str]) -> IngestionResponse:
    response = server_requests.ingest(collection_name, urls)
    resp_json = response.json()
    return IngestionResponse(
        collection_name=resp_json["collection_name"],
        total_urls=resp_json["total_urls"],
        num_urls_ingested=resp_json["num_urls_ingested"],
        num_urls_failed=resp_json["num_urls_failed"],
    )
