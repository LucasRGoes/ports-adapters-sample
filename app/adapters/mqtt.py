"""A MQTT interface adapter."""

import json
import logging
from multiprocessing import Process

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

from ..settings import identify
from ..domain.ports import QueueSender
from ..domain.messages import RegisterBookCommand


LOGGER = logging.getLogger('sample')


@identify('mqtt', 'interface')
class MqttInterface(object):
	"""Listens to incoming MQTT packages and executes the associated commands.

	Methods: set_message_bus, set_view, start, stop
	"""
	def __init__(self, cfg: dict):
		"""MqttInterface's constructor.
		
		Params
		------
		cfg: dict -- the MQTT interface adapter's configuration
		"""
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

	def set_message_bus(self, bus):
		"""Sets the message bus to be used by the adapter to execute commands.

		Params
		------
		bus -- the message bus
		"""
		self.bus = bus

	def set_view(self, view):
		"""Sets the view used to read the database.

		Params
		------
		view -- the database view
		"""
		self.view = view
	
	def run(self):
		"""Method to initialize the adapter by connecting to the broker and
		listening to incoming requests."""
		self.client.connect(self.host, self.port)
		server = Process(target=self.client.loop_forever)
		server.start()

	def __on_connect(self):
		"""Creates MQTT callback for estabilished connections."""
		def on_connect(client, userdata, flags, rc):
			if rc == 0:
				LOGGER.info('Connected successfully')
				client.subscribe(self.topic)
			else:
				LOGGER.warning(
					'Failure at connect with result code {0}'.format(rc))

		return on_connect

	def __on_disconnect(self):
		"""MQTT callback for succesfull or unexpected disconnections."""
		def on_disconnect(client, userdata, rc):
			if rc == 0:
				LOGGER.info('Disconnected successfully')
			else:
				LOGGER.warning(
					'Unexpected disconnection with result code {0}' \
					.format(rc))
				client.connect(self.host, self.port)

		return on_disconnect

	def __on_subscribe(self):
		"""MQTT callback for estabilished subscriptions."""
		def on_subscribe(client, userdata, mid, granted_qos):
			LOGGER.info('Subscribed to {0}'.format(self.topic))

		return on_subscribe

	def __on_message(self):
		"""MQTT callback for received messages."""
		def on_message(client, userdata, msg):
			try:

				topic = msg.topic
				payload = json.loads(str(msg.payload.decode('utf8')))

				LOGGER.info('Message arrived | topic: {0} | payload: {1}' \
							.format(topic, payload))

				if 'register' in topic:
					cmd = RegisterBookCommand(payload['isbn'],
											  payload['name'],
											  payload['author'],
											  payload['content'])

					self.bus.handle(cmd)
					LOGGER.info('A new book has been registered')

				elif 'read' in topic:
					book = self.view.get_by_isbn(payload['isbn'])
					LOGGER.info('Reading book: {0}'.format(book.content))

				elif 'view/isbn' in topic:
					book = self.view.get_by_isbn(payload['isbn'])
					LOGGER.info('Found book: {0}'.format(book))

				elif 'view/name' in topic:
					books = self.view.get_by_name(payload['name'])
					LOGGER.info('Found books: {0}'.format(books))

				elif 'view/author' in topic:
					books = self.view.get_by_author(payload['author'])
					LOGGER.info('Found books: {0}'.format(books))

				elif 'view' in topic:
					books = self.view.get_all()
					LOGGER.info('Found books: {0}'.format(books))

			except Exception as err:
				LOGGER.error(
					'Error at application execution: {0}'.format(err))

		return on_message


@identify('mqtt', 'sender')
class MqttSender(QueueSender):
	"""An MQTT implementation of a sender to dispatch the application's events.

	Methods: send
	"""
	def __init__(self, cfg: dict):
		"""MqttSender's constructor.
		
		Params
		------
		cfg: dict -- the MQTT sender adapter's configuration
		"""
		self.topic = cfg['topic']
		self.host = cfg['host']
		self.port = cfg['port']
		self.username = cfg['username']
		self.password = cfg['password']

	def send(self, msg):
		"""View @app.domain.ports.QueueSender."""
		if self.username is not None and self.password is not None:
			publish.single(
				self.topic, payload=msg, hostname=self.host, port=self.port,
				auth={'username': self.username, 'password': self.password}
			)
		else:
			publish.single(
				self.topic, payload=msg, hostname=self.host, port=self.port)
