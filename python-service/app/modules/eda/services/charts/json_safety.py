"""
JSON-safety sanitizer.

Pandas/numpy computations produce NaN or Inf on plenty of edge cases
that are easy to miss upfront — a zero-variance column in .corr(), a
single-row group in .std(), a divide-by-zero in a derived stat. Any
one of those crashes FastAPI's default JSONResponse with
`ValueError: Out of range float values are not JSON compliant`.

Rather than chase every individual source, this recursively walks
the response and replaces NaN/Inf with None (-> JSON null) right
before it leaves the service. Call this once, at the boundary, on
whatever you're about to return from an endpoint.
"""
import math
from typing import Any


def sanitize_for_json(value: Any) -> Any:
    if isinstance(value, float):
        return None if (math.isnan(value) or math.isinf(value)) else value

    if isinstance(value, dict):
        return {k: sanitize_for_json(v) for k, v in value.items()}

    if isinstance(value, (list, tuple)):
        return [sanitize_for_json(v) for v in value]

    return value