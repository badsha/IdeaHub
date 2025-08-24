from typing import Optional, Dict
from .repository import WorkspaceRepository

class WorkspaceService:
    def __init__(self, repo: WorkspaceRepository):
        self.repo = repo

    def get(self, ws_id: int) -> Optional[Dict]:
        return self.repo.get_by_id(ws_id)
