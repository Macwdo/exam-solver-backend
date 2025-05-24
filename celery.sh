#!/bin/sh
uv run celery -A core worker --loglevel=info --concurrency=2