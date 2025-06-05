FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ app/
COPY images/ images/
COPY embeddings/ embeddings/
# COPY .env .env # à commenter sur render / decommenter en local
EXPOSE 80
WORKDIR /app/app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]