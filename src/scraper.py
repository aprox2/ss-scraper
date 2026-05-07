import time
import requests

BASE_URL = "https://www.ss.lv"
SORT_PRICE_ASC = "fDgSeF4belM="

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "lv",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def create_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(HEADERS)
    return session


def fetch_listing_page(session: requests.Session, make_slug: str) -> str:
    url = f"{BASE_URL}/lv/transport/cars/{make_slug}/{SORT_PRICE_ASC}.html"
    response = session.get(url, timeout=30)
    response.raise_for_status()
    return response.text


def fetch_detail_page(session: requests.Session, path: str) -> str:
    url = f"{BASE_URL}{path}"
    time.sleep(1)
    response = session.get(url, timeout=30)
    response.raise_for_status()
    return response.text
