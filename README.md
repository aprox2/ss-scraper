# SS.lv Car Scraper

A Python scraper that monitors [SS.lv](https://www.ss.lv) car listings and sends notifications about new listings to Discord via webhooks.

## Features

- Scrapes car listings from SS.lv (Latvia's largest classifieds site)
- Tracks seen listings to only notify about new ones
- Sends rich Discord embed notifications with car details (year, engine, fuel type, mileage, tech inspection, price)
- Configurable car makes to monitor
- Sorts listings by price (ascending)

## Project Structure

```
ss-scraper/
├── main.py              # Entry point - orchestrates scraping and notifications
├── config.json          # Car makes to monitor
├── seen_cars.json       # State file tracking already-seen listing IDs
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
└── src/
    ├── scraper.py       # HTTP session and page fetching
    ├── parser.py        # HTML parsing for listings and detail pages
    ├── notifier.py      # Discord webhook notifications
    ├── models.py        # CarListing and CarDetails dataclasses
    └── state.py         # Persistence for seen listing IDs
```

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/aprox2/ss-scraper.git
   cd ss-scraper
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set your Discord webhook URL:
   ```
   DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your/webhook
   ```

4. **Configure car makes to monitor:**

   Edit `config.json` to add or remove car makes:
   ```json
   {
     "car_makes": [
       {"name": "BMW", "slug": "bmw"},
       {"name": "Audi", "slug": "audi"},
       {"name": "Mercedes", "slug": "mercedes-benz"}
     ]
   }
   ```
   The `slug` must match the SS.lv URL path for that make (e.g. `https://www.ss.lv/lv/transport/cars/bmw/`).

## Usage

```bash
python main.py
```

The scraper will:
1. Load configured car makes from `config.json`
2. Fetch the listing page for each make from SS.lv
3. Compare listings against previously seen IDs in `seen_cars.json`
4. Fetch detail pages for new listings
5. Send Discord notifications with car details
6. Save all current listing IDs to `seen_cars.json`

## Discord Notifications

Each notification includes an embed per car with:
- Make and model (as the title, linked to the SS.lv listing)
- Year, engine size, fuel type
- Mileage, tech inspection date, price

Discord limits 10 embeds per message, so notifications are automatically batched.

## Dependencies

- [requests](https://docs.python-requests.org/) - HTTP requests
- [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing
- [python-dotenv](https://github.com/theskumar/python-dotenv) - Environment variable loading from `.env`
