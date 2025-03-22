"""Tests for the OpenAlex API client.

This module contains tests for the OpenAlexClient class and its methods.
"""
from typing import TYPE_CHECKING
from unittest.mock import Mock, patch

import pytest
import requests

from paperscraper.api import OpenAlexClient
from paperscraper.models import Author, Paper

if TYPE_CHECKING:
    from _pytest.fixtures import FixtureRequest
    from pytest_mock import MockerFixture


@pytest.fixture
def mock_response() -> Mock:
    """Create a mock response for API calls.

    Returns:
        Mock: A mock response object.
    """
    mock = Mock()
    mock.json.return_value = {
        "results": [
            {
                "title": "Test Paper",
                "authorships": [
                    {
                        "author": {"display_name": "John Doe"},
                        "institutions": [{"display_name": "Test University"}],
                    }
                ],
                "abstract": "Test abstract",
                "cited_by_count": 100,
                "publication_year": 2023,
            }
        ]
    }
    return mock


@pytest.fixture
def client() -> OpenAlexClient:
    """Create an OpenAlexClient instance for testing.

    Returns:
        OpenAlexClient: A client instance for testing.
    """
    return OpenAlexClient()


def test_get_top_cited_papers(
    client: OpenAlexClient,
    mock_response: Mock,
    mocker: "MockerFixture",
) -> None:
    """Test retrieving top cited papers.

    Args:
        client: The OpenAlexClient instance.
        mock_response: Mock response object.
        mocker: Pytest mocker fixture.
    """
    mocker.patch("requests.get", return_value=mock_response)

    papers = client.get_top_cited_papers("test")

    assert len(papers) == 1
    paper = papers[0]
    assert paper.title == "Test Paper"
    assert paper.citation_count == 100
    assert paper.publication_year == 2023
    assert paper.abstract == "Test abstract"
    assert len(paper.authors) == 1
    assert paper.authors[0].name == "John Doe"
    assert paper.authors[0].affiliation == "Test University"


def test_get_top_cited_papers_api_error(
    client: OpenAlexClient,
    mocker: "MockerFixture",
) -> None:
    """Test handling of API errors.

    Args:
        client: The OpenAlexClient instance.
        mocker: Pytest mocker fixture.
    """
    mocker.patch(
        "requests.get",
        side_effect=requests.RequestException("API Error"),
    )

    with pytest.raises(requests.RequestException):
        client.get_top_cited_papers("test") 