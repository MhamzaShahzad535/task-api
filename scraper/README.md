# Books to Scrape Pipeline

A small, polite web-scraping pipeline built for the FlyRank Backend Internship Track.

The scraper downloads the first three catalogue pages of Books to Scrape, discovers 60 unique books, visits each book page, extracts the data, normalizes and validates the records, stores the valid records as JSON, handles a deliberately broken page without crashing, and produces a run report.

---

## Target classification

### Target

Books to Scrape

Website:

https://books.toscrape.com/

Books to Scrape is a public sandbox website designed for practicing web scraping.

### Scope

The scraper processes only the first 3 catalogue pages.

These pages contain 60 unique books in total.

The scraper follows the catalogue's own `next` links instead of hardcoding individual book URLs.

### Data collected

Each book record contains:

- `title`
- `product_url`
- `price_text`
- `price_gbp`
- `availability_text`
- `rating_text`
- `description`
- `source_page`
- `fetched_at`

### Robots check

I checked:

https://books.toscrape.com/robots.txt

The request returned:

`404 Not Found`

Result:

`no robots file found`

A missing robots.txt file is not treated as permission to scrape other websites.

I will not reuse this code on another site without checking its rules and terms first.

---

## Technology

This project uses the Python lane.

- Python 3.10+
- Requests
- Beautiful Soup
- Pydantic
- JSON
- Git / GitHub

No database, paid proxy, cloud account, or browser is required.

---

## Project structure

```text
scraper/
│
├── src/
│   └── main.py
│
├── cache/
│   ├── catalogue-page-1.html
│   ├── catalogue-page-2.html
│   ├── catalogue-page-3.html
│   └── book-*.html
│
├── output/
│   ├── books.json
│   ├── errors.json
│   └── run-report.json
│
├── schemas.py
└── README.md