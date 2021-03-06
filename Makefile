SHELL := /bin/bash

.PHONY: clean deps docker docker-down docs flake8 githooks isort lint postgres psql pylint pycodestyle run spec test_1 test_2 test_3 test_4 test_5 test_6 tests validate-spec

.DEFAULT: help
help:
	@echo "make clean"
	@echo "    Remove all Python compile & cache files"
	@echo "make deps"
	@echo "    Install Python dependencies"
	@echo "make docker"
	@echo "    Start up Docker containers and boostrap"
	@echo "make docker-down"
	@echo "    Shut down all things Docker"
	@echo "make docs"
	@echo "    Open Swagger UI docs - use make run first"
	@echo "make flake8"
	@echo "    Run flake8 linter"
	@echo "make githooks"
	@echo "    Register git hooks dir"
	@echo "make isort"
	@echo "    Run isort linter"
	@echo "make lint"
	@echo "    Run all linters"
	@echo "make postgres"
	@echo "    Setup postgresql db"
	@echo "make psql"
	@echo "    Get a psql connection to the docker database"
	@echo "make pylint"
	@echo "    Run pylint linter"
	@echo "make pycodestyle"
	@echo "    Run pycodestyle linter"
	@echo "make run"
	@echo "    Run Flask app"
	@echo "make spec"
	@echo "    Resolve specs into a single file"
	@echo "make test_1"
	@echo "    Run the hello world test"
	@echo "make test_2"
	@echo "    Run the collection get test"
	@echo "make test_3"
	@echo "    Run the collection post test"
	@echo "make test_4"
	@echo "    Run the resource get test"
	@echo "make test_5"
	@echo "    Run the resource put test"
	@echo "make test_6"
	@echo "    Run the resource delete test"
	@echo "make tests"
	@echo "    Run all the tests"
	@echo "make validate-spec"
	@echo "    Validate openapi spec"

build:
	python setup.py sdist bdist_wheel

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -Rf {} +

deps:
	pip install -r requirements.txt

docker: docker-up postgres

docker-down:
	docker-compose down

docker-up:
	docker-compose up -d

docs:
	open http://127.0.0.1:9000/ui/

flake8:
	@echo "> running flake8..."
	@flake8 --exclude='yoyo' --max-line-length=99
	@if [ $$? != 0 ]; then exit 1; else echo "flake8 looks good!"; fi
	@echo

githooks:
	git config core.hooksPath githooks

isort:
	@echo "> running isort..."
	@isort -c
	@if [ $$? != 0 ]; then exit 1; else echo "isort looks good!"; fi
	@echo

lint: pycodestyle flake8 pylint isort validate-spec

postgres:
	sleep 10  # waiting for PG to be ready
	yoyo apply -c yoyo/dev.ini

psql:
	psql -U dev -h localhost tutorial_openapi_aiohttp

pycodestyle:
	@echo "> running pycodestyle..."
	@pycodestyle --max-line-length=99 --exclude='yoyo' .
	@if [ $$? != 0 ]; then exit 1; else echo "pycodestyle looks good!"; fi
	@echo

pylint:
	@echo "> running pylint..."
	@find . -path ./yoyo -prune -o -name '*.py' -exec pylint --rcfile=.pylintrc {} +
	@if [ $$? != 0 ] && [ $$? != 32 ]; then echo "Exit code: $$?"; exit 1; else echo "pylint looks good!"; fi
	@echo

run:
	prance compile spec/index.yaml spec/resolved.yaml
	python main.py

spec:
	prance compile spec/index.yaml spec/resolved.yaml

test_1:
	pytest tests/test_1_hello_world.py

test_2:
	pytest tests/test_2_kudos_get.py

test_3:
	pytest tests/test_3_kudos_post.py

test_4:
	pytest tests/test_4_kudo_get.py

test_5:
	pytest tests/test_5_kudo_put.py

test_6:
	pytest tests/test_6_kudo_delete.py

tests:
	pytest tests/

validate-spec:
	prance validate spec/index.yaml
