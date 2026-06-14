from fastapi import FastAPI, Depends, Query, HTTPException
import time
import asyncio

app = FastAPI()

@app.get("/async-sin-await")
async def async_sin_await():
    print("Hola")
    time.sleep(5)
    return {"message": "Adios"}

@app.get("/async-con-await")
async def async_con_await():
    print("Hola2")
    await asyncio.sleep(5)
    return {"message": "Adios2"}

@app.get("/sync")
def sync():
    print("Hola3")
    time.sleep(5)
    return {"message": "Adios3"}