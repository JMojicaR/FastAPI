from fastapi import FastAPI, Depends, Query, HTTPException
import asyncio
from typing import Annotated

app = FastAPI()

class MockDatabase:
    def __init__(self):
        self.items: dict[str, dict] = {
            "item1": {"name": "Item 1", "price": 10.0},
            "item2": {"name": "Item 2", "price": 20.0},
        }

    async def get_data(self, key: str) -> dict:
        await asyncio.sleep(0.1)  # Simulate a delay
        if key in self.items:
            return self.items[key]
        raise HTTPException(status_code=404, detail="Key not found")

    async def set_data(self, key: str, value: dict) -> dict:
        await asyncio.sleep(0.1)  # Simulate a delay
        if key in self.items:
            raise HTTPException(status_code=400, detail="Key already exists")
        self.items[key] = value
        return value
    
async def get_db():
    bd = MockDatabase()
    yield bd


@app.get("/data/{key}")
##async def read_data(key: str, db: MockDatabase = Depends(get_db)):
async def read_data(key: str, db: Annotated[MockDatabase, Depends(get_db)]):    
    return await db.get_data(key)

@app.post("/data/")
async def update_data(data: dict, db: Annotated[MockDatabase, Depends(get_db)]):
    key = data.get("key")
    value = data.get("value")
    if not key or not value:
        raise HTTPException(status_code=400, detail="Key and value are required")
    return await db.set_data(key, value)