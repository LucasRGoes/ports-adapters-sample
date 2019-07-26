"""Integration tests of the application's mqtt.py functions."""

import warnings
from gevent import monkey
with warnings.catch_warnings():
	warnings.simplefilter('ignore')
	monkey.patch_all()


import unittest

import requests

from app.domain.model import Book
from app.domain.ports import MessageBus
from app.handlers import RegisterBookHandler
from app.adapters.flask import FlaskInterface
from app.adapters.memory import MemoryDatabase
from app.domain.messages import RegisterBookCommand


class TestAdaptersFlaskInterface(unittest.TestCase):
	"""Set of integration tests for the flask.py FlaskInterface class
	and its implementations.

	Tests: test_run
	"""
	def test_run(self):
		"""Steps:
		1 - Instantiates a FlaskInterface
		2 - Sends HTTP request and verify if a new book has been registered
		"""
		bus = MessageBus()

		memory = MemoryDatabase({})
		memory.set_up()
		view = memory.get_view()

		bus.subscribe(RegisterBookCommand,
					  RegisterBookHandler(bus, memory.get_uowm()))

		flask = FlaskInterface({'host': '0.0.0.0', 'port': 5000})
		flask.set_message_bus(bus)
		flask.set_view(view)
		flask.run()

		requests.post('http://localhost:5000/books',
					  json={'isbn': 'isbn', 'name': 'name', 'author': 'author',
					  		'content': 'content'})

		self.assertEqual(Book('isbn', 'name', 'author', 'content'),
						 view.get_by_isbn('isbn'))
		flask.stop()


if __name__ == '__main__':
	unittest.main()
