from fastapi import FastAPI
from app.presentation.books_api import router

app = FastAPI(title="Books API")

@app.get("/")
def health():
    return {"status": "ok"}

app.include_router(router)