"""Tests for the export functionality.

This module contains tests for exporting paper data to CSV files.
"""
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import pandas as pd
import pytest

from paperscraper.export import export_papers_to_csv
from paperscraper.models import Author, Paper

if TYPE_CHECKING:
    from _pytest.fixtures import FixtureRequest
    from pytest_mock import MockerFixture


@pytest.fixture
def sample_papers() -> list[Paper]:
    """Create sample papers for testing.

    Returns:
        list[Paper]: List of sample Paper objects.
    """
    return [
        Paper(
            title="Test Paper 1",
            authors=[Author(name="John Doe", affiliation="University 1")],
            citation_count=100,
            publication_year=2023,
            abstract="Test abstract 1",
        ),
        Paper(
            title="Test Paper 2",
            authors=[Author(name="Jane Smith", affiliation="University 2")],
            citation_count=50,
            publication_year=2022,
            abstract="Test abstract 2",
        ),
    ]


def test_export_papers_to_csv(
    sample_papers: list[Paper],
    tmp_path: Path,
    mocker: "MockerFixture",
) -> None:
    """Test exporting papers to CSV.

    Args:
        sample_papers: List of sample Paper objects.
        tmp_path: Temporary directory path.
        mocker: Pytest mocker fixture.
    """
    # Mock the current date
    mock_date = datetime(2024, 1, 1)
    mocker.patch("paperscraper.export.datetime", now=lambda: mock_date)

    # Change to temporary directory
    with pytest.MonkeyPatch.context() as mp:
        mp.chdir(tmp_path)
        output_file = export_papers_to_csv(sample_papers, "test")

    # Verify output file exists
    assert Path(output_file).exists()

    # Read the CSV file
    df = pd.read_csv(output_file)

    # Verify the data
    assert len(df) == 2
    assert list(df.columns) == [
        "Title",
        "Authors",
        "Citation Count",
        "Publication Year",
        "Abstract",
        "AI Summary",
        "Main Findings",
    ]
    assert df["Title"].tolist() == ["Test Paper 1", "Test Paper 2"]
    assert df["Citation Count"].tolist() == [100, 50]
    assert df["Publication Year"].tolist() == [2023, 2022]
    assert df["Authors"].tolist() == ["John Doe", "Jane Smith"]
    assert df["Abstract"].tolist() == ["Test abstract 1", "Test abstract 2"]
    assert df["AI Summary"].tolist() == ["", ""]
    assert df["Main Findings"].tolist() == ["", ""] 