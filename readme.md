# image-search

## Presentation

**image-search** est un moteur de recherche d’images basé sur la similarité sémantique entre texte et image.  
Ce projet met en œuvre le modèle CLIP d’OpenAI, qui permet de comparer directement une requête textuelle et des images en les projetant dans un même espace d’embeddings.

L’objectif est de proposer une API web performante et une interface simple pour explorer la recherche d’images par description sémantique. L'application est déployée sur un instance d'AWS EC2 et est disponible à cette [adresse](http://16.171.6.178:8000/).

ajout demo

## Stack technique

- **AWS EC2** : Hébergement du serveur et déploiement de l’application dans le cloud.
- **AWS S3** : Les embeddings et les images sont stockés sur S3, avec l’API Python **Boto3** pour automatiser l’upload et le téléchargement des fichiers.
- **Docker** : Conteneurisation de l’application pour simplifier le déploiement et la reproductibilité de l’environnement.
- **transformers (Hugging Face)** : Librairie utilisée pour importer et exploiter le modèle CLIP, basée sur **PyTorch**.
- **FastAPI** : FastAPI permet de rapidement creer API web. J'y ai également ajouté du code HTML dynamiquement généré avec **Jinja2**.
- **systemd** : Gestionnaire de services Linux pour garantir la disponibilité continue de l’application sur le serveur.

## Installation et configuration

### prerequis

- git
- Un compte AWS avec accès à S3 et EC2
- Docker (optionnel mais je vous le conseil fortement :) )

### installation avec docker

1. Clonez le projet

```shell
git clone https://github.com/ton-utilisateur/image-search.git
cd image-search
```

2. Creez un fichier `.env` à la racine du projet, avec les informations d'accès à votre bucket S3.

```shell
ENDPOINT_URL=...
BUCKET_NAME=...
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
```

3. Construisez l'image docker et lancer un conteneur

```shell
docker build -t image-search .
docker run -it --env-file .env -p 8000:80 image-search bash
```

### lancement en local

Depuis votre conteneur, lancer la commande uvicorn

```shell
uvicorn main:app --host 0.0.0.0 --port 8000
```

Puis dans votre navigateur, allez à l'adresse `http://localhost:8000/`. L'application apparait !

### Déploiement sur le cloud

à faire

## Choix et détails techniques

BDD ImageNet

## à trier

```shell
docker build -t image-search .
docker run -it --env-file .env -p 8000:80 image-search bash
docker exec -it <container> bash
```

```shell
uvicorn main:app --host 0.0.0.0 --port 80
http://localhost:8000/
http://localhost:8000/search?q=blue+and+yellow+chairs
```

```shell
python upload_to_r2.py 
C:\\Users\\Paul\\Downloads\\imagenet-1k_val 
--bucket image-search-db 
--endpoint https://16ee9e2a9099aedfcaf86cd5a5ef621f.r2.cloudflarestorage.com
--access_key <access_key>
--secret_key <secret_key>
```