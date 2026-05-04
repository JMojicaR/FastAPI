from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/index", response_class=HTMLResponse)
async def read_index():
    return templates.TemplateResponse("index.html", {"request": {}})