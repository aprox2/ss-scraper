import json
import os
import sys
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

from src.notifier import send_discord_notification
from src.parser import parse_detail, parse_listings
from src.scraper import create_session, fetch_detail_page, fetch_listing_page, SORT_PRICE_ASC_PAGE_2
from src.state import cleanup_old, load_seen, save_seen

load_dotenv()

CONFIG_PATH = Path(__file__).parent / "config.json"
STATE_PATH = Path(__file__).parent / "seen_cars.json"


def main():
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL", "")
    if not webhook_url:
        print("DISCORD_WEBHOOK_URL not set, skipping notifications")

    config = json.loads(CONFIG_PATH.read_text())
    seen_ids = load_seen(str(STATE_PATH))
    session = create_session()

    # Clean up entries older than 3 months
    before_cleanup = len(seen_ids)
    seen_ids = cleanup_old(seen_ids)
    removed = before_cleanup - len(seen_ids)
    if removed:
        print(f"Cleaned up {removed} entries older than 3 months")

    today = date.today().isoformat()
    all_new_cars = []
    all_current_ids = {}

    for make in config["car_makes"]:
        make_name = make["name"]
        make_slug = make["slug"]

        print(f"Fetching listings for {make_name}...")
        html = fetch_listing_page(session, make_slug)
        listings = parse_listings(html, make_name)

        html_page2 = fetch_listing_page(session, make_slug, SORT_PRICE_ASC_PAGE_2)
        listings_page2 = parse_listings(html_page2, make_name)

        seen_ids_page1 = {l.id for l in listings}
        listings += [l for l in listings_page2 if l.id not in seen_ids_page1]
        print(f"  Found {len(listings)} listings (2 pages)")

        current_ids = {listing.id: today for listing in listings}
        all_current_ids.update(current_ids)

        new_listings = [l for l in listings if l.id not in seen_ids]
        print(f"  {len(new_listings)} new listings")

        for listing in new_listings:
            print(f"  Fetching details for {listing.title[:60]}...")
            try:
                detail_html = fetch_detail_page(session, listing.url)
                details = parse_detail(detail_html)
                details.id = listing.id
                details.url = listing.url
                if details.gearbox != "Manual":
                    print(f"    Skipping (gearbox: {details.gearbox or 'unknown'})")
                    continue
                all_new_cars.append(details)
            except Exception as e:
                print(f"  Error fetching details for {listing.id}: {e}")

    print(f"\nTotal new cars: {len(all_new_cars)}")

    if all_new_cars and webhook_url:
        print("Sending Discord notification...")
        try:
            send_discord_notification(webhook_url, all_new_cars)
            print("Notification sent!")
        except Exception as e:
            print(f"Error sending notification: {e}")
            sys.exit(1)

    # Update state with all current listing IDs
    updated_ids = {**seen_ids, **all_current_ids}
    save_seen(str(STATE_PATH), updated_ids)
    print(f"State saved ({len(updated_ids)} total seen IDs)")


if __name__ == "__main__":
    main()
