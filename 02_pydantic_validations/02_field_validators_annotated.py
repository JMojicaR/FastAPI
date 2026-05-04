### ANOTATED
from typing import Annotated
from pydantic import BaseModel, AfterValidator

# Types of Validators available in Pydantic
# - BeforeValidator: Used to validate before standard validation/transformation
# - AfterValidator: Used to validate after standard validation/transformation
# - WrapValidator: Used to wrap around the standard validation/transformation
# - PlainValidator: Used for simple validation without transformation

### Example of using Annotated with Pydantic validators
#x: Annotated[int, "This is an integer"] = 5

def is_even(value: int) -> int:
    if value % 2 != 0:
        raise ValueError(f"Value {value} must be even")
    return value

NummeroPar = Annotated[int, AfterValidator(is_even)]

class Model1(BaseModel):
    numero_par: NummeroPar

#ejemplo: Model1 = Model1(numero_par=3)

class Model2(BaseModel):
    other_number: Annotated[NummeroPar, AfterValidator(lambda v: v + 2)]

#ejemplo2: Model2 = Model2(other_number=4)
#print(ejemplo2)

class Model3(BaseModel):
    lista_pares: list[NummeroPar]

ejemplo3: Model3 = Model3(lista_pares=[2, 4, 6])
print(ejemplo3)