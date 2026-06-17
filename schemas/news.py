from pydantic import BaseModel
from typing import List, Optional


class NewsArticle(BaseModel):
    title: str
    summary: Optional[str]
    url: str
    date: Optional[str]


class NewsResponse(BaseModel):
    query: str
    results: List[NewsArticle]
