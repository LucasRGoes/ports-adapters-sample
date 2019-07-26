"""Integration tests of the application's mqtt.py functions."""

import json
import time
import unittest

import paho.mqtt.publish as publish

from app.domain.model import Book
from app.domain.ports import MessageBus
from app.adapters.mqtt import MqttInterface
from app.handlers import RegisterBookHandler
from app.adapters.memory import MemoryDatabase
from app.domain.messages import RegisterBookCommand


class TestAdaptersMqttInterface(unittest.TestCase):
	"""Set of integration tests for the mqtt.py MqttInterface class
	and its implementations.

	Tests: test_run
	"""
	def test_run(self):
		"""Steps:
		1 - Instantiates a MqttInterface
		2 - Sends MQTT command and verify if a new book has been registered
		"""
		bus = MessageBus()

		memory = MemoryDatabase({})
		memory.set_up()
		view = memory.get_view()

		bus.subscribe(RegisterBookCommand,
					  RegisterBookHandler(bus, memory.get_uowm()))

		mqtt = MqttInterface(
			{'topic': 'tests/book/#', 'host': 'localhost', 'port': 1883,
			 'username': None, 'password': None})
		mqtt.set_message_bus(bus)
		mqtt.set_view(view)
		mqtt.run()

		publish.single(
			'tests/book/register',
			payload=json.dumps({'isbn': 'isbn', 'name': 'name',
							    'author': 'author', 'content': 'content'})
		)
		time.sleep(0.1)

		self.assertEqual(Book('isbn', 'name', 'author', 'content'),
						 view.get_by_isbn('isbn'))
		mqtt.stop()


if __name__ == '__main__':
	unittest.main()
