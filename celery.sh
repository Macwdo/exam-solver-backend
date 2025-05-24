#!/bin/sh

set -e

# Only add user if it doesn't already exist
id -u celery 2>/dev/null || adduser -D -h /home/celery celery

# Make sure .venv is owned by celery
chown -R celery:celery .venv

# Run as celery user (ensure su-exec is installed)
exec su-exec celery .venv/bin/celery -A core worker --loglevel=info --concurrency=2
