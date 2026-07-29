from pydantic import BaseModel
from typing import Any


class AnalyzeS3Request(BaseModel):
    session_id: str
    s3_key: str


