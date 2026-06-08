
from fastapi import APIRouter

pamela_cook_router = APIRouter(prefix="/friday_13th/pamela", tags=["pamela"])

@pamela_cook_router.get("/signup")
async def signup_pamela():
    return {"message": "Pamela signed up!"}