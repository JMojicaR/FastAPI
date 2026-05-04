from fastapi import FastAPI

app = FastAPI()

cars_list: list[dict] = [
    {"car_name": "Elantra"},
    {"car_name": "Sonata"},
    {"car_name": "Tucson"},
    {"car_name": "Santa Fe"},
]

@app.get("/cars/")
async def read_cars(skip: int = 0, limit: int = 10, optional: str | None = None):
    if optional:
        return {
            "message": f"Optional parameter received: {optional}",
            "list": cars_list[skip : skip + limit] 
            }
    return cars_list[skip : skip + limit]