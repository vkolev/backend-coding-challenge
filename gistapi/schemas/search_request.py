import re

from pydantic import BaseModel, Field, validator


class SearchRequest(BaseModel):
    username: str = Field(...)
    pattern: str = Field(...)

    @validator('username', pre=True)
    def username_validator(cls, v):
        if v is None or v == "":
            raise ValueError("is required")
        if ' ' in v:
            raise ValueError('cannot contain space')
        return v

    @validator('pattern', pre=True)
    def pattern_validator(cls, v):
        if v is None or v == '':
            raise ValueError("is required")
        try:
            re.compile(v)
            return v
        except re.error as error:
            raise ValueError(f"invalid pattern: {error}")

    class Config:
        anystr_strip_whitespace = True
        validate_assignment = True
