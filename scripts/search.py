import argparse
import pickle
from pathlib import Path

import numpy as np
import torch
from transformers import CLIPModel, CLIPProcessor


class Searcher:
    def __init__(self, embeddings_path: Path)->None:
        # Chargement du modèle CLIP
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        model_name = "openai/clip-vit-base-patch32"
        self.model = CLIPModel.from_pretrained(model_name).to(self.device).eval()
        self.processor = CLIPProcessor.from_pretrained(model_name)
        
        # Chargement des embeddings
        with open(embeddings_path, 'rb') as f:
            embeddings = pickle.load(f)
        image_features = np.array(list(embeddings.values()))
        self.image_features = torch.tensor(image_features).to(self.device)
        self.image_paths = list(embeddings.keys())

    def search(self, text_query: str, top_k: int)->list:
        """Recherche les images les plus similaires à une requête textuelle."""
        with torch.no_grad():
            # Calcul des embeddings du texte
            text_inputs = self.processor(text=[text_query], return_tensors="pt").to(self.device)
            text_features = self.model.get_text_features(**text_inputs)
            text_features = text_features.pooler_output
            text_features /= text_features.norm(dim=-1, keepdim=True)

            # Calcul des similarités cosinus
            logits = self.image_features @ text_features.T
            logits = logits.squeeze()

            # Récupération des top_k résultats
            top_indices = logits.topk(top_k).indices.tolist()
            results = [(self.image_paths[i], logits[i].item()) for i in top_indices]
            return results


if __name__=="__main__":
    parser = argparse.ArgumentParser(
        description="Rechercher les images les plus similaires à une requête textuelle")
    parser.add_argument('--embeddings', type=Path, required=True,
                        help='Fichier .pkl contenant les embeddings')
    parser.add_argument('--query', type=str, required=True, help='Requête textuelle')
    parser.add_argument('--top-k', type=int, default=5, help='Nombre de résultats à afficher')
    args = parser.parse_args()

    searcher = Searcher(args.embeddings)
    results = searcher.search(args.query, args.top_k)
    for i, (image_path, score) in enumerate(results):
        print(f"{i+1}. {image_path} ({score:.4f})")
