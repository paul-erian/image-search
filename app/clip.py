import torch
from transformers import CLIPProcessor, CLIPModel
import os
import boto3
from dotenv import load_dotenv

# chargement de CLIP
print("Chargement du modèle CLIP")
model_name = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_name).eval()
processor = CLIPProcessor.from_pretrained(model_name)

# connexion cloud 
print("Connexion au cloud")
load_dotenv(dotenv_path="../.env")
endpoint_url = "https://16ee9e2a9099aedfcaf86cd5a5ef621f.r2.cloudflarestorage.com"
bucket = "image-search-db"
access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url=endpoint_url,
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
)

# chargement des embeddings
if not os.path.exists("clip_embeddings.pt"):
    print("Téléchargement des embeddings depuis le cloud")
    s3.download_file(bucket, "embeddings/clip_embeddings.pt", "clip_embeddings.pt")
print("Chargement des embeddings")
embeddings = torch.load("clip_embeddings.pt")
image_paths_cloud = list(embeddings.keys())
image_features = torch.stack(list(embeddings.values()))

# recherche d'images
def search_images(text_query: str, top_k: int = 5, treshold: float = 0.3):
    with torch.no_grad():
        text_inputs = processor(text=[text_query], return_tensors="pt")
        text_features = model.get_text_features(**text_inputs)
        text_features /= text_features.norm(dim=-1, keepdim=True)

        logits_per_image = image_features @ text_features.T
        logits_per_image = logits_per_image.squeeze(1)

        top_k_indices = logits_per_image.topk(top_k).indices.tolist()
        results = [(image_paths_cloud[i], logits_per_image[i].item()) for i in top_k_indices if logits_per_image[i] >= treshold]
        return results

def dowload_images_from_r2(image_paths_cloud):
    for cloud_path in image_paths_cloud:
        local_path = os.path.join("../images", os.path.basename(cloud_path))
        s3.download_file(Bucket=bucket, Key=cloud_path, Filename=local_path)
        print(f"Téléchargement {cloud_path} vers {local_path}")
