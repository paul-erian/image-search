import torch
from transformers import CLIPProcessor, CLIPModel
import os
from config import s3, bucket
from s3_data_loader import S3DataLoader

def load_clip(model_name="openai/clip-vit-base-patch32", local_dir="./clip_model"):
    source = local_dir if os.path.exists(local_dir) else model_name
    model = CLIPModel.from_pretrained(source).eval()
    processor = CLIPProcessor.from_pretrained(source)
    return model, processor

model, processor = load_clip()

loader = S3DataLoader(s3, bucket)
paths = loader.download(["embeddings/clip_embeddings.pt"], "../embeddings")

embeddings = torch.load("../embeddings/clip_embeddings_20000.pt")
image_paths_cloud = list(embeddings.keys())
image_features = torch.stack(list(embeddings.values())).half()
del embeddings

# recherche d'images
def search_images(text_query: str, top_k: int = 12, treshold: float = 0.2):
    with torch.no_grad():
        text_inputs = processor(text=[text_query], return_tensors="pt")
        text_features = model.get_text_features(**text_inputs).half()
        text_features /= text_features.norm(dim=-1, keepdim=True)

        logits_per_image = image_features @ text_features.T
        logits_per_image = logits_per_image.squeeze(1)

        top_k_indices = logits_per_image.topk(top_k).indices.tolist()
        results = [(image_paths_cloud[i], logits_per_image[i].item()) for i in top_k_indices if logits_per_image[i] >= treshold]
        return results
