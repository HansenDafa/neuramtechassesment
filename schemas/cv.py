from pydantic import BaseModel
from typing import Optional


class CVSummaryResponse(BaseModel):
    name: Optional[str]
    location: Optional[str]
    work_experience_summary: Optional[str]
    raw_text_excerpt: Optional[str]
