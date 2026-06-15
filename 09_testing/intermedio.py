from fastapi import FastAPI, HTTPException, Header
from typing import Annotated
from pydantic import BaseModel

fake_secret_token = "coneofsilence"

class User(BaseModel):
    id: str
    username: str
    email: str

fake_users_db: dict[str, User] = {
    "user1": User(id="user1", username="user1", email="email1"),
    "user2": User(id="user2", username="user2", email="email2"),
}

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: str, x_token: Annotated[str, Header()]):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=401, detail="Invalid X-Token header")
    if user_id not in fake_users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return fake_users_db[user_id]

@app.post("/users/", response_model=User)
async def create_user(user: User, x_token: Annotated[str, Header()]):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=401, detail="Invalid X-Token header")
    if user.id in fake_users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    fake_users_db[user.id] = user
    return user

