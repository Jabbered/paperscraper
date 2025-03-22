"""Module for exporting paper data to CSV files.

This module handles the export of paper data to CSV files with proper
naming conventions and formatting.
"""
from datetime import datetime
from pathlib import Path
from typing import List

import pandas as pd

from .models import Paper


def export_papers_to_csv(papers: List[Paper], search_term: str) -> str:
    """Export papers to a CSV file with timestamp in the filename.

    Args:
        papers: List of Paper objects to export.
        search_term: The search term used to find the papers.

    Returns:
        str: Path to the created CSV file.

    Raises:
        IOError: If there's an error writing the CSV file.
    """
    # Create output directory if it doesn't exist
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d")
    filename = f"{search_term}_top10_{timestamp}.csv"
    filepath = output_dir / filename

    # Convert papers to DataFrame
    df = pd.DataFrame([paper.to_dict() for paper in papers])

    # Export to CSV
    df.to_csv(filepath, index=False, encoding="utf-8")

    return str(filepath) 