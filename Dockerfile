FROM python:3.11-slim

WORKDIR /app

# Limpiar caché de Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN apt-get update && apt-get install -y gcc libpq-dev \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

# Limpiar archivos .pyc
RUN find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.app:create_app"]