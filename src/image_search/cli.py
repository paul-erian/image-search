import shutil
from pathlib import Path

import typer
from tqdm import tqdm
from typer import Argument, Option

from .compute_embeddings import compute_embeddings
from .searcher import Searcher

app = typer.Typer()


@app.command()
def search(embeddings: Path = Argument(
           ..., help="Fichier .pkl contenant les chemins vers les images et les embeddings"),
           query: str = Argument(..., help="Requête textuelle"),
           top_k: int = Option(5, help="Nombre de résultats à afficher")):
    """Recherche les images qui correspondent le plus à une description textuelle."""
    # Recherche
    searcher = Searcher(embeddings)
    results = searcher.search(query, top_k)

    # Affichage des résultats
    for i, (image_path, score) in enumerate(results):
        print(f"{i+1}. {image_path} ({score:.4f})")


@app.command()
def precompute(image_dir: Path = Argument(..., help="Répertoire contenant les images"),
               output_dir: Path = Argument(..., help="Chemin de sortie pour les embeddings"),
               image_format: str = Option("JPEG", help="Format des images")):
    """Calcule les embeddings CLIP d'un repertoire d'images et les sauvegarde au format .pkl."""
    compute_embeddings(image_dir, output_dir, image_format)


@app.command()
def prepare_data(input_dir: Path = Argument(..., help="Répertoire d'entrée à aplatir"),
                 output_dir: Path = Argument(..., help="Répertoire de sortie")):
    """Copie tous les fichiers d'une arborescence dans un répertoire unique."""   
    # Chemins
    output_dir.mkdir(parents=True, exist_ok=True)
    image_paths = [p for p in input_dir.rglob("*") if p.is_file()]

    # Copie des fichiers
    for image_path in tqdm(image_paths, desc="Flattening dataset"):
        output_path = output_dir / image_path.name
        shutil.copy2(image_path, output_path)
