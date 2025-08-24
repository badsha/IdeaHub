from pydantic import BaseModel
from typing import Optional

class Idea(BaseModel):
    id: int
    community_id: int
    campaign_id: Optional[int] = None
    author_member_id: Optional[int] = None
    title: str
    body: str
    visibility: str = "public"
