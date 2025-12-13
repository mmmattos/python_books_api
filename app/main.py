from fastapi import FastAPI

app = FastAPI(title="Sanity Check API")

@app.get("/")
def health():
    return {"status": "ok"}