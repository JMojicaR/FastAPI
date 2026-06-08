from typing import Callable
from fastapi import FastAPI, Request, Response
import time

app = FastAPI()

# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next: Callable):
#     start_time = time.perf_counter()
#     response = await call_next(request)
#     process_time = time.perf_counter() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response

@app.middleware("http")
async def first_middleware(request: Request, call_next: Callable):
    print("First middleware - before request")
    response = await call_next(request)
    print("First middleware - after request")
    return response

@app.middleware("http")
async def second_middleware(request: Request, call_next: Callable):
    print("Second middleware - before request")
    response = await call_next(request)
    print("Second middleware - after request")
    return response

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/slow")
async def slow_route():
    time.sleep(5)
    return {"message": "This was a slow response"}