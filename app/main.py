# app/main.py
import os
import torch
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from clip_utils import load_clip
from config import s3_embeddings_dir, model_name, embeddings_dir, embeddings_name, clip_path, image_dir, start_top_k, start_treshold, s3, bucket
from s3_data_downloader import S3DataDownloader
from clip_image_searcher import ClipImageSearcher

print("telechargement des embeddings image depuis s3 ...")
downloader = S3DataDownloader(s3, bucket)
downloader.download([os.path.join(s3_embeddings_dir, embeddings_name)], embeddings_dir)

print("chargement des embeddings image dans la RAM ...")
embeddings = torch.load(os.path.join(embeddings_dir, embeddings_name))
s3_image_paths = list(embeddings.keys())
image_features = torch.stack(list(embeddings.values())).half()
del embeddings

print("chargement clip ...")
model, processor = load_clip(model_name=model_name, local_dir=clip_path)
clip_image_searcher = ClipImageSearcher(model=model,
                                        processor=processor,
                                        image_features=image_features,
                                        s3_image_paths=s3_image_paths)

app = FastAPI()
app.mount("/images", StaticFiles(directory=os.path.abspath(image_dir)), name="images")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
        return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "k": start_top_k,
            "t": start_treshold
        }
    )

@app.get("/search", response_class=HTMLResponse)
def search_endpoint(request: Request,  k: int, t: float, q: str=Query(..., description="Description de la recherche")):
    results = clip_image_searcher.search(q, top_k=k, treshold=t)
    s3_images_to_donwload = [path for path, _ in results]
    downloader.download(s3_images_to_donwload, image_dir)
    return templates.TemplateResponse("results.html", {
        "request": request,
        "q": q,
        "k": k,
        "t": t,
        "results": [{"filename": os.path.basename(path), "score": score} for path, score in results]
    })
