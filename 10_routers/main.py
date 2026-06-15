from fastapi import FastAPI, Depends, Query, HTTPException
import user

app = FastAPI()

app.include_router(user.router)

@app.get("/users/")
async def get_users():
    return user.users_list

