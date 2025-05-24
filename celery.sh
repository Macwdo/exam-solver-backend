#!/bin/sh

set -e

useradd -ms .venv/bin/celery
chown -R celery:celery .venv
uv run celery -A core worker --loglevel=info --concurrency=2