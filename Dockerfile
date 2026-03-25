FROM python:3.14-slim

# installation uv
WORKDIR /app
RUN pip install --no-cache-dir uv

# installation et activation de l'env
COPY pyproject.toml uv.lock ./
RUN uv sync

# mapping des volumes
COPY app/ app/
COPY images/ images/
COPY embeddings/ embeddings/

# lancement de l'application
WORKDIR /app/app
EXPOSE 80
CMD ["/app/.venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]