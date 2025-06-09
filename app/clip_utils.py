from transformers import CLIPProcessor, CLIPModel
import os

def load_clip(model_name="openai/clip-vit-base-patch32", local_dir="./clip_model"):
    """Téléchargement de CLIP dans un dossier local (si pas deja present)."""
    source = local_dir if os.path.exists(local_dir) else model_name
    model = CLIPModel.from_pretrained(source).eval()
    processor = CLIPProcessor.from_pretrained(source)
    return model, processor
