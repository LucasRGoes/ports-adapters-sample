"""A MQTT driver adapter."""

import json
import logging

import paho.mqtt.client as mqtt

from ..ports import RegisterBookCommand, BorrowBookCommand, ReturnBookCommand


class MqttAdapter(object):
	"""A MQTT adapter class that listens to incoming MQTT packages and
	executes the associated commands.

	Params
	------
	config: dict -- a dictionary containing the MQTT adapter's configuration
	"""
	def __init__(self, config, command_bus):
		"""MqttAdapter's constructor.
		
		Params
		------
		config: -- MQTT adapter configuration
		command_bus: -- the command bus to dispatch commands
		"""
		self.logger = logging.getLogger(config.logger_name)
		self.command_bus = command_bus

		self.topic = config.topic
		self.host = config.host
		self.port = config.port
		self.username = config.username
		self.password = config.password

		self.client = mqtt.Client()
		self.client.username_pw_set(self.username, password=self.password)
		self.client.on_connect = self.__on_connect()
		self.client.on_disconnect = self.__on_disconnect()
		self.client.on_subscribe = self.__on_subscribe()
		self.client.on_message = self.__on_message()

	def __on_connect(self):
		"""Creates MQTT callback for estabilished connections."""
		def on_connect(client, userdata, flags, rc):
			if rc == 0:
				self.logger.info('Connected successfully.')
				client.subscribe(self.topic)
			else:
				self.logger.warning(
					'Failure at connect with result code {0}.'.format(rc))

		return on_connect

	def __on_disconnect(self):
		"""MQTT callback for succesfull or unexpected disconnections."""
		def on_disconnect(client, userdata, rc):
			if rc == 0:
				self.logger.info('Disconnected successfully.')
			else:
				self.logger.warning(
					'Unexpected disconnection with result code {0}.' \
					.format(rc))
				client.connect(self.host, self.port)

		return on_disconnect

	def __on_subscribe(self):
		"""MQTT callback for estabilished subscriptions."""
		def on_subscribe(client, userdata, mid, granted_qos):
			self.logger.info('Subscribed to {0}.'.format(self.topic))

		return on_subscribe

	def __on_message(self):
		"""MQTT callback for received messages."""
		def on_message(client, userdata, msg):
			topic = msg.topic
			payload = json.loads(str(msg.payload.decode('utf8')))

			self.logger.info('Message arrived | topic: {0} | payload: {1}.' \
							 .format(topic, payload))

			if 'register' in topic:
				cmd = RegisterBookCommand(payload['author'], payload['isbn'],
										  payload['name'])
			elif 'borrow' in topic:
				cmd = BorrowBookCommand(payload['isbn'])
			elif 'return' in topic:
				cmd = ReturnBookCommand(payload['isbn'])

			self.command_bus.dispatch(cmd)

		return on_message

	def start(self):
		"""Method to initialize the adapter by connecting to the broker and
		listening to incoming requests."""
		self.client.connect(self.host, self.port)
		self.client.loop_forever()

	def stop(self):
		"""Finishes MQTT connection."""
		self.client.disconnect()
