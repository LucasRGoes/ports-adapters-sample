.PHONY: venv system-packages python-packages install unit-tests tests run all

venv:
	pip install --user virtualenv
	virtualenv venv

system-packages:
	sudo apt install python-pip -y

python-packages:
	pip install -r requirements.txt

install: system-packages python-packages

unit-tests:

tests: unit-tests

run:
	@python -m app

all: install tests run
