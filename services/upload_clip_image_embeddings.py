import os
import boto3
from io import BytesIO
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
from concurrent.futures import ThreadPoolExecutor
from torch.nn.functional import normalize
from dotenv import load_dotenv
import argparse

def download_image(key, s3, bucket):
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        image_bytes = response['Body'].read()
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        return key, image
    except Exception as e:
        print(f"Erreur image {key} : {e}")
        return None

def batch_download(keys, s3, bucket, max_workers=8):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(lambda k: download_image(k, s3, bucket), keys))
    return [(k, img) for (k, img) in results if k is not None and img is not None]

def main(args):
    # Chargement des variables d'environnement
    print("Connexion au cloud")
    load_dotenv(dotenv_path=args.env_path)
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url=args.endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    
    # Chargement du modèle CLIP
    print("Chargement du modèle CLIP")
    model_name = "openai/clip-vit-base-patch32"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = CLIPModel.from_pretrained(model_name).to(device)
    processor = CLIPProcessor.from_pretrained(model_name)

    # Récupération des chemins d'images sur le bucket
    bucket = args.bucket
    paginator = s3.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket)
    jpg_files = []
    for page in page_iterator:
        if 'Contents' in page:
            for obj in page['Contents']:
                key = obj['Key']
                if key.lower().endswith('.jpg'):
                    jpg_files.append(key)

    print(f"{len(jpg_files)} images trouvées.")

    # Calcul des embeddings par batch
    batch_size = args.batch_size
    embeddings = {}
    for i in range(0, len(jpg_files), batch_size):
        batch_keys = jpg_files[i:i + batch_size]
        downloaded = batch_download(batch_keys, s3, bucket)
        if not downloaded:
            continue
        valid_keys, images = zip(*downloaded)
        inputs = processor(images=list(images), return_tensors="pt", padding=True).to(device)
        with torch.no_grad():
            image_embeds = model.get_image_features(**inputs)
            image_embeds = normalize(image_embeds, p=2, dim=1).cpu()
        for key, embedding in zip(valid_keys, image_embeds):
            embeddings[key] = embedding
        print(f"Batch {(i//batch_size)+1} OK ({i+len(batch_keys)}/{len(jpg_files)})")

    # Sauvegarde et upload des embeddings sur le bucket
    torch.save(embeddings, "clip_embeddings.pt")
    s3.upload_file("clip_embeddings.pt", bucket, Key="embeddings/clip_embeddings.pt")
    print("Embeddings sauvegardés et uploadés avec succès.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch_size', type=int, default=16, help='Taille du batch pour le calcul des embeddings')
    parser.add_argument('--env_path', type=str, default='../.env', help='Chemin vers le fichier .env')
    parser.add_argument('--bucket', type=str, default='image-search-db', help='Nom du bucket S3/R2')
    parser.add_argument('--endpoint_url', type=str, default='https://16ee9e2a9099aedfcaf86cd5a5ef621f.r2.cloudflarestorage.com', help='Endpoint S3/R2')
    args = parser.parse_args()
    main(args)
