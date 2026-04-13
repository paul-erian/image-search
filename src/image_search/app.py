from pathlib import Path

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .searcher import Searcher


def create_app(embeddings_path: Path, image_dir: Path) -> FastAPI:
    # Creation de l'application et montage du dossier d'images et des templates
    app = FastAPI()
    app.mount("/images", StaticFiles(directory=image_dir), name="images")
    templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

    # Initialisation du searcher
    searcher = Searcher(embeddings_path)

    # Page d'acceuil pour la recherche
    @app.get("/", response_class=HTMLResponse)
    def home(request: Request):
        return templates.TemplateResponse(
            request=request,
            name="home.html",
            context={
                "request": request,
                "k": 9,
                "t": 0.20,
                "git_url": "https://github.com/paul-erian/image-search/"
            }
        )

    # Page d'affichage des resultats de la recherche
    @app.get("/search", response_class=HTMLResponse)
    def search_endpoint(request: Request,
                        k: int,
                        t: float,
                        q: str=Query(..., description="Description de la recherche")):
        
        results = searcher.search(q, top_k=k)
        results = [{"filename": Path(path).name, "score": score} for path, score in results]

        return templates.TemplateResponse(
            request=request,
            name="results.html",
            context={
                "request": request,
                "q": q,
                "k": k,
                "t": t,
                "git_url": "https://github.com/paul-erian/image-search/",
                "results": results
            }
        )
    
    return app
