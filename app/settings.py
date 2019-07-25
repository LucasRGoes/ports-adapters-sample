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


def identify(tech: str, ctx: str):
	"""Adds two attributes to a class: (1) the class technology (mqtt, sqlite,
	etc...) and (2) the class context (database, interface or sender).

	Params
	------
	tech: str -- the technology associated with the class
	ctx: str -- the context where the class is inserted

	Returns
	-------
	func -- the decorator that adds these attributes to the class and its
	instances
	"""
	def decorator(cls):
		# Sets attributes to class
		setattr(cls, 'tech', tech)
		setattr(cls, 'ctx', ctx)

		# Sets properties to instances
		cls.name = tech

		return cls

	return decorator


class Builder(abc.ABC):
	"""Abstract base class to be extended by further builders. Follows the
	Builder design pattern.

	Methods: __call__
	"""
	def __init__(self):
		"""Builder's constructor."""
		pass

	@abc.abstractmethod
	def __call__(self) -> dict:
		"""Bundles the builder's configuration for its associated adapter and
		returns it."""
		pass


class Director(object):
	"""The application's director that builds the necessary modules for it to
	work. It follows the Builder design pattern.

	Methods: set_builder, get_adapter
	"""
	def __init__(self):
		"""Director's constructor."""
		self.builder = None

	def set_builder(self, builder: Builder):
		"""Configures the director's builder.

		Params
		------
		builder: Builder -- the builder to be used on construction
		"""
		self.builder = builder

	def get_adapter(self):
		"""Using the current builder builds a driver adapter (or primary
		adapter).

		Returns
		-------
		adapter -- the built driver adapter
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

		return adapter(self.builder())


@identify('mqtt', 'interface')
class MqttInterfaceBuilder(Builder):
	"""Builder class for setting up a MQTT driver adapter.

	Methods: __call__, __get_topic, __get_host, __get_port, __get_username,
	__get_password
	"""
	def __init__(self):
		"""MqttInterfaceBuilder's constructor."""
		pass

	def __call__(self) -> dict:
		"""View @settings.Builder"""
		return {
			'topic': self.__get_topic(),
			'host': self.__get_host(),
			'port': self.__get_port(),
			'username': self.__get_username(),
			'password': self.__get_password()
		}

	def __get_topic(self) -> str:
		"""Returns MQTT topic for subscription."""
		return os.getenv('MQTT_DRIVER_TOPIC', 'app/book/#')

	def __get_host(self) -> str:
		"""Returns host of the MQTT broker to connect."""
		return os.getenv('MQTT_DRIVER_HOST', 'localhost')

	def __get_port(self) -> int:
		"""Returns port of the MQTT broker to connect."""
		try:
			return int(os.getenv('MQTT_DRIVER_PORT'))
		except:
			return 1883

	def __get_username(self) -> str:
		"""Returns username to use on MQTT connection."""
		return os.getenv('MQTT_DRIVER_USERNAME')

	def __get_password(self) -> str:
		"""Returns password to use on MQTT connection."""
		return os.getenv('MQTT_DRIVER_PASSWORD')


@identify('flask', 'interface')
class FlaskInterfaceBuilder(Builder):
	"""Builder class for setting up a Flask driver adapter.

	Methods: __call__, _get_host, __get_port, __get_debug
	"""
	def __init__(self):
		"""FlaskInterfaceBuilder's constructor."""
		pass

	def __call__(self) -> dict:
		"""View @settings.Builder"""
		return {
			'host': self.__get_host(),
			'port': self.__get_port(),
			'debug': self.__get_debug()
		}

	def __get_host(self) -> str:
		"""Returns host of the Flask server."""
		return os.getenv('FLASK_DRIVER_HOST', '0.0.0.0')

	def __get_port(self) -> int:
		"""Returns port of the Flask server."""
		try:
			return int(os.getenv('FLASK_DRIVER_PORT'))
		except:
			return 5000

	def __get_debug(self) -> str:
		"""Returns debug flag for Flask server."""
		return os.getenv('FLASK_DRIVER_DEBUG', False)


@identify('memory', 'database')
class MemoryDatabaseBuilder(Builder):
	"""Builder class for setting up a memory database driven adapter.

	Methods: __call__
	"""
	def __init__(self):
		"""MemoryDatabaseBuilder's constructor."""
		pass

	def __call__(self) -> dict:
		"""View @settings.Builder"""
		return {}


@identify('sqlite', 'database')
class SqliteDatabaseBuilder(Builder):
	"""Builder class for setting up a SQLite database driven adapter.

	Methods: __call__, __get_location
	"""
	def __init__(self):
		"""SqliteDatabaseBuilder's constructor."""
		pass

	def __call__(self) -> dict:
		"""View @settings.Builder"""
		return {'location': self.__get_location()}

	def __get_location(self) -> str:
		"""Returns location to store SQLite database."""
		return os.getenv('SQLITE_DRIVER_LOCATION', 'db.sqlite')


class ApplicationConfig(object):
	"""Configuration class for setting up the application.
	
	Methods: logger_level, database, interfaces, senders
	"""
	def __init__(self):
		"""ApplicationConfig's constructor."""
		pass

	@property
	def logger_level(self) -> str:
		"""Returns logger level for configuration."""
		logger_level = os.getenv('APP_LOGGER_LEVEL', 'INFO').upper()

		if logger_level != 'DEBUG' \
		   and logger_level != 'INFO' \
		   and logger_level != 'WARNING' \
		   and logger_level != 'ERROR' \
		   and logger_level != 'CRITICAL':

		   logger_level = 'INFO'

		return logger_level

	@property
	def logger_styles(self) -> str:
		"""Returns the logger color for each level of logging."""
		return ('info=blue;'
				'warning=green;'
				'error=red;'
				'critical=red,bold;'
				'debug=white')
	
	@property
	def logger_format(self) -> str:
		"""Returns the logger format to be used on the logger."""
		return ('%(asctime) -19s | %(levelname) -8s | %(threadName) -10s | '
				'%(funcName) -16s | %(message)s')

	@property
	def database(self) -> str:
		"""The chosen driven adapter to be used as the application's data
		storage.
		"""
		return os.getenv('APP_DATABASE', 'memory').lower()

	@property
	def interfaces(self) -> list:
		"""The chosen driver adapters for usage as interfaces of the app."""
		interfaces = os.getenv('APP_INTERFACES', 'mqtt').lower()

		# Parses it into a list.
		return re.sub(r'\ ', '', interfaces).split(',')

	@property
	def senders(self) -> list:
		"""The chosen driven adapters for sending the app's events."""
		senders = os.getenv('APP_SENDERS', 'mqtt').lower()

		# Parses it into a list.
		return re.sub(r'\ ', '', senders).split(',')
