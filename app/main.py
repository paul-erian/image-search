# app/main.py
import os
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from clip import search_images, dowload_images_from_r2

app = FastAPI()
app.mount("/images", StaticFiles(directory=os.path.abspath("../images")), name="images")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/search", response_class=HTMLResponse)
def search_endpoint(request: Request, q: str = Query(..., description="Description de la recherche"), k: int = 5, t: float = 0.3):
    results = search_images(q, top_k=k, treshold=t)
    image_paths_cloud = [path for path, _ in results]
    dowload_images_from_r2(image_paths_cloud)
    return templates.TemplateResponse("results.html", {
        "request": request,
        "q": q,
        "k": k,
        "t": t,
        "results": [{"filename": os.path.basename(path), "score": score} for path, score in results]
    })
