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

## TODO

- [ ] suppression softmax + facteur exp
- [ ] récupération des images depuis cloudflare R2
- [ ] descriptif du nombres d'image matchées après recherche
- [ ] sauvegarder les images embeddings sur cloud
- [ ] charger CLIP en local ?
