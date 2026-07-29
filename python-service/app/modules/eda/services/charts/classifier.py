"""
Dataset type classifier.

Infers the broad business domain of the dataset from column names/
descriptions, so downstream recommendation logic can bias toward
chart types and phrasing that actually make sense for that domain.
Pure heuristic, no ML — cheap and good enough to steer scoring.
"""
from enum import Enum
from typing import Dict, List
import re


class DatasetType(str, Enum):
    SALES_TRANSACTIONAL = "sales_transactional"
    FINANCIAL = "financial"
    TIME_SERIES = "time_series"
    SURVEY_FEEDBACK = "survey_feedback"
    HR_PEOPLE = "hr_people"
    GEOSPATIAL = "geospatial"
    MARKETING = "marketing"
    GENERAL = "general"


_KEYWORD_MAP: Dict[DatasetType, List[str]] = {
    DatasetType.SALES_TRANSACTIONAL: [
        "sale", "revenue", "order", "invoice", "price", "quantity",
        "product", "sku", "discount", "profit", "cost",
    ],
    DatasetType.FINANCIAL: [
        "amount", "balance", "transaction", "account", "budget",
        "expense", "income", "asset", "liability", "currency",
    ],
    DatasetType.SURVEY_FEEDBACK: [
        "rating", "score", "satisfaction", "nps", "feedback",
        "survey", "response", "likert",
    ],
    DatasetType.HR_PEOPLE: [
        "employee", "salary", "department", "tenure", "attrition",
        "hire", "performance", "manager",
    ],
    DatasetType.GEOSPATIAL: [
        "latitude", "longitude", "lat", "lon", "country", "state",
        "city", "region", "zipcode", "postal",
    ],
    DatasetType.MARKETING: [
        "campaign", "click", "impression", "ctr", "conversion",
        "lead", "channel", "spend", "roi",
    ],
}


def classify_dataset(column_metadata: List[dict]) -> DatasetType:
    """
    Scores each dataset type by how many column names/descriptions
    match its keyword set and returns the best match. Falls back to
    TIME_SERIES if a datetime column dominates with no other domain
    winning, else GENERAL.
    """
    haystack = " ".join(
        f"{c.get('name', '')} {c.get('description', '')}".lower()
        for c in column_metadata
    )

    scores = {
        dtype: sum(1 for kw in keywords if re.search(rf"\b{kw}", haystack))
        for dtype, keywords in _KEYWORD_MAP.items()
    }

    best_type, best_score = max(scores.items(), key=lambda kv: kv[1])

    if best_score == 0:
        has_datetime = any(
            c.get("category") == "datetime" for c in column_metadata
        )
        return DatasetType.TIME_SERIES if has_datetime else DatasetType.GENERAL

    return best_type