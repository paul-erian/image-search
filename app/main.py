# app/main.py
import os
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from clip import search_images

app = FastAPI()
app.mount("/images", StaticFiles(directory=os.path.abspath("../images")), name="images")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/search", response_class=HTMLResponse)
def search_endpoint(q: str = Query(..., description="Description de la recherche"), k: int = 5):
    results = search_images(q, top_k=k)
    html = """
    <html>
        <head><title>Results</title></head>
        <body>
            <h1>Results for: {}</h1>
            <a href="/">Back to search</a>
            <ul>
    """.format(q)
    for path, score in results:
        # Extract filename for URL
        filename = os.path.basename(path)
        html += f'<li><img src="/images/{filename}" width="256"/><br>Score: {score:.3f}</li>'
    html += """
            </ul>
        </body>
    </html>
    """
    return html