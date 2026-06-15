from fastapi import APIRouter, Depends
from dependencies import log_request


router = APIRouter(
    prefix="/users", 
    tags=["users"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(log_request)]
    )

users_list = [
    {"id": "user1", "username": "user1", "email": "email1"},
    {"id": "user2", "username": "user2", "email": "email2"},
]

@router.get("/", tags=["Get all"])
async def get_users():
    return users_list

@router.get("/{user_id}", tags=["Get by ID"])
async def get_user(user_id: str):
    for user in users_list:
        if user["id"] == user_id:
            return user
    return {"error": "User not found"}

