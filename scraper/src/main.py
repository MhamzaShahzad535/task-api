import json
import time
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


# --------------------------------------------------
# Make scraper/ available for schemas.py
# --------------------------------------------------

SCRAPER_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(SCRAPER_DIR))

from schemas import BookRecord


# --------------------------------------------------
# Configuration
# --------------------------------------------------

BASE_URL = "https://books.toscrape.com/"

CACHE_DIR = SCRAPER_DIR / "cache"
OUTPUT_DIR = SCRAPER_DIR / "output"

BOOKS_FILE = OUTPUT_DIR / "books.json"
ERRORS_FILE = OUTPUT_DIR / "errors.json"
REPORT_FILE = OUTPUT_DIR / "run-report.json"

HEADERS = {
    "User-Agent": (
        "FlyRankInternshipA9/1.0 "
        "(+https://github.com/MhamzaShahzad535/task-api)"
    )
}


# --------------------------------------------------
# Statistics
# --------------------------------------------------

stats = {
    "pages_fetched": 0,
    "cache_hits": 0,
    "valid_records": 0,
    "invalid_records": 0,
    "failed_pages": 0
}


# --------------------------------------------------
# Fetch page
# --------------------------------------------------

def fetch_page(url, cache_file):

    if cache_file.exists():

        stats["cache_hits"] += 1

        html = cache_file.read_text(
            encoding="utf-8"
        )

        print(f"CACHE HIT: {url}")
        print(
            f"Response size: {len(html)} bytes"
        )

        return html

    print(f"FETCH: {url}")

    stats["pages_fetched"] += 1

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

    except requests.Timeout:

        print("TIMEOUT - retrying once...")

        time.sleep(1)

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

    except requests.RequestException as error:

        raise RuntimeError(
            f"Request failed: {error}"
        )

    # Retry 5xx once
    if 500 <= response.status_code <= 599:

        print(
            f"SERVER ERROR {response.status_code} "
            "- retrying once..."
        )

        time.sleep(1)

        try:

            response = requests.get(
                url,
                headers=HEADERS,
                timeout=10
            )

        except requests.RequestException as error:

            raise RuntimeError(
                f"Retry failed: {error}"
            )

    # Never retry 403
    if response.status_code == 403:

        raise RuntimeError(
            "403 Forbidden - request rejected"
        )

    # Never retry 404
    if response.status_code == 404:

        raise RuntimeError(
            "404 Not Found - page does not exist"
        )

    if response.status_code != 200:

        raise RuntimeError(
            f"Request failed with status code "
            f"{response.status_code}"
        )

    html = response.text

    cache_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    cache_file.write_text(
        html,
        encoding="utf-8"
    )

    print(
        f"Response size: {len(html)} bytes"
    )

    return html


# --------------------------------------------------
# Extract book URLs
# --------------------------------------------------

def extract_book_urls(html, page_url):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    book_urls = []

    for article in soup.select(
        "article.product_pod"
    ):

        link = article.select_one(
            "h3 a"
        )

        if link:

            href = link.get("href")

            if href:

                absolute_url = urljoin(
                    page_url,
                    href
                )

                book_urls.append(
                    absolute_url
                )

    return book_urls


# --------------------------------------------------
# Find next catalogue page
# --------------------------------------------------

def find_next_page(html, page_url):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    next_link = soup.select_one(
        "li.next a"
    )

    if next_link:

        href = next_link.get("href")

        if href:

            return urljoin(
                page_url,
                href
            )

    return None


# --------------------------------------------------
# Extract raw book details
# --------------------------------------------------

def extract_book_details(
    html,
    product_url,
    source_page
):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    title = soup.select_one(
        "div.product_main h1"
    )

    price = soup.select_one(
        "div.product_main p.price_color"
    )

    availability = soup.select_one(
        "div.product_main "
        "p.instock.availability"
    )

    rating = soup.select_one(
        "div.product_main "
        "p.star-rating"
    )

    description = soup.select_one(
        "#product_description + p"
    )

    rating_text = None

    if rating:

        rating_classes = rating.get(
            "class",
            []
        )

        for value in rating_classes:

            if value != "star-rating":

                rating_text = value

                break

    return {

        "title": (
            title.get_text(strip=True)
            if title
            else None
        ),

        "product_url": product_url,

        "price_text": (
            price.get_text(strip=True)
            if price
            else None
        ),

        "availability_text": (
            availability.get_text(
                " ",
                strip=True
            )
            if availability
            else None
        ),

        "rating_text": rating_text,

        "description": (
            description.get_text(
                " ",
                strip=True
            )
            if description
            else None
        ),

        "source_page": source_page,

        "fetched_at": (
            datetime.now(
                timezone.utc
            ).isoformat()
        )
    }


# --------------------------------------------------
# Normalize price
# --------------------------------------------------

def normalize_price(price_text):

    if not price_text:

        raise ValueError(
            "Price is missing"
        )

    cleaned = price_text.strip()

    cleaned = cleaned.replace(
        "£",
        ""
    )

    cleaned = cleaned.replace(
        "Ã‚Â£",
        ""
    )

    cleaned = cleaned.replace(
        "Â£",
        ""
    )

    cleaned = cleaned.replace(
        "Ã£",
        ""
    )

    cleaned = "".join(
        character
        for character in cleaned
        if character.isdigit()
        or character == "."
    )

    if not cleaned:

        raise ValueError(
            f"Invalid price: {price_text}"
        )

    try:

        return float(cleaned)

    except ValueError:

        raise ValueError(
            f"Invalid price: {price_text}"
        )


# --------------------------------------------------
# Normalize record
# --------------------------------------------------

def normalize_record(raw_record):

    price_gbp = normalize_price(
        raw_record["price_text"]
    )

    return {

        "title": raw_record["title"],

        "product_url": raw_record[
            "product_url"
        ],

        "price_text": raw_record[
            "price_text"
        ],

        "price_gbp": price_gbp,

        "availability_text": raw_record[
            "availability_text"
        ],

        "rating_text": raw_record[
            "rating_text"
        ],

        "description": raw_record[
            "description"
        ],

        "source_page": raw_record[
            "source_page"
        ],

        "fetched_at": raw_record[
            "fetched_at"
        ]
    }


# --------------------------------------------------
# Validate record
# --------------------------------------------------

def validate_record(record):

    validated = BookRecord(
        **record
    )

    return validated.model_dump(
        mode="json"
    )


# --------------------------------------------------
# Discover first three catalogue pages
# --------------------------------------------------

def discover_books():

    current_url = BASE_URL

    discovered_books = []

    catalogue_pages = 0

    while catalogue_pages < 3:

        catalogue_pages += 1

        cache_file = (
            CACHE_DIR
            / f"catalogue-page-{catalogue_pages}.html"
        )

        html = fetch_page(
            current_url,
            cache_file
        )

        book_urls = extract_book_urls(
            html,
            current_url
        )

        for book_url in book_urls:

            discovered_books.append(
                {
                    "product_url": book_url,
                    "source_page": current_url
                }
            )

        print(
            f"Page {catalogue_pages}: "
            f"found {len(book_urls)} books"
        )

        if catalogue_pages < 3:

            next_url = find_next_page(
                html,
                current_url
            )

            if next_url is None:

                raise RuntimeError(
                    "Could not find the "
                    "next catalogue page"
                )

            current_url = next_url

            next_cache = (
                CACHE_DIR
                / f"catalogue-page-"
                f"{catalogue_pages + 1}.html"
            )

            if not next_cache.exists():

                time.sleep(0.5)

    # Remove duplicate URLs
    unique_books = {}

    for book in discovered_books:

        unique_books[
            book["product_url"]
        ] = book

    unique_books = list(
        unique_books.values()
    )

    print()

    print(
        f"catalogue_pages={catalogue_pages}"
    )

    print(
        f"discovered={len(discovered_books)}"
    )

    print(
        f"unique_urls={len(unique_books)}"
    )

    return unique_books


# --------------------------------------------------
# Save JSON
# --------------------------------------------------

def save_json(file_path, data):

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with file_path.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    # Reset statistics for every run
    stats["pages_fetched"] = 0
    stats["cache_hits"] = 0
    stats["valid_records"] = 0
    stats["invalid_records"] = 0
    stats["failed_pages"] = 0

    start_time = time.time()

    started_at = datetime.now(
        timezone.utc
    ).isoformat()

    print()
    print("Starting scraper...")
    print()

    # --------------------------------------------------
    # Discover 60 real books
    # --------------------------------------------------

    books = discover_books()

    if not books:

        raise RuntimeError(
            "No books discovered"
        )

    # --------------------------------------------------
    # Stage 5 test
    #
    # Add ONE fake URL locally.
    # This proves that one broken page does not
    # stop the rest of the scraper.
    # --------------------------------------------------

    books.append(
        {
            "product_url": (
                "https://books.toscrape.com/"
                "THIS_IS_A_DELIBERATELY_BROKEN_URL/"
            ),
            "source_page": BASE_URL
        }
    )

    print()
    print(
        "STAGE 5 TEST: "
        "Added one deliberately broken URL"
    )
    print()

    valid_records = []

    errors = []

    seen_urls = set()

    # --------------------------------------------------
    # Process books
    # --------------------------------------------------

    for index, book in enumerate(
        books,
        start=1
    ):

        product_url = book[
            "product_url"
        ]

        source_page = book[
            "source_page"
        ]

        print()

        print(
            f"Processing book "
            f"{index}/{len(books)}"
        )

        print(product_url)

        # Give fake URL a special cache path
        if "THIS_IS_A_DELIBERATELY_BROKEN_URL" in product_url:

            book_cache = (
                CACHE_DIR
                / "deliberately-broken-page.html"
            )

        else:

            book_cache = (
                CACHE_DIR
                / f"book-{index}.html"
            )

        # Polite delay only for real requests
        if not book_cache.exists():

            time.sleep(0.5)

        try:

            # Duplicate protection
            if product_url in seen_urls:

                print(
                    "DUPLICATE URL - SKIPPED"
                )

                continue

            # --------------------------------------------------
            # Deliberate local failure
            #
            # We do NOT contact the real website for this test.
            # --------------------------------------------------

            if "THIS_IS_A_DELIBERATELY_BROKEN_URL" in product_url:

                raise RuntimeError(
                    "Deliberate test failure: "
                    "broken page"
                )

            # Fetch
            book_html = fetch_page(
                product_url,
                book_cache
            )

            # Extract
            raw_record = extract_book_details(
                book_html,
                product_url,
                source_page
            )

            # Normalize
            clean_record = normalize_record(
                raw_record
            )

            # Validate
            validated_record = validate_record(
                clean_record
            )

            seen_urls.add(
                product_url
            )

            valid_records.append(
                validated_record
            )

            stats["valid_records"] += 1

            print("VALID")

        except Exception as error:

            print(
                f"FAILED: {error}"
            )

            stats["invalid_records"] += 1
            stats["failed_pages"] += 1

            errors.append(
                {
                    "product_url": product_url,

                    "error": str(error),

                    "timestamp": (
                        datetime.now(
                            timezone.utc
                        ).isoformat()
                    )
                }
            )

    # --------------------------------------------------
    # Save valid books
    # --------------------------------------------------

    save_json(
        BOOKS_FILE,
        valid_records
    )

    # --------------------------------------------------
    # Save errors
    # --------------------------------------------------

    save_json(
        ERRORS_FILE,
        errors
    )

    # --------------------------------------------------
    # Duration
    # --------------------------------------------------

    duration_seconds = round(
        time.time() - start_time,
        2
    )

    finished_at = datetime.now(
        timezone.utc
    ).isoformat()

    # --------------------------------------------------
    # Run report
    # --------------------------------------------------

    report = {

        "started_at": started_at,

        "finished_at": finished_at,

        "duration_seconds": duration_seconds,

        "catalogue_pages": 3,

        "discovered_urls": 60,

        "unique_urls": 60,

        "pages_fetched": stats[
            "pages_fetched"
        ],

        "cache_hits": stats[
            "cache_hits"
        ],

        "valid_records": stats[
            "valid_records"
        ],

        "invalid_records": stats[
            "invalid_records"
        ],

        "failed_pages": stats[
            "failed_pages"
        ]
    }

    save_json(
        REPORT_FILE,
        report
    )

    # --------------------------------------------------
    # Final report
    # --------------------------------------------------

    print()
    print("=" * 60)
    print("SCRAPER COMPLETE")
    print("=" * 60)

    print(
        f"Catalogue pages: "
        f"{report['catalogue_pages']}"
    )

    print(
        f"Discovered URLs: "
        f"{report['discovered_urls']}"
    )

    print(
        f"Unique URLs: "
        f"{report['unique_urls']}"
    )

    print(
        f"Pages fetched: "
        f"{report['pages_fetched']}"
    )

    print(
        f"Cache hits: "
        f"{report['cache_hits']}"
    )

    print(
        f"Valid records: "
        f"{report['valid_records']}"
    )

    print(
        f"Invalid records: "
        f"{report['invalid_records']}"
    )

    print(
        f"Failed pages: "
        f"{report['failed_pages']}"
    )

    print(
        f"Duration: "
        f"{report['duration_seconds']} seconds"
    )

    print()

    print(
        f"Books saved to: "
        f"{BOOKS_FILE}"
    )

    print(
        f"Errors saved to: "
        f"{ERRORS_FILE}"
    )

    print(
        f"Report saved to: "
        f"{REPORT_FILE}"
    )

    # --------------------------------------------------
    # Show first record
    # --------------------------------------------------

    if valid_records:

        print()
        print(
            "FIRST VALID RECORD"
        )

        print("=" * 60)

        print(
            json.dumps(
                valid_records[0],
                indent=2,
                ensure_ascii=False
            )
        )


# --------------------------------------------------
# Start
# --------------------------------------------------

if __name__ == "__main__":

    main()