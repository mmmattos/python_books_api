from fastapi import FastAPI
from app.presentation.books_api import router

app = FastAPI(title="Books API")

app.include_router(router)

@app.get("/")
def health():
    return {"status": "ok"}