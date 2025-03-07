from fastapi import APIRouter

health_router = APIRouter()


@health_router.get("/ping")
def pong():
    return {"message": "pong from api"}
