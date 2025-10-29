import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from ..models.cron import Listing
from .db import get_db_connection

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
headers = {
    "Accept": "application/vnd.github.raw+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
}


# Gets listings from the GitHub API
def get_listings():
    current_year = datetime.now().year

    for year in range(current_year + 1, current_year - 2, -1):
        ENDPOINT = f"https://api.github.com/repos/SimplifyJobs/Summer{year}-Internships/contents/.github/scripts/listings.json"

        r = requests.get(ENDPOINT, headers=headers)
        if r.ok:
            raw_listings = r.json()
            listings = [Listing.from_json(listing) for listing in raw_listings]
            return listings
    assert False, "No listings found"


# Assigns company logos to listings
def assign_logos(listings: list[Listing]):
    with get_db_connection() as conn:
        # Get existing company logos
        with conn.cursor() as cur:
            cur.execute("SELECT company_name, url FROM logos;")
            existing_logos = {
                row[0].strip().lower(): row[1] for row in cur.fetchall() if row[0]
            }

        # Assign logos, scraping if necessary
        new_logos = []
        for listing in listings:
            company_key = listing.company_name.strip().lower()
            if company_key not in existing_logos:
                logo_url = scrape_company_logo(listing)
                new_logos.append((listing.company_name, logo_url))
                existing_logos[company_key] = logo_url
                listing.company_logo = logo_url
        if new_logos:
            with conn.cursor() as cur:
                cur.executemany(
                    """
                    INSERT INTO logos (company_name, url)
                    VALUES (%s, %s)
                    ON CONFLICT (company_name) DO NOTHING;
                """,
                    new_logos,
                )


# Scrapes company logo from Simplify website
def scrape_company_logo(listing: Listing) -> str | None:
    # Only scrape companies on Simplify
    if not listing.company_url.startswith("https://simplify.jobs/c/"):
        return None

    soup = BeautifulSoup(requests.get(listing.company_url).text, "html.parser")
    img = soup.find(name="img", attrs={"alt": listing.company_name})
    if img:
        return str(img["src"])
    return None


# Inserts listings into DB
def insert_listings(listings: list[Listing]):
    with get_db_connection() as conn:
        # Update listings
        conn.execute("TRUNCATE TABLE listings;")
        with conn.cursor() as cur:
            cur.executemany(
                """
                INSERT INTO listings (
                    id, source, company_name, title, active,
                    date_updated, is_visible, date_posted, url,
                    locations, company_url, terms, sponsorship,
                    category, faang_plus, company_logo
                ) VALUES (
                    %(id)s, %(source)s, %(company_name)s, %(title)s, %(active)s,
                    %(date_updated)s, %(is_visible)s, %(date_posted)s, %(url)s,
                    %(locations)s, %(company_url)s, %(terms)s, %(sponsorship)s,
                    %(category)s, %(faang_plus)s, %(company_logo)s
                );
            """,
                [l.model_dump() for l in listings],
            )
