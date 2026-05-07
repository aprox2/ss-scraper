import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

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

    retry = Retry(
        total=3,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

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
