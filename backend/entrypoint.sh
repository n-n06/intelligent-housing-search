#!/bin/bash
set -e

echo "Loading environment variables..."

# Load .env and auth.env dynamically if they exist
if [ -f /app/.env ]; then
  export $(grep -v '^#' /app/.env | xargs)
fi

if [ -f /app/auth.env ]; then
  export $(grep -v '^#' /app/auth.env | xargs)
fi

echo "Waiting for PostgreSQL to be ready at ${DB_HOST}:${DB_PORT}..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" > /dev/null 2>&1; do
  sleep 1
done

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting FastAPI app..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000
