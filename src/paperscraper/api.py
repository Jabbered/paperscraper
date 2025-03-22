"""OpenAlex API client for retrieving scholarly paper data.

This module provides functionality to interact with the OpenAlex API
and retrieve publication information.
"""
from typing import List
import requests
from datetime import datetime
import time
import random

from .models import Author, Paper


class OpenAlexClient:
    """Client for interacting with the OpenAlex API.

    This class handles all interactions with the OpenAlex API, including
    querying for papers and processing the responses.

    Attributes:
        base_url: The base URL for the OpenAlex API.
        headers: Headers to send with API requests.
        last_request_time: The timestamp of the last API request.
        min_request_interval: The minimum time between API requests in seconds.
    """

    def __init__(self, base_url: str = "https://api.openalex.org") -> None:
        """Initialize the OpenAlex client.

        Args:
            base_url: The base URL for the OpenAlex API.
        """
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Paperscraper/0.1.0 (mailto:jerome.paperscraper@gmail.com)"
        }
        self.last_request_time = 0
        self.min_request_interval = 0.5  # Minimum time between requests in seconds

    def _rate_limit(self):
        """Implement rate limiting between requests."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last_request
            time.sleep(sleep_time)
        self.last_request_time = time.time()

    def get_top_cited_papers(
        self, search_term: str, limit: int = 10, min_year: int | None = None
    ) -> List[Paper]:
        """Retrieve the top cited papers for a given search term.

        Args:
            search_term: The search term to find relevant papers.
            limit: Maximum number of papers to retrieve.
            min_year: Minimum publication year to include in results.

        Returns:
            List[Paper]: List of Paper objects containing the paper information.

        Raises:
            requests.RequestException: If the API request fails.
        """
        self._rate_limit()  # Implement rate limiting
        
        current_year = datetime.now().year
        params = {
            "search": search_term,
            "sort": "cited_by_count:desc",
            "per_page": limit,
            "select": "display_name,authorships,abstract_inverted_index,cited_by_count,publication_year,doi,primary_location",
            "mailto": "jerome.paperscraper@gmail.com"
        }

        # Add year filter if specified
        if min_year is not None:
            # Format the filter parameter according to OpenAlex API requirements
            params["filter"] = f"from_publication_date:{min_year}"
            print(f"Searching with year filter: {min_year} onwards")
            print(f"Filter parameter: {params['filter']}")

        try:
            response = requests.get(f"{self.base_url}/works", params=params, headers=self.headers)
            print(f"API URL: {response.url}")  # Debug information
            
            if response.status_code == 403:
                print("Received 403 error. Response content:", response.text)
                # Try without the filter parameter
                if "filter" in params:
                    print("Retrying without filter parameter...")
                    del params["filter"]
                    response = requests.get(f"{self.base_url}/works", params=params, headers=self.headers)
                    response.raise_for_status()
                else:
                    response.raise_for_status()
            else:
                response.raise_for_status()

            data = response.json()

            # Print total results count
            total_results = data.get("meta", {}).get("count", 0)
            print(f"Total results found: {total_results}")

            papers: List[Paper] = []
            for result in data.get("results", []):
                # Extract citation count and print debug info
                cited_by_count = result.get("cited_by_count", 0)
                title = result.get("display_name", "")
                pub_year = result.get("publication_year", 0)
                
                # Skip papers before min_year if filter was not applied
                if min_year is not None and pub_year < min_year:
                    continue
                    
                print(f"\nProcessing paper: {title}")
                print(f"Citation count: {cited_by_count}")
                print(f"Publication year: {pub_year}")

                # Get paper URL (prefer DOI, fallback to primary location)
                url = ""
                if result.get("doi"):
                    url = f"https://doi.org/{result['doi']}"
                elif result.get("primary_location", {}).get("landing_page_url"):
                    url = result["primary_location"]["landing_page_url"]
                print(f"Paper URL: {url}")

                authors = [
                    Author(
                        name=author.get("author", {}).get("display_name", ""),
                        affiliation=author.get("institutions", [{}])[0].get("display_name")
                        if author.get("institutions")
                        else None,
                    )
                    for author in result.get("authorships", [])
                ]

                # Convert abstract_inverted_index to text if available
                abstract = ""
                if "abstract_inverted_index" in result:
                    try:
                        # Simple conversion of inverted index to text
                        words = []
                        for word, positions in result["abstract_inverted_index"].items():
                            for pos in positions:
                                while len(words) <= pos:
                                    words.append("")
                                words[pos] = word
                        abstract = " ".join(words)
                    except Exception as e:
                        print(f"Error processing abstract: {e}")

                paper = Paper(
                    title=title,
                    authors=authors,
                    citation_count=cited_by_count,
                    publication_year=pub_year,
                    abstract=abstract,
                    url=url,
                    search_term=search_term  # Add search term to paper object
                )
                papers.append(paper)

            print(f"\nTotal papers processed: {len(papers)}")
            return papers

        except requests.exceptions.RequestException as e:
            print(f"API request failed: {str(e)}")
            if hasattr(e.response, 'text'):
                print(f"Response content: {e.response.text}")
            raise 