#!/bin/sh

echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 1
done

echo "Applying migrations..."
cd src && alembic upgrade head

echo "Starting application..."
exec fastapi run main.py --port 8000