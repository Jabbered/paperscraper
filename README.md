# Paperscraper

A web application for finding and analyzing academic papers using the OpenAlex API. Paperscraper helps researchers find the most cited papers on any topic, with support for multiple search terms and filtering by publication date.

## Features

- Search for academic papers using multiple search terms
- Find the most cited papers on any topic
- Filter results to show only recent papers (last 10 years)
- Export search results to CSV
- Beautiful and responsive web interface
- Rate-limited API calls to respect OpenAlex's terms of service

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/paperscraper.git
cd paperscraper
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -e .
```

## Usage

1. Start the web application:
```bash
python -m paperscraper
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Enter your search terms (one per line) and click "Search"

4. View the results and download them as CSV if desired

## Development

The project structure is organized as follows:

```
paperscraper/
├── src/
│   └── paperscraper/
│       ├── __init__.py
│       ├── api.py          # OpenAlex API client
│       ├── models.py       # Data models
│       ├── web.py          # Flask web application
│       ├── export.py       # CSV export functionality
│       └── templates/      # HTML templates
├── tests/                  # Test files
├── setup.py               # Package configuration
└── README.md             # This file
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 