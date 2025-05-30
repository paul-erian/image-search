import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import os

# chargement de CLIP
model_name = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_name).eval()
processor = CLIPProcessor.from_pretrained(model_name)

# chargement des images
image_dir = "../images"
image_paths = [os.path.join(image_dir, f) for f in os.listdir(image_dir)]
images = [Image.open(p).convert("RGB") for p in image_paths]

# chargements embeddings d'images (#TODO: precompute embeddings)
with torch.no_grad():
    image_inputs = processor(images=images, return_tensors="pt", padding=True)
    image_features = model.get_image_features(**image_inputs)
    image_features /= image_features.norm(dim=-1, keepdim=True)

# recherche d'images
def search_images(text_query: str, top_k: int = 5):
    with torch.no_grad():
        text_inputs = processor(text=[text_query], return_tensors="pt")
        text_features = model.get_text_features(**text_inputs)
        text_features /= text_features.norm(dim=-1, keepdim=True)

        similarities = image_features @ text_features.T  # shape (N, 1)
        similarities = similarities.squeeze(1)

        top_k_indices = similarities.topk(top_k).indices.tolist()
        results = [(image_paths[i], similarities[i].item()) for i in top_k_indices]
        return results
