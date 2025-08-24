from pydantic import BaseModel
from typing import Optional, List

class Workspace(BaseModel):
    id: int
    name: str
    public_default: bool = True
    features: Optional[List[str]] = None
