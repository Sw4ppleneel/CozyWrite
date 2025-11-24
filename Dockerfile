FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    postgresql-client \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Use a simple shell loop instead of a separate script
CMD sh -c 'echo "Waiting for PostgreSQL..." && \
    until pg_isready -h postgres -U postgres > /dev/null 2>&1; do \
      echo "PostgreSQL is unavailable - sleeping"; \
      sleep 1; \
    done && \
    echo "PostgreSQL is ready - starting app" && \
    uvicorn CozyWrites.main:app --host 0.0.0.0 --port 8000'