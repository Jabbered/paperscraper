"""Main entry point for the paperscraper script.

This module provides the command-line interface for the paperscraper tool,
allowing users to search for papers and export them to CSV.
"""
import argparse
import logging
from typing import NoReturn

from .api import OpenAlexClient
from .export import export_papers_to_csv


def setup_logging() -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def parse_args() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Retrieve top cited papers from OpenAlex API"
    )
    parser.add_argument(
        "search_term",
        help="Search term to find relevant papers",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of papers to retrieve (default: 10)",
    )
    return parser.parse_args()


def main() -> NoReturn:
    """Main entry point for the paperscraper script."""
    setup_logging()
    logger = logging.getLogger(__name__)
    args = parse_args()

    try:
        # Initialize API client
        client = OpenAlexClient()

        # Fetch papers
        logger.info(f"Fetching papers for search term: {args.search_term}")
        papers = client.get_top_cited_papers(args.search_term, args.limit)

        # Export to CSV
        output_file = export_papers_to_csv(papers, args.search_term)
        logger.info(f"Successfully exported {len(papers)} papers to {output_file}")

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise


if __name__ == "__main__":
    main() 