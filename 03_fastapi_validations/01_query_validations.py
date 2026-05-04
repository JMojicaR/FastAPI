from fastapi import FastAPI, Query
from typing import Annotated
from pydantic import AfterValidator

app = FastAPI()
#STRINGS
#max_length, min_length, pattern

#NUMBERS
#gt, ge, lt, le

#LISTS
#max_items, min_items, unique_items

#METADATA
#description, 
#title
#alias
#deprecated

def check_valid_id(id: str):
    if id % 2 != 0:
        raise ValueError("El id debe ser un número par")
    return id

@app.get("/items/")
async def read_items(q: Annotated[list[str] | None, Query(title="Query", description="What is searching for", alias="item-query")] = None):
    results: dict = {"items": ["item1", "item2", "item3"]}
    if q:
        results.update({"q": q})

    return results

@app.get("/items2/")
async def read_items(q: Annotated[int | None, AfterValidator(check_valid_id)] = None):
    results: dict = {"items": ["item1", "item2", "item3"]}
    if q:
        results.update({"q": q})

    return results