from typing import Dict, List

from pydantic import BaseModel


class SearchResponse(BaseModel):
    status: str
    username: str
    pattern: str
    matches: List[Dict]

    class Config:
        anystr_strip_whitespace = True
