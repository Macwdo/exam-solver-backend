up-prod:
	docker compose -f docker-compose-prod.yml up

build:
	docker buildx build \
	-t exam-backend \
	. 

run:
	docker run \
	-p 8000:8000 \
	--network host \
	--env-file .env \
	exam-backend

run-worker:
	docker run \
	--network host \
	--env-file .env \
	exam-backend \
	sh ./celery.sh

down:
	docker compose down

up:
	docker compose down
	docker compose up -d

attach:
	docker exec -it exam-solver-backend-web sh

createadmin:
	docker exec -it exam-solver-backend-web sh -c "uv run manage.py createsuperuser --username admin --email admin@admin.com"
