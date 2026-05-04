from fastapi import FastAPI, Query
from typing import Annotated, Literal
from pydantic import BaseModel, Field

app = FastAPI()

class FilterParams(BaseModel):
    limit: Annotated[int, Field(ge=0, le=100)]
    offset: int
    order_by: Literal["created_at", "updated_at"] = "created_at"

@app.get("/items/")
async def read_items(params: FilterParams = Query(...)):
    """ results: dict = {"items": ["item1", "item2", "item3"]}
    if params:
        results.update({"params": params.dict()}) """

    return {"message": "Items retrieved successfully", **params.model_dump()}