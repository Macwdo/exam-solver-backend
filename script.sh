#!/bin/sh

set -e


echo "Migrating database..."
uv run manage.py migrate --noinput

echo "Collecting static files..."
uv run manage.py collectstatic --noinput

echo "Starting server..."
uv run manage.py runserver 0.0.0.0:8000 --insecure