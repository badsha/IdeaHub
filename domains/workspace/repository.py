from typing import Optional, Dict

class WorkspaceRepository:
    def __init__(self):
        # In-memory store for Milestone 2
        self._by_id: Dict[int, Dict] = {
            1: {"id": 1, "name": "Public WS", "public_default": True, "features": []},
        }

    def get_by_id(self, ws_id: int) -> Optional[Dict]:
        return self._by_id.get(ws_id)
