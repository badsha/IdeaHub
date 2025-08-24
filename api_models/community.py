from pydantic import BaseModel

class Community(BaseModel):
    id: int
    workspace_id: int
    name: str
    public: bool = True
