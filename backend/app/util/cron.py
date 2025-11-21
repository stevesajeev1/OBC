import os
from datetime import datetime
from uuid import uuid4

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from ..models.companies import Company
from ..models.listings import Listing
from .companies import get_companies_from_db
from .db import get_db_connection

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
headers = {
    "Accept": "application/vnd.github.raw+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
}


# Classifies a listing into a category
def classifyJobCategory(job):
    # Always classify by title for better accuracy, ignore existing category
    title = job.get("title", "").lower()

    # Filter out IT technical support roles that aren't really tech internships
    if any(
        term in title
        for term in [
            "it technical intern",
            "it technician",
            "it support",
            "technical support intern",
            "help desk",
            "desktop support",
            "it help desk",
            "computer support",
            "security operations",
            "field operations",
            "information technology",
        ]
    ):
        return "IT Technical Support"

    # Hardware (first priority) - expanded keywords
    if any(
        term in title
        for term in [
            "hardware",
            "embedded",
            "fpga",
            "circuit",
            "chip",
            "silicon",
            "asic",
            "robotics",
            "firmware",
            "manufactur",
            "electrical",
            "mechanical",
            "systems engineer",
            "test engineer",
            "validation",
            "verification",
            "pcb",
            "analog",
            "digital",
            "signal",
            "power",
            "rf",
            "antenna",
        ]
    ):
        return "Hardware Engineering"

    # Quant (second priority) - expanded keywords
    elif any(
        term in title
        for term in [
            "quant",
            "quantitative",
            "trading",
            "finance",
            "investment",
            "financial",
            "risk",
            "portfolio",
            "derivatives",
            "algorithmic trading",
            "market",
            "capital",
            "equity",
            "fixed income",
            "credit",
        ]
    ):
        return "Quantitative Finance"

    # Data Science (third priority) - expanded keywords
    elif any(
        term in title
        for term in [
            "data science",
            "artificial intelligence",
            "data scientist",
            "ai",
            "machine learning",
            "ml",
            "data analytics",
            "data analyst",
            "research eng",
            "nlp",
            "computer vision",
            "research sci",
            "data eng",
            "analytics",
            "statistician",
            "modeling",
            "algorithms",
            "deep learning",
            "pytorch",
            "tensorflow",
            "pandas",
            "numpy",
            "sql",
            "etl",
            "pipeline",
            "big data",
            "spark",
            "hadoop",
        ]
    ):
        return "Data Science, AI & Machine Learning"

    # Product (fourth priority) - check before Software to catch "Software Product Management" roles
    elif any(
        term in title
        for term in [
            "product manag",
            "product analyst",
            "apm",
            "associate product",
            "product owner",
            "product design",
            "product marketing",
            "product strategy",
            "business analyst",
            "program manag",
            "project manag",
        ]
    ) or (
        "product" in title
        and any(
            word in title for word in ["analyst", "manager", "associate", "coordinator"]
        )
    ):
        return "Product Management"

    # Software Engineering (fifth priority) - greatly expanded keywords
    elif any(
        term in title
        for term in [
            "software",
            "engineer",
            "developer",
            "dev",
            "programming",
            "coding",
            "fullstack",
            "full-stack",
            "full stack",
            "frontend",
            "front end",
            "front-end",
            "backend",
            "back end",
            "back-end",
            "mobile",
            "web",
            "app",
            "application",
            "platform",
            "infrastructure",
            "cloud",
            "devops",
            "sre",
            "site reliability",
            "systems",
            "network",
            "security",
            "cybersecurity",
            "qa",
            "quality assurance",
            "test",
            "automation",
            "ci/cd",
            "deployment",
            "kubernetes",
            "docker",
            "aws",
            "azure",
            "gcp",
            "api",
            "microservices",
            "database",
            "java",
            "python",
            "javascript",
            "react",
            "node",
            "golang",
            "rust",
            "c++",
            "c#",
            ".net",
            "ios",
            "android",
            "flutter",
            "technical",
            "technology",
            "tech",
            "coding",
            "programming",
            "sde",
            "swe",
        ]
    ):
        return "Software Engineering"

    # Return None for jobs that don't fit any category (will be filtered out)
    else:
        return "Software Engineering"


# Classifies a listing as FAANG+
def classifyFaangPlus(job):
    FAANG_PLUS = {
        "airbnb",
        "adobe",
        "amazon",
        "amd",
        "anthropic",
        "apple",
        "asana",
        "atlassian",
        "bytedance",
        "cloudflare",
        "coinbase",
        "crowdstrike",
        "databricks",
        "datadog",
        "doordash",
        "dropbox",
        "duolingo",
        "figma",
        "google",
        "ibm",
        "instacart",
        "intel",
        "linkedin",
        "lyft",
        "meta",
        "microsoft",
        "netflix",
        "notion",
        "nvidia",
        "openai",
        "oracle",
        "palantir",
        "paypal",
        "perplexity",
        "pinterest",
        "ramp",
        "reddit",
        "rippling",
        "robinhood",
        "roblox",
        "salesforce",
        "samsara",
        "servicenow",
        "shopify",
        "slack",
        "snap",
        "snapchat",
        "spacex",
        "splunk",
        "snowflake",
        "stripe",
        "square",
        "tesla",
        "tinder",
        "tiktok",
        "uber",
        "visa",
        "waymo",
        "x",
    }
    return job.get("company_name", "").lower() in FAANG_PLUS


# Gets listings from the GitHub API
def get_listings():
    current_year = datetime.now().year

    for year in range(current_year + 1, current_year - 2, -1):
        ENDPOINT = f"https://api.github.com/repos/SimplifyJobs/Summer{year}-Internships/contents/.github/scripts/listings.json"

        r = requests.get(ENDPOINT, headers=headers)
        if r.ok:
            raw_listings = r.json()
            listings = [Listing.from_json(listing) for listing in raw_listings]
            listings = ensure_unique_ids(listings)
            return listings
    assert False, "No listings found"


# Ensures each listing has a unique ID
def ensure_unique_ids(listings: list[Listing]):
    unique_ids = set()
    unique_listings: list[Listing] = []
    for listing in listings:
        if listing.id in unique_ids:
            listing.id = uuid4()
        unique_ids.add(listing.id)
        unique_listings.append(listing)
    return unique_listings


# Assigns companies to listings
def assign_companies(listings: list[Listing]):
    existing_companies = get_companies_from_db()
    existing_map = {c.name.strip().lower(): c for c in existing_companies}

    # Scrape new logos
    new_companies: list[Company] = []
    for listing in listings:
        key = listing.company.name.strip().lower()
        if key not in existing_map:
            scrape_company_logo(listing.company)
            new_companies.append(listing.company)
            existing_map[key] = listing.company
    if new_companies:
        ids = insert_companies(new_companies)
        for company, id in zip(new_companies, ids):
            company.id = id
            key = company.name.strip().lower()
            existing_map[key] = company

    # Assign companies
    for listing in listings:
        key = listing.company.name.strip().lower()
        listing.company = existing_map[key]


# Scrapes company logo from Simplify website
def scrape_company_logo(company: Company) -> str | None:
    # Only scrape companies on Simplify
    if not company.url.startswith("https://simplify.jobs/c/"):
        return None

    soup = BeautifulSoup(requests.get(company.url).text, "html.parser")
    img = soup.find(name="img", attrs={"alt": company.name})
    if img:
        company.logo_url = str(img["src"])


# Inserts companies into DB
def insert_companies(companies: list[Company]):
    with get_db_connection() as conn:
        # Update companies
        with conn.cursor() as cur:
            cur.executemany(
                """
                INSERT INTO companies (name, url, logo_url)
                VALUES (%s, %s, %s)
                ON CONFLICT (name) DO NOTHING;
            """,
                [c.to_tuple() for c in companies],
            )

            company_names = [c.name for c in companies]
            cur.execute(
                """
                SELECT id, name
                FROM companies
                WHERE name = ANY(%s);
                """,
                (company_names,),
            )
            id_map = {row[1].strip().lower(): row[0] for row in cur.fetchall()}
            return [id_map[c.name.strip().lower()] for c in companies]


# Inserts listings into DB
def insert_listings(listings: list[Listing]):
    if not listings:
        return

    listing_tuples = [l.to_tuple() for l in listings]
    new_ids = [(l.id,) for l in listings]

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Upsert listings
            cur.executemany(
                """
                INSERT INTO listings (
                    id, source, title, active, date_updated, is_visible,
                    date_posted, url, locations, terms, sponsorship,
                    category, faang_plus, company_id
                ) VALUES (
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s
                )
                ON CONFLICT (id) DO UPDATE SET
                    source = EXCLUDED.source,
                    title = EXCLUDED.title,
                    active = EXCLUDED.active,
                    date_updated = EXCLUDED.date_updated,
                    is_visible = EXCLUDED.is_visible,
                    date_posted = EXCLUDED.date_posted,
                    url = EXCLUDED.url,
                    locations = EXCLUDED.locations,
                    terms = EXCLUDED.terms,
                    sponsorship = EXCLUDED.sponsorship,
                    category = EXCLUDED.category,
                    faang_plus = EXCLUDED.faang_plus,
                    company_id = EXCLUDED.company_id;
                """,
                listing_tuples,
            )

            # Delete old listings
            cur.execute("CREATE TEMP TABLE tmp_listing_ids(id UUID) ON COMMIT DROP;")

            cur.executemany("INSERT INTO tmp_listing_ids(id) VALUES (%s);", new_ids)

            cur.execute(
                """
                DELETE FROM listings
                WHERE id NOT IN (SELECT id FROM tmp_listing_ids);
                """
            )

        conn.commit()
