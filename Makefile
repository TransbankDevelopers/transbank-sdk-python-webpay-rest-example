SHELL := /bin/bash

all: build run

run: build
	docker-compose run --rm --service-ports web

build: .built .pipped

.built: Dockerfile
	docker-compose build
	touch .built

.pipped: requirements.txt
	docker-compose run web pip install -r requirements.txt
	touch .pipped

logs:
	docker-compose logs

clean:
	docker-compose rm
	rm .built
	rm .pipped
