# image-search

```shell
docker build -t image-search .
docker run -it -p 8000:80 image-search bash
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

## TODO

- [ ] récupération des images depuis cloudflare R2
- [ ] descriptif du nombres d'image matchées après recherche
- [ ] sauvegarder les images embeddings sur cloud
- [ ] charger CLIP en local ?
- [ ] replacer CLIP (adapaté au ranking) par BLIP-2 (adapté au matching)
