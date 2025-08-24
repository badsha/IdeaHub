from fastapi import APIRouter

router = APIRouter(prefix="/ideas")

@router.get("/{idea_id}")
def get_idea(idea_id: int):
    return {"id": idea_id, "community_id": 1, "title": "Hello", "body": "World"}
