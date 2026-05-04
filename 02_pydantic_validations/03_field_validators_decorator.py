from typing import Annotated
from pydantic import BaseModel, AfterValidator, field_validator

class Item(BaseModel):
    item_id: int
    price: float

    @field_validator('item_id', 'price')
    def check_item_id_positive(cls, value:int | float) -> int | float:
        if value < 0:
            raise ValueError('Item ID must be non-negative')
        return value
    
banana: Item = Item(item_id=10, price=-2.5)
print(banana)
#ejemplo_error: Item = Item(item_id=-5, price=3.0)
#print(ejemplo_error)