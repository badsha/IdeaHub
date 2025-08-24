from fastapi import APIRouter, Query

router = APIRouter()

@router.get("/search")
def search(q: str = Query(default="")):
    return {"q": q, "items": []}
