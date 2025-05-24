FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

RUN groupadd -g 999 appgroup && useradd -u 999 -g appgroup -m appuser

WORKDIR /app

ADD . /app
RUN uv sync

RUN chown -R appuser:appgroup /app

USER appuser
CMD ["sh", "./script.sh"]
