#!/bin/sh
set -e

adduser -D -h /home/celery celery
chown -R celery:celery /app
exec su-exec celery uv run celery -A core worker --loglevel=info --concurrency=2