from datetime import datetime
from uuid import UUID
from zoneinfo import ZoneInfo

from pydantic import BaseModel

pst = ZoneInfo("America/Los_Angeles")

from .companies import Company


class Listing(BaseModel):
    id: UUID
    source: str
    title: str
    active: bool
    date_updated: datetime
    is_visible: bool
    date_posted: datetime
    url: str
    locations: list[str]
    terms: list[str]
    sponsorship: str
    category: str
    faang_plus: bool
    company: Company

    @staticmethod
    def from_json(raw_listing: dict):
        from ..util.cron import classifyFaangPlus, classifyJobCategory

        parsed_json = raw_listing
        parsed_json["date_posted"] = datetime.fromtimestamp(
            raw_listing.get("date_posted", 0), tz=pst
        )
        parsed_json["date_updated"] = datetime.fromtimestamp(
            raw_listing.get("date_updated", 0), tz=pst
        )
        parsed_json["category"] = classifyJobCategory(raw_listing)
        parsed_json["faang_plus"] = classifyFaangPlus(raw_listing)

        company_name = parsed_json["company_name"]
        del parsed_json["company_name"]
        company_url = parsed_json["company_url"]
        del parsed_json["company_url"]
        parsed_json["company"] = Company(name=company_name, url=company_url)

        return Listing.model_validate(parsed_json)

    @classmethod
    def from_tuple(cls, row: tuple):
        return cls(
            id=row[0],
            source=row[1],
            title=row[2],
            active=row[3],
            date_updated=row[4],
            is_visible=row[5],
            date_posted=row[6],
            url=row[7],
            locations=row[8] if isinstance(row[8], list) else [],
            terms=row[9] if isinstance(row[9], list) else [],
            sponsorship=row[10],
            category=row[11],
            faang_plus=row[12],
            company=Company(id=row[13], name=row[14], url=row[15], logo_url=row[16]),
        )

    def to_tuple(self):
        return (
            self.id,
            self.source,
            self.title,
            self.active,
            self.date_updated,
            self.is_visible,
            self.date_posted,
            self.url,
            self.locations,
            self.terms,
            self.sponsorship,
            self.category,
            self.faang_plus,
            self.company.id,
        )
