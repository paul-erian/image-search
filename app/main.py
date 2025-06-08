# app/main.py
import os
import torch
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.clip_utils import load_clip
from config import s3, bucket
from s3_data_loader import S3DataLoader
from clip_image_searcher import ClipImageSearcher

print("telechargement des embeddings image depuis s3 ...")
loader = S3DataLoader(s3, bucket)
loader.download(["embeddings/clip_embeddings.pt"], "../embeddings")

print("chargement des embeddings image dans la RAM ...")
embeddings = torch.load("../embeddings/clip_embeddings_20000.pt")
s3_image_paths = list(embeddings.keys())
image_features = torch.stack(list(embeddings.values())).half()
del embeddings

print("chargement clip ...")
model, processor = load_clip(model_name="openai/clip-vit-base-patch32", local_dir="./clip_model")
clip_image_searcher = ClipImageSearcher(model=model,
                                        processor=processor,
                                        image_features=image_features,
                                        s3_image_paths=s3_image_paths)

app = FastAPI()
app.mount("/images", StaticFiles(directory=os.path.abspath("../images")), name="images")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/search", response_class=HTMLResponse)
def search_endpoint(request: Request, q: str = Query(..., description="Description de la recherche"), k: int = 12, t: float = 0.2):
    results = clip_image_searcher.search(q, top_k=k, treshold=t)
    s3_images_to_donwload = [path for path, _ in results]
    loader.download(s3_images_to_donwload, "../images")
    return templates.TemplateResponse("results.html", {
        "request": request,
        "q": q,
        "k": k,
        "t": t,
        "results": [{"filename": os.path.basename(path), "score": score} for path, score in results]
    })
