from fastapi import FastAPI
from enum import Enum

class CarDealer(Enum):
    TOYOTA = "Toyota"
    FORD = "Ford"
    HONDA = "Honda"

app = FastAPI()

@app.get("/models/{car_dealer}")
async def get_model(car_dealer: CarDealer):
    if car_dealer == CarDealer.TOYOTA:
        return {"model": "Corolla"}
    elif car_dealer == CarDealer.FORD:
        return {"model": "Mustang"}
    elif car_dealer == CarDealer.HONDA:
        return {"model": "Civic"}
    return {"model": "Unknown"}