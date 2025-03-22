"""Data models for paper information.

This module contains the data structures used to represent paper information
retrieved from the OpenAlex API.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class Author:
    """Represents an author of a paper.

    Attributes:
        name: The full name of the author.
        affiliation: The author's institutional affiliation.
    """
    name: str
    affiliation: str | None = None


@dataclass
class Paper:
    """Represents a scholarly paper with its metadata.

    Attributes:
        title: The complete title of the publication.
        authors: List of authors who contributed to the paper.
        citation_count: Total number of citations received.
        publication_year: Year when the paper was published.
        abstract: The paper's abstract text.
        url: URL to access the paper.
        search_term: The search term that found this paper.
        ai_summary: Placeholder for AI-generated summary (empty by default).
        main_findings: Placeholder for AI-generated main findings (empty by default).
    """
    title: str
    authors: List[Author]
    citation_count: int
    publication_year: int
    abstract: str
    url: str = ""
    search_term: str = ""
    ai_summary: str = ""
    main_findings: str = ""

    def to_dict(self) -> dict:
        """Convert the paper to a dictionary format suitable for CSV export.

        Returns:
            dict: Dictionary representation of the paper.
        """
        return {
            "Title": self.title,
            "Authors": ", ".join(author.name for author in self.authors),
            "Citation Count": self.citation_count,
            "Publication Year": self.publication_year,
            "URL": self.url,
            "Search Term": self.search_term,
            "Abstract": self.abstract,
            "AI Summary": self.ai_summary,
            "Main Findings": self.main_findings,
        } 