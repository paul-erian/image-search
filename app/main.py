# app/main.py
from fastapi import FastAPI, Query
from clip import search_images

app = FastAPI()

@app.get("/search")
def search_endpoint(q: str = Query(..., description="Description de la recherche"), k: int = 5):
    results = search_images(q, top_k=k)
    return {"query": q, "results": [{"image_path": path, "score": score} for path, score in results]}