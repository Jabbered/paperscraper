"""Script to run paper search directly."""
from paperscraper.api import OpenAlexClient
from paperscraper.export import export_papers_to_csv

def main():
    """Run the paper search."""
    search_term = "machine learning"
    client = OpenAlexClient()
    papers = client.get_top_cited_papers(search_term)
    output_file = export_papers_to_csv(papers, search_term)
    print(f"Papers exported to: {output_file}")

if __name__ == "__main__":
    main() 