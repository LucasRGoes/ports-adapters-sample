.PHONY: venv system-packages python-packages install unit-tests integration-tests tests run all

venv:
	pip install --user virtualenv
	virtualenv venv

system-packages:
	sudo apt install python-pip -y

python-packages:
	pip install -r requirements.txt

install: system-packages python-packages

unit-tests:
	python -m unittest tests.test_domain_ports \
					   tests.test_database_memory \
					   tests.test_database_sqlite \
					   tests.test_sender_mqtt

integration-tests:
	python -m unittest tests.test_handlers \
					   tests.test_interface_mqtt \
					   tests.test_interface_flask

tests: unit-tests integration-tests

run:
	@python -m app

all: install tests run
