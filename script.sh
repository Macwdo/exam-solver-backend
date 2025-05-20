#!/bin/sh

set -e


echo "Migrating database..."
uv run manage.py migrate --noinput

echo "Collecting static files..."
uv run manage.py collectstatic --noinput

echo "Starting server..."
uv run gunicorn core.wsgi -c gunicorn.py 