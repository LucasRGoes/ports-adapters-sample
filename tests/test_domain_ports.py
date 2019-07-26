"""Unit tests of the application's ports.py functions."""

import unittest

from app.domain.ports import MessageBus
from app.domain.errors import CommandAlreadySubscribedError
from app.domain.messages import RegisterBookCommand, BookRegisteredEvent


class MockHandler(object):
	def __init__(self):
		self.triggered = False

	def handle(self, msg):
		self.triggered = True


class TestDomainPortsMessageBus(unittest.TestCase):
	"""Set of unit tests for the ports.py MessageBus class and its
	implementations.

	Tests: test_handle, test_subscribe
	"""
	def test_handle(self):
		"""Steps:
		1 - Instantiates a MessageBus
		2 - Subscribes one mock command handler and two mock event handlers
		3 - Handles command and verifies behavior
		4 - Handles event and verifies behavior
		"""
		bus = MessageBus()
		
		MockCommandHandler1 = MockHandler()
		MockEventHandler1 = MockHandler()
		MockEventHandler2 = MockHandler()

		bus.subscribe(RegisterBookCommand, MockCommandHandler1)
		bus.subscribe(BookRegisteredEvent, MockEventHandler1)
		bus.subscribe(BookRegisteredEvent, MockEventHandler2)

		bus.handle(RegisterBookCommand('isbn', 'name', 'author', 'content'))
		self.assertTrue(MockCommandHandler1.triggered)

		bus.handle(BookRegisteredEvent('isbn'))
		self.assertTrue(MockEventHandler1.triggered)
		self.assertTrue(MockEventHandler2.triggered)

	def test_subscribe(self):
		"""Steps:
		1 - Instantiates a MessageBus
		2 - Subscribes one mock command handler and two mock event handlers
		and verifies subscriber list
		3 - Tries to subscribe two handlers to the same command and verifies
		if it raises the expected error
		"""
		bus = MessageBus()

		bus.subscribe(RegisterBookCommand, 'MockCommandHandler1')
		bus.subscribe(BookRegisteredEvent, 'MockEventHandler1')
		bus.subscribe(BookRegisteredEvent, 'MockEventHandler2')

		self.assertTrue(bus.subscribers.get('RegisterBookCommand') is not None)
		self.assertTrue(bus.subscribers.get('BookRegisteredEvent') is not None)

		self.assertTrue(len(bus.subscribers.get('RegisterBookCommand')) == 1)
		self.assertTrue(len(bus.subscribers.get('BookRegisteredEvent')) == 2)

		self.assertIn(
			'MockCommandHandler1', bus.subscribers['RegisterBookCommand'])
		self.assertIn(
			'MockEventHandler1', bus.subscribers['BookRegisteredEvent'])
		self.assertIn(
			'MockEventHandler2', bus.subscribers['BookRegisteredEvent'])

		with self.assertRaises(CommandAlreadySubscribedError):
			bus.subscribe(RegisterBookCommand, 'MockCommandHandler2')


if __name__ == '__main__':
	unittest.main()
