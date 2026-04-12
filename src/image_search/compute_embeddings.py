import pickle
from pathlib import Path

import torch
from PIL import Image
from torch.nn.functional import normalize
from tqdm import tqdm
from transformers import CLIPModel, CLIPProcessor


def compute_embeddings(image_dir: Path, output_dir: Path, image_format: str)->None:
    """Calcule les embeddings CLIP pour les images d'un répertoire
       et les sauvegarde dans un fichier .pt."""
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Chargement du modèle CLIP
    model_name = "openai/clip-vit-base-patch32"
    model = CLIPModel.from_pretrained(model_name).to(device).eval()
    processor = CLIPProcessor.from_pretrained(model_name)

    # Chemins
    input_dir = Path(image_dir)
    image_paths = list(input_dir.rglob("*." + image_format))
    output_dir.mkdir(parents=True, exist_ok=True)
    file_name = f"{model_name.replace('/', '_')}_{image_dir.name}.pkl"
    output_path = output_dir / file_name

    # Calcul des embeddings
    embeddings = {}
    for image_path in tqdm(image_paths[:100], desc="Computing embeddings"):
        image = Image.open(image_path).convert("RGB")
        inputs = processor(images=image, return_tensors="pt", padding=True).to(device)

        with torch.no_grad():
            image_features = model.get_image_features(**inputs)
            image_features = image_features.pooler_output # (batch_size, embedding_dim)
            image_features = normalize(image_features, p=2, dim=-1)
            embeddings[image_path] = image_features.cpu().numpy()

    with open(output_path, 'wb') as f:
        pickle.dump(embeddings, f)
