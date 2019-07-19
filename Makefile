.PHONY: venv system-packages python-packages install unit-tests tests run all

venv:
	pip install --user virtualenv
	virtualenv venv

system-packages:
	sudo apt install python-pip -y

python-packages:
	pip install -r requirements.txt
	pip install -e .

install: system-packages python-packages

unit-tests:

tests: unit-tests

run:
	python -m pa_microservice

all: install tests run
