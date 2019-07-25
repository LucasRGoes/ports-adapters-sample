"""A MQTT interface adapter."""

import json
import logging

import paho.mqtt.client as mqtt

from ..settings import identify
from ..domain.messages import RegisterBookCommand, ReadBookCommand, \
							  ViewBooksCommand, ViewBookByIsbnCommand, \
							  ViewBooksByNameCommand, ViewBooksByAuthorCommand


@identify('mqtt', 'interface')
class MqttAdapter(object):
	"""Listens to incoming MQTT packages and executes the associated commands.

	Methods: start, stop
	"""
	def __init__(self, cfg: dict, bus):
		"""Mqtt's constructor.
		
		Params
		------
		cfg: dict -- the MQTT adapter's configuration
		bus: -- the message bus used to handle incoming commands
		"""
		self.logger = logging.getLogger(cfg['logger_name'])
		self.bus = bus

		self.topic = cfg['topic']
		self.host = cfg['host']
		self.port = cfg['port']
		self.username = cfg['username']
		self.password = cfg['password']

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
				cmd = RegisterBookCommand(
					payload['isbn'], payload['name'], payload['author'],
					payload['content']
				)
			elif 'read' in topic:
				cmd = ReadBookCommand(payload['isbn'])
			elif 'view/isbn' in topic:
				cmd = ViewBookByIsbnCommand(payload['isbn'])
			elif 'view/name' in topic:
				cmd = ViewBooksByNameCommand(payload['name'])
			elif 'view/author' in topic:
				cmd = ViewBooksByAuthorCommand(payload['author'])
			elif 'view' in topic:
				cmd = ViewBooksCommand()

			self.logger.debug('Command created: {0}'.format(cmd))

			ret = self.bus.handle(cmd)
			if ret is not None:
				self.logger.info('Response: {0}'.format(ret))

		return on_message

	def start(self):
		"""Method to initialize the adapter by connecting to the broker and
		listening to incoming requests."""
		self.client.connect(self.host, self.port)
		self.client.loop_forever()

	def stop(self):
		"""Finishes MQTT connection."""
		self.client.disconnect()
