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
	docker compose -f docker-compose-prod.yml down

up:
	docker compose -f docker-compose-prod.yml down
	docker compose -f docker-compose-prod.yml up

