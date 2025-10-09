import json
import os

VERCEL_ENV = os.getenv("VERCEL_ENV")
VERCEL_RELATED_PROJECTS = os.getenv("VERCEL_RELATED_PROJECTS")

DEFAULT_URL = "http://localhost:5173"


def get_allowed_origin() -> str:
    # Local
    if VERCEL_ENV is None or VERCEL_RELATED_PROJECTS is None:
        return DEFAULT_URL

    related_projects = json.loads(VERCEL_RELATED_PROJECTS)
    project = related_projects[0]

    # Preview
    if VERCEL_ENV == "preview":
        branch = project.get("preview", {}).get("branch")
        if branch:
            return f"https://{branch}"

    # Production
    if VERCEL_ENV == "production":
        production = project.get("production", {})
        alias = production.get("alias")
        url = production.get("url")

        if alias:
            return f"https://{alias}"
        if url:
            return f"https://{url}"

    # Default
    return DEFAULT_URL
