FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN apt-get update && \
    apt-get upgrade && \
    apt-get install --no-install-recommends -y curl && \
    pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir && \
    rm -rf /var/lib/apt/lists/*

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
