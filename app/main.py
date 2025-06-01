# app/main.py
import os
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from clip import search_images

app = FastAPI()

app.mount("/images", StaticFiles(directory=os.path.abspath("../images")), name="images")

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Image Search</title>
        </head>
        <body>
            <h1>Image Search</h1>
            <form action="/search" method="get">
                <input type="text" name="q" placeholder="Enter your search..." required>
                <input type="number" name="k" value="5" min="1" max="20">
                <button type="submit">Search</button>
            </form>
        </body>
    </html>
    """

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