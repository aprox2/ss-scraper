import requests

from src.models import CarDetails

BASE_URL = "https://www.ss.lv"
MAX_EMBEDS_PER_MESSAGE = 10


def send_discord_notification(webhook_url: str, cars: list[CarDetails]) -> None:
    if not cars:
        return

    # Chunk into batches of 10 embeds (Discord limit)
    for i in range(0, len(cars), MAX_EMBEDS_PER_MESSAGE):
        batch = cars[i:i + MAX_EMBEDS_PER_MESSAGE]
        embeds = [build_embed(car) for car in batch]

        payload = {
            "username": "SS.LV Car Monitor",
            "embeds": embeds,
        }

        response = requests.post(webhook_url, json=payload, timeout=30)
        response.raise_for_status()


def build_embed(car: CarDetails) -> dict:
    fields = []

    if car.year:
        fields.append({"name": "Year", "value": car.year, "inline": True})
    if car.engine:
        fields.append({"name": "Engine", "value": car.engine, "inline": True})
    if car.fuel_type:
        fields.append({"name": "Fuel", "value": car.fuel_type, "inline": True})
    if car.mileage:
        fields.append({"name": "Mileage", "value": f"{car.mileage} km", "inline": True})
    if car.tech_inspection:
        fields.append({"name": "Tech Inspection", "value": car.tech_inspection, "inline": True})
    if car.price:
        fields.append({"name": "Price", "value": car.price, "inline": True})

    embed = {
        "title": f"{car.make}",
        "url": f"{BASE_URL}{car.url}",
        "color": 0x2ECC71,
        "fields": fields,
    }

    if car.description:
        desc = car.description if len(car.description) <= 300 else car.description[:297] + "..."
        embed["description"] = desc

    if car.image_url:
        embed["thumbnail"] = {"url": car.image_url}

    return embed
