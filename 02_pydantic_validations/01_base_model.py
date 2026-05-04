from fastapi import FastAPI
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True
    age: int | None = None

class UserResponse(BaseModel):
    mensaje: str
    datos: User

app = FastAPI()

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    return User(id=user_id, name="John Doe", email="john.doe@example.com")

@app.post("/users/", response_model=UserResponse)
async def create_user(user: User):
    return {
        "mensaje": f"Usuario {user.name.capitalize()} creado con éxito",
        "datos": user
    }

@app.put("/users/{user_id}")
async def update_user(user_id: int, user: User, q: str | None = None):
    result: dict = {"user_id": user_id, **user.model_dump()}
    if q:
        result.update({"q": q})
    return result