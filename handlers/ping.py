from fastapi import APIRouter


router = APIRouter(prefix="/ping", tags=["ping"])


@router.get("/")
async def ping():
    return {"message": "ok"}


@router.get("/app")
async def ping_app():
    return {"text": "app is working"}
