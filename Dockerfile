FROM python:3.11-slim

WORKDIR /app


COPY requirements.txt .

RUN apt-get update && apt-get install -y gcc libpq-dev \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.app:create_app"]