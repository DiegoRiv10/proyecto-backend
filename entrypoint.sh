#!/bin/sh
set -e

echo "Esperando la base de datos..."
sleep 5

echo "Ejecutando migraciones de Alembic..."
alembic upgrade head

echo "Levantando la API..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
