# image-search

```shell
docker build -t image-search .
docker run -it -w /app -p 8000:80 image-search bash
docker exec -it <container> bash
```

```shell
uvicorn main:app --host 0.0.0.0 --port 80
http://localhost:8000/
```
