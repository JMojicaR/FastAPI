from fastapi import FastAPI

app = FastAPI()

@app.get("/books/favorite")
async def read_favorite_book():
    return {"book": "The Great Gatsby"}

@app.get("/books/{book_id}")
async def read_item(book_id: int):
    return {"book_id": book_id}