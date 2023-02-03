from typing import List, Dict

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    status: str
    errors: List[Dict]
