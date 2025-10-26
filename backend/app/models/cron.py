from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import BaseModel

pst = ZoneInfo("America/Los_Angeles")

# Classifies a listing into a category
def classifyJobCategory(job):
    # Always classify by title for better accuracy, ignore existing category
    title = job.get("title", "").lower()

    # Filter out IT technical support roles that aren't really tech internships
    if any(term in title for term in [
        "it technical intern", "it technician", "it support", "technical support intern",
        "help desk", "desktop support", "it help desk", "computer support", "security operations", "field operations",
        "information technology"
    ]):
        return "IT Technical Support"

    # Hardware (first priority) - expanded keywords
    if any(term in title for term in [
        "hardware", "embedded", "fpga", "circuit", "chip", "silicon", "asic", "robotics", "firmware",
        "manufactur", "electrical", "mechanical", "systems engineer", "test engineer", "validation",
        "verification", "pcb", "analog", "digital", "signal", "power", "rf", "antenna"
    ]):
        return "Hardware Engineering"

    # Quant (second priority) - expanded keywords
    elif any(term in title for term in [
        "quant", "quantitative", "trading", "finance", "investment", "financial", "risk", "portfolio",
        "derivatives", "algorithmic trading", "market", "capital", "equity", "fixed income", "credit"
    ]):
        return "Quantitative Finance"

    # Data Science (third priority) - expanded keywords
    elif any(term in title for term in [
        "data science", "artificial intelligence", "data scientist", "ai", "machine learning", "ml",
        "data analytics", "data analyst", "research eng", "nlp", "computer vision", "research sci",
        "data eng", "analytics", "statistician", "modeling", "algorithms", "deep learning", "pytorch",
        "tensorflow", "pandas", "numpy", "sql", "etl", "pipeline", "big data", "spark", "hadoop"
    ]):
        return "Data Science, AI & Machine Learning"

    # Product (fourth priority) - check before Software to catch "Software Product Management" roles
    elif any(term in title for term in [
        "product manag", "product analyst", "apm", "associate product", "product owner", "product design",
        "product marketing", "product strategy", "business analyst", "program manag", "project manag"
    ]) or ("product" in title and any(word in title for word in ["analyst", "manager", "associate", "coordinator"])):
        return "Product Management"

    # Software Engineering (fifth priority) - greatly expanded keywords
    elif any(term in title for term in [
        "software", "engineer", "developer", "dev", "programming", "coding", "fullstack", "full-stack",
        "full stack", "frontend", "front end", "front-end", "backend", "back end", "back-end",
        "mobile", "web", "app", "application", "platform", "infrastructure", "cloud", "devops",
        "sre", "site reliability", "systems", "network", "security", "cybersecurity", "qa",
        "quality assurance", "test", "automation", "ci/cd", "deployment", "kubernetes", "docker",
        "aws", "azure", "gcp", "api", "microservices", "database", "java", "python", "javascript",
        "react", "node", "golang", "rust", "c++", "c#", ".net", "ios", "android", "flutter",
        "technical", "technology", "tech", "coding", "programming", "sde", "swe"
    ]):
        return "Software Engineering"

    # Return None for jobs that don't fit any category (will be filtered out)
    else:
        return "Software Engineering"


# Classifies a listing as FAANG+
def classifyFaangPlus(job):
    FAANG_PLUS = {
        "airbnb", "adobe", "amazon", "amd", "anthropic", "apple", "asana", "atlassian", "bytedance", "cloudflare","coinbase", "crowdstrike","databricks", "datadog",
        "doordash", "dropbox", "duolingo", "figma", "google", "ibm", "instacart", "intel", "linkedin", "lyft", "meta", "microsoft",
        "netflix", "notion", "nvidia", "openai", "oracle", "palantir", "paypal", "perplexity", "pinterest", "ramp", "reddit","rippling", "robinhood", "roblox",
        "salesforce", "samsara", "servicenow", "shopify", "slack", "snap", "snapchat", "spacex", "splunk","snowflake", "stripe", "square", "tesla", "tinder","tiktok", "uber",
        "visa","waymo", "x"
    }
    return job.get("company_name", "").lower() in FAANG_PLUS


class Listing(BaseModel):
    source: str
    company_name: str
    id: str
    title: str
    active: bool
    date_updated: datetime
    is_visible: bool
    date_posted: datetime
    url: str
    locations: list[str]
    company_url: str
    terms: list[str]
    sponsorship: str
    category: str
    faang_plus: bool
    company_logo: str | None = None

    @staticmethod
    def from_json(raw_listing):
        parsed_json = raw_listing
        parsed_json["date_posted"] = datetime.fromtimestamp(raw_listing.get("date_posted", 0), tz=pst)
        parsed_json["date_updated"] = datetime.fromtimestamp(raw_listing.get("date_updated", 0), tz=pst)
        parsed_json["category"] = classifyJobCategory(raw_listing)
        parsed_json["faang_plus"] = classifyFaangPlus(raw_listing)
        return Listing.model_validate(parsed_json)