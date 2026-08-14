import requests
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time


BASE_URL = "https://books.toscrape.com/"
CACHE_DIR = Path("cache")

HEADERS = {
    "User-Agent": "FlyRankInternshipA9/1.0 (+https://github.com/MhamzaShahzad535/task-api)"
}


def fetch_page(url, cache_file):
    if cache_file.exists():
        html = cache_file.read_text(encoding="utf-8")

        print(f"CACHE HIT: {url}")
        print(f"Response size: {len(html)} bytes")

        return html

    print(f"FETCH: {url}")

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=10
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Request failed with status code {response.status_code}"
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

    print(f"Response size: {len(html)} bytes")

    return html


def extract_book_urls(html, page_url):
    soup = BeautifulSoup(html, "html.parser")

    book_urls = []

    for article in soup.select("article.product_pod"):
        link = article.select_one("h3 a")

        if link:
            href = link.get("href")

            if href:
                absolute_url = urljoin(page_url, href)
                book_urls.append(absolute_url)

    return book_urls


def find_next_page(html, page_url):
    soup = BeautifulSoup(html, "html.parser")

    next_link = soup.select_one("li.next a")

    if next_link:
        href = next_link.get("href")

        if href:
            return urljoin(page_url, href)

    return None


def main():
    current_url = BASE_URL
    all_book_urls = []
    catalogue_pages = 0

    while catalogue_pages < 3:
        catalogue_pages += 1

        cache_file = CACHE_DIR / f"catalogue-page-{catalogue_pages}.html"

        html = fetch_page(
            current_url,
            cache_file
        )

        book_urls = extract_book_urls(
            html,
            current_url
        )

        all_book_urls.extend(book_urls)

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
                    "Could not find the next catalogue page"
                )

            current_url = next_url

            # Polite delay before the next real request.
            # Cache hits do not need a delay.
            if not (
                CACHE_DIR / f"catalogue-page-{catalogue_pages + 1}.html"
            ).exists():
                time.sleep(0.5)

    unique_urls = list(dict.fromkeys(all_book_urls))

    print()
    print(f"catalogue_pages={catalogue_pages}")
    print(f"discovered={len(all_book_urls)}")
    print(f"unique_urls={len(unique_urls)}")


if __name__ == "__main__":
    main()