"""Integration tests of the application's handlers.py functions."""

import time
import unittest
import threading

import paho.mqtt.subscribe as subscribe

from app.domain.model import Book
from app.domain.ports import MessageBus
from app.adapters.mqtt import MqttSender
from app.adapters.memory import MemoryDatabase
from app.handlers import RegisterBookHandler, BookRegisteredHandler
from app.domain.messages import RegisterBookCommand, BookRegisteredEvent


class MockSubscriber(object):
	def __init__(self):
		self.topic = ''
		self.payload = ''

	def wait_event(self):
		msg = subscribe.simple('tests/event')

		self.topic = msg.topic
		self.payload = str(msg.payload.decode('utf8'))


class TestRegisterBookHandler(unittest.TestCase):
	"""Set of integration tests for the handlers.py RegisterBookHandler class
	and its implementations.

	Tests: test_handle
	"""
	def test_handle(self):
		"""Steps:
		1 - Instantiates a RegisterBookHandler
		2 - Handles command and verifies if the book has been registered
		"""
		memory = MemoryDatabase({})
		memory.set_up()

		handler = RegisterBookHandler(MessageBus(), memory.get_uowm())
		handler.handle(
			RegisterBookCommand('isbn', 'name', 'author', 'content'))

		book = memory.get_view().get_by_isbn('isbn')

		self.assertEqual(book.isbn, 'isbn')
		self.assertEqual(book.name, 'name')
		self.assertEqual(book.author, 'author')
		self.assertEqual(book.content, 'content')


class TestBookRegisteredHandler(unittest.TestCase):
	"""Set of integration tests for the handlers.py BookRegisteredHandler class
	and its implementations.

	Tests: test_handle
	"""
	def test_handle(self):
		"""Steps:
		1 - Instantiates a RegisterBookHandler
		2 - Instantiates a BookRegisteredHandler
		3 - Subscribe them to a bus
		2 - Handles event and verifies if the message has been published
		"""
		bus = MessageBus()

		memory = MemoryDatabase({})
		memory.set_up()

		sender = MqttSender(
			{'topic': 'tests/event', 'host': 'localhost', 'port': 1883,
			 'username': None, 'password': None}
		)

		bus.subscribe(RegisterBookCommand,
					  RegisterBookHandler(bus, memory.get_uowm()))
		bus.subscribe(BookRegisteredEvent,
					  BookRegisteredHandler(memory.get_view(), sender))

		subscriber = MockSubscriber()
		t = threading.Thread(target=subscriber.wait_event)
		t.start()
		time.sleep(0.1)

		bus.handle(RegisterBookCommand('isbn', 'name', 'author', 'content'))
		t.join()

		self.assertIn(subscriber.topic, 'tests/event')
		self.assertIn(
			subscriber.payload,
			'{0} has been successfully registered.'.format(
				Book('isbn', 'name', 'author', 'content').__repr__()
			)
		)


if __name__ == '__main__':
	unittest.main()
