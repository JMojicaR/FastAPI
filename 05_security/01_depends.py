from fastapi import Depends, FastAPI, HTTPException, status
from typing import Annotated

app = FastAPI()

class logger:
    def log(self, message: str) -> None:
        print(message)

def get_logger():
    return logger()

logger_dependency = Annotated[logger, Depends(get_logger)]

@app.get("/items/{message}")
def read_item(message: str, log: logger_dependency):
    log.log(message)
    return {"message": message}

@app.get("/items2/{message}")
def read_item2(message: str, log: logger_dependency):
    log.log(message)
    return {"message": message}