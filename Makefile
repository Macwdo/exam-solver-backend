up-prod:
	docker compose -f docker-compose-prod.yml up

build:
	docker build \
	-t exam-backend \
	. 

run:
	docker run \
	-d \
	-p 8000:8000 \
	--name exam-backend \
	--network host \
	exam-backend

down:
	docker compose down

up:
	docker compose down
	docker compose up -d

attach:
	docker exec -it  exam-solver-backend-web sh

createadmin:
	docker exec -it exam-solver-backend-web sh -c "uv run manage.py createsuperuser --username admin --email admin@admin.com"
