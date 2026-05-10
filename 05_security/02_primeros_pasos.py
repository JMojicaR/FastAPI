# OAuth2
# OAuth1
# OpenID Connect
# OpenID
# OpenAPI
# JWT

# OAuth2 flujo de password +  Bearer token
# Frontend(username+password) -> /token -> return token

from fastapi import Depends, FastAPI, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/items/")
async def get_items(token: Annotated[str, Depends(oauth2_scheme)]):
    #if token != "secrettoken":
    #    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return {"token": token}