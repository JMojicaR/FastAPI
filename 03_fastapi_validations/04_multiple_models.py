from fastapi import Body, FastAPI
from typing import Annotated
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class User(BaseModel):
    username: str
    full_name: str | None = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results

@app.put("/items2/{item_id}")
async def update_item(item_id: int, item: Item, user: User, priority: Annotated[int, Body()] = 1):
    results = {"item_id": item_id, "item": item, "user": user, "priority": priority}
    return results