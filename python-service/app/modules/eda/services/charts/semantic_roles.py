"""
Column semantic role detection.

Goes beyond dtype (numeric/categorical/datetime/boolean) to answer:
what does this column *mean* for chart generation? An "id" and a
"revenue" column are both numeric, but only one should ever be
summed or averaged. This is the layer that was missing before — it's
what lets the candidate generator refuse to build nonsense charts.
"""
from dataclasses import dataclass
from enum import Enum
from typing import List
import re

import pandas as pd


class SemanticRole(str, Enum):
    IDENTIFIER = "identifier"
    MEASURE = "measure"
    DIMENSION = "dimension"
    DATETIME = "datetime"
    GEOGRAPHIC = "geographic"
    BOOLEAN_FLAG = "boolean_flag"
    TEXT = "text"
    IGNORE = "ignore"


_ID_PATTERN = re.compile(r"(^id$|_id$|^uuid$|^guid$)", re.I)
# Continuous coordinates — not groupable, excluded from bar/pie candidates.
_GEO_COORDINATE_PATTERN = re.compile(r"(latitude|longitude|^lat$|^lon$|^lng$)", re.I)
# Place names — categorical and one of the best groupable dimensions there
# is ("revenue by region"), so these are classified as DIMENSION directly
# rather than a separate excluded GEOGRAPHIC bucket.
_GEO_NAME_PATTERN = re.compile(r"(country|state|city|region|zip|postal)", re.I)


@dataclass
class ColumnRole:
    name: str
    role: SemanticRole
    dtype: str
    cardinality: int
    null_percent: float
    unit: str = ""


def detect_semantic_roles(
    df: pd.DataFrame,
    column_metadata: List[dict],
) -> List[ColumnRole]:

    roles = []
    n_rows = max(len(df), 1)

    for col in column_metadata:
        name = col["name"]
        if name not in df.columns:
            continue

        dtype_category = col.get("category", "categorical")
        unit = col.get("unit", "")

        series = df[name]
        cardinality = int(series.nunique(dropna=True))
        null_percent = round(float(series.isna().mean() * 100), 2)
        uniqueness_ratio = cardinality / n_rows
        is_integer_dtype = pd.api.types.is_integer_dtype(series)

        role = _classify_column(
            name=name,
            dtype_category=dtype_category,
            cardinality=cardinality,
            uniqueness_ratio=uniqueness_ratio,
            is_integer_dtype=is_integer_dtype,
        )

        roles.append(
            ColumnRole(
                name=name,
                role=role,
                dtype=dtype_category,
                cardinality=cardinality,
                null_percent=null_percent,
                unit=unit,
            )
        )

    return roles


def _classify_column(
    name: str,
    dtype_category: str,
    cardinality: int,
    uniqueness_ratio: float,
    is_integer_dtype: bool,
) -> SemanticRole:

    if _ID_PATTERN.search(name):
        return SemanticRole.IDENTIFIER

    if _GEO_COORDINATE_PATTERN.search(name):
        return SemanticRole.GEOGRAPHIC

    if _GEO_NAME_PATTERN.search(name) and dtype_category == "categorical":
        return SemanticRole.DIMENSION

    if dtype_category == "datetime":
        return SemanticRole.DATETIME

    if dtype_category == "boolean":
        return SemanticRole.BOOLEAN_FLAG

    if dtype_category == "numeric":
        # A constant column (every value identical) has zero variance —
        # correlation and std against it are mathematically NaN, and it
        # carries no business signal either way. Excluding it here is
        # what stops NaN from ever entering the aggregation/statistics
        # layer downstream.
        if cardinality <= 1:
            return SemanticRole.IGNORE

        # Near-unique *integer* columns behave like identifiers (e.g. an
        # auto-increment transaction_ref). Near-unique *float* columns are
        # normal for continuous measures like revenue or price — almost
        # every value is naturally distinct, that's not an ID signal.
        if is_integer_dtype and uniqueness_ratio > 0.95 and cardinality > 50:
            return SemanticRole.IDENTIFIER
        return SemanticRole.MEASURE

    if dtype_category == "categorical":
        # High-cardinality "categorical" columns are usually free
        # text (names, comments, addresses) rather than a groupable
        # dimension — grouping by them produces useless mega-charts.
        if uniqueness_ratio > 0.9 and cardinality > 50:
            return SemanticRole.TEXT
        return SemanticRole.DIMENSION

    return SemanticRole.IGNORE