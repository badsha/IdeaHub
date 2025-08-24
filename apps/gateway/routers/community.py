from fastapi import APIRouter

router = APIRouter(prefix="/communities")

@router.get("/{community_id}")
def get_community(community_id: int):
    return {"id": community_id, "name": "Community", "workspace_id": 1, "public": True}
