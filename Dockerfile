FROM ghcr.io/astral-sh/uv:python3.12-alpine

ADD . /app
WORKDIR /app

RUN uv sync
RUN apk add --no-cache su-exec

COPY . .

CMD ["sh", "./script.sh"]