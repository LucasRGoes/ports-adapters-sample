"""
Settings
========
	The settings script is solely dedicated to parsing the application's
configuration files and bundling them as builders for the app's components.

Decorators: identify

ABCs: Builder

Classes: Director, MqttInterfaceBuilder, MemoryDatabaseBuilder,
ApplicationConfig
"""

import os
import re
import abc
import sys
import inspect
import importlib

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


APP_LOGGER_NAME = os.getenv('APP_LOGGER_NAME', 'app')


def identify(tech: str, ctx: str):
	"""Adds two attributes to a class: (1) the class technology (mqtt, sqlite,
	etc...) and (2) the class context (database, interface or sender).

	Params
	------
	tech: str -- the technology associated with the class
	ctx: str -- the context where the class is inserted

	Returns
	-------
	func -- the decorator that adds the attributes to the class
	"""
	def decorator(cls):
		setattr(cls, 'tech', tech)
		setattr(cls, 'ctx', ctx)

		return cls

	return decorator


class Builder(abc.ABC):
	"""Abstract base class to be extended by further builders. Follows the
	Builder design pattern.

	Methods: __call__, name, get_logger_name
	"""
	@abc.abstractmethod
	def __call__(self) -> dict:
		"""Bundles the builder configuration and returns it.

		Returns
		-------
		configuration: dict	
		"""
		pass

	@property
	@abc.abstractmethod
	def name(self) -> str:
		"""Returns the name of the module associated with the adapter.

		Returns
		-------
		name: str
		"""
		pass

	def get_logger_name(self) -> str:
		"""Returns logger name for same logger usage between modules.

		Returns
		-------
		logger_name: str
		"""
		return APP_LOGGER_NAME


class Director(object):
	"""The application's director that builds the necessary modules for it to
	work. It follows the Builder design pattern.

	Methods: set_builder, get_repository, get_interface, get_sender
	"""
	def __init__(self, bus):
		"""Director's constructor.

		bus -- a message bus used by adapters
		"""
		self.builder = None
		self.bus = bus

	def set_builder(self, builder: Builder):
		"""Configures the director's builder.

		Params
		------
		builder: Builder -- the builder to be used on construction
		"""
		self.builder = builder

	def get_adapter(self):
		"""Using the current builder builds an adapter.

		Returns
		-------
		adapter -- the built adapter
		"""
		importlib.import_module('app.adapters.{0}'.format(self.builder.name))

		classes = inspect.getmembers(
			sys.modules['app.adapters.{0}'.format(self.builder.name)],
			inspect.isclass
		)

		adapter = next(
			cls_ for cls_ in classes \
			if hasattr(cls_[1], 'tech') and hasattr(cls_[1], 'ctx')
		)[1]

		if adapter.ctx == 'interface':
			return adapter(self.builder(), self.bus)
		else:
			return adapter(self.builder())


@identify('mqtt', 'interface')
class MqttInterfaceBuilder(Builder):
	"""Builder class for setting up a MQTT driver adapter.

	Methods: __call__, name, get_topic, get_host, get_port, get_username,
	get_password
	"""
	def __init__(self):
		"""MqttInterfaceBuilder's constructor."""
		pass

	def __call__(self) -> dict:
		"""View @settings.Builder"""
		return {
			'logger_name': self.get_logger_name(),
			'topic': self.get_topic(),
			'host': self.get_host(),
			'port': self.get_port(),
			'username': self.get_username(),
			'password': self.get_password()
		}

	@property
	def name(self) -> str:
		"""View @settings.Builder"""
		return 'mqtt'

	def get_topic(self) -> str:
		"""Returns MQTT topic for subscription.

		Returns
		-------
		topic: str
		"""
		return os.getenv('MQTT_DRIVER_TOPIC', 'app/book/#')

	def get_host(self) -> str:
		"""Returns host of the MQTT broker to connect.

		Returns
		-------
		host: str
		"""
		return os.getenv('MQTT_DRIVER_HOST', 'localhost')

	def get_port(self) -> int:
		"""Returns port of the MQTT broker to connect.

		Returns
		-------
		port: int
		"""
		try:
			return int(os.getenv('MQTT_DRIVER_PORT'))
		except:
			return 1883

	def get_username(self) -> str:
		"""Returns username to use on MQTT connection.

		Returns
		-------
		username: str
		"""
		return os.getenv('MQTT_DRIVER_USERNAME')

	def get_password(self) -> str:
		"""Returns password to use on MQTT connection.

		Returns
		-------
		password: str
		"""
		return os.getenv('MQTT_DRIVER_PASSWORD')


@identify('memory', 'database')
class MemoryDatabaseBuilder(Builder):
	"""Builder class for setting up a memory database driven adapter.

	Methods: __call__, name
	"""
	def __init__(self):
		"""MemoryDatabaseBuilder's constructor."""
		pass

	def __call__(self) -> dict:
		"""View @settings.Builder"""
		return {'logger_name': self.get_logger_name()}

	@property
	def name(self) -> str:
		"""View @settings.Builder"""
		return 'memory'


class ApplicationConfig(object):
	"""Configuration class for setting up the application.
	
	Methods: logger_name, logger_level, database, interfaces, senders
	"""
	def __init__(self):
		"""ApplicationConfig's constructor."""
		pass

	@property
	def logger_name(self) -> str:
		"""Returns logger name for same logger usage between modules.

		Returns
		-------
		logger_name: str
		"""
		return APP_LOGGER_NAME

	@property
	def logger_level(self) -> str:
		"""Returns logger level for configuration.

		Returns
		-------
		logger_level: str
		"""
		logger_level = os.getenv('APP_LOGGER_LEVEL', 'INFO').upper()

		if logger_level != 'DEBUG' \
		   and logger_level != 'INFO' \
		   and logger_level != 'WARNING' \
		   and logger_level != 'ERROR' \
		   and logger_level != 'CRITICAL':

		   logger_level = 'INFO'

		return logger_level

	@property
	def database(self) -> str:
		"""The chosen driven adapter to be used as the application's data
		storage.

		Returns
		-------
		repository: str
		"""
		return os.getenv('APP_DATABASE', 'memory').lower()

	@property
	def interfaces(self) -> list:
		"""The chosen driver adapters for usage as interfaces of the app.

		Returns
		-------
		interfaces: list
		"""
		interfaces = os.getenv('APP_INTERFACES', 'mqtt').lower()

		# Parses it into a list.
		return re.sub(r'\ ', '', interfaces).split(',')

	@property
	def senders(self) -> list:
		"""The chosen driven adapters for sending the app's events.

		Returns
		-------
		senders: list
		"""
		senders = os.getenv('APP_SENDERS', 'mqtt').lower()

		# Parses it into a list.
		return re.sub(r'\ ', '', senders).split(',')
