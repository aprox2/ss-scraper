import re

from bs4 import BeautifulSoup

from src.models import CarDetails, CarListing

LISTING_ID_PATTERN = re.compile(r"/msg/lv/transport/cars/[^/]+/[^/]+/([^.]+)\.html")


def parse_listings(html: str, make_name: str) -> list[CarListing]:
    soup = BeautifulSoup(html, "html.parser")
    listings = []

    for row in soup.find_all("tr", id=lambda x: x and x.startswith("tr_")):
        link = row.find("a", class_="am")
        if not link:
            continue

        href = link.get("href", "")
        match = LISTING_ID_PATTERN.search(href)
        if not match:
            continue

        listing_id = match.group(1)

        tds = row.find_all("td", class_=lambda c: c and ("msga2-o" in c or "msga2-r" in c))
        # Columns after the title: Model, Year, Engine, Mileage, Price
        values = [_cell_text(td) for td in tds]

        if len(values) < 5:
            continue

        listings.append(CarListing(
            id=listing_id,
            url=href,
            title=link.get_text(strip=True),
            model=values[0],
            year=values[1],
            engine=values[2],
            mileage=values[3],
            price=values[4],
            make_name=make_name,
        ))

    return listings


def parse_detail(html: str) -> CarDetails:
    soup = BeautifulSoup(html, "html.parser")

    fields = {}
    for label_td in soup.find_all("td", class_="ads_opt_name"):
        label = label_td.get_text(strip=True).rstrip(":")
        value_td = label_td.find_next_sibling("td", class_="ads_opt")
        if value_td:
            fields[label] = value_td.get_text(strip=True)

    # Parse engine + fuel from "Motors" field (e.g. "2.0 dīzelis")
    motor = fields.get("Motors", "")
    engine, fuel_type = _parse_motor(motor)

    # Price from dedicated price element
    price_el = soup.find("span", class_="ads_price", id="tdo_8")
    price = price_el.get_text(strip=True) if price_el else ""

    # Make from "Marka" field
    marka = fields.get("Marka", "")

    return CarDetails(
        id="",  # filled by caller
        url="",  # filled by caller
        make=marka,
        model=_extract_model(marka),
        year=fields.get("Izlaiduma gads", ""),
        engine=engine,
        fuel_type=fuel_type,
        mileage=fields.get("Nobraukums, km", ""),
        tech_inspection=fields.get("Tehniskā apskate", ""),
        price=price,
    )


def _cell_text(td) -> str:
    return td.get_text(strip=True)


def _parse_motor(motor: str) -> tuple[str, str]:
    if not motor:
        return ("", "")

    parts = motor.split(None, 1)
    engine = parts[0] if parts else ""
    fuel_type = parts[1] if len(parts) > 1 else ""

    fuel_map = {
        "benzīns": "Petrol",
        "dīzelis": "Diesel",
        "hibrīds": "Hybrid",
        "elektriskais": "Electric",
        "benzīns/gāze": "Petrol/Gas",
    }
    fuel_type = fuel_map.get(fuel_type.lower(), fuel_type)

    return (engine, fuel_type)


def _extract_model(marka: str) -> str:
    # Marka is like "Bmw 520" - extract the model part after the make name
    parts = marka.split(None, 1)
    return parts[1] if len(parts) > 1 else marka
