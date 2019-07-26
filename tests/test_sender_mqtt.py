"""Unit tests of the application's adapter mqtt.py functions."""

import time
import unittest
import threading

import paho.mqtt.subscribe as subscribe

from app.adapters.mqtt import MqttSender


class MockSubscriber(object):
	def __init__(self):
		self.topic = ''
		self.payload = ''

	def wait_event(self):
		msg = subscribe.simple('tests/event')

		self.topic = msg.topic
		self.payload = str(msg.payload.decode('utf8'))


class TestAdaptersMqttSender(unittest.TestCase):
	"""Set of unit tests for the mqtt.py MqttSender class and its
	implementations.

	Tests: test_send
	"""
	def test_send(self):
		"""Steps:
		1 - Instantiates a MqttSender
		2 - Creates a MQTT subscriber to listen to the message
		3 - Sends message using the sender and verify if it arrived
		"""
		sender = MqttSender(
			{'topic': 'tests/event', 'host': 'localhost', 'port': 1883,
			 'username': None, 'password': None}
		)

		subscriber = MockSubscriber()
		t = threading.Thread(target=subscriber.wait_event)
		t.start()
		time.sleep(0.1)

		sender.send('An event has ocurred!')
		t.join()

		self.assertIn(subscriber.topic, 'tests/event')
		self.assertIn(subscriber.payload, 'An event has ocurred!')


if __name__ == '__main__':
	unittest.main()
