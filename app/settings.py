"""The settings script is solely dedicated to parsing the application's
configuration files and bundling them for the app's components.
"""

import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from .adapters import __all__ as adapters


class Config(object):
	"""Generic configuration to be extended by further classes."""
	def __init__(self):
		"""Config's constructor."""
		pass

	@property
	def logger_name(self) -> str:
		"""Returns logger name for same logger usage between modules.

		Returns
		-------
		logger_name: str
		"""
		return os.getenv('APP_LOGGER_NAME', 'app')


class ApplicationConfig(Config):
	"""Configuration class for the application setup."""

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
	def driver_adapter(self) -> str:
		"""The chosen driver adapter for usage.

		Returns
		-------
		driver_adapter: str
		"""
		driver_adapter = os.getenv('APP_DRIVER_ADAPTER', 'mqtt').lower()

		if driver_adapter not in adapters:
			driver_adapter = 'mqtt'

		return driver_adapter

	@property
	def driven_adapter(self) -> str:
		"""The chosen driven adapter for usage.

		Returns
		-------
		driven_adapter: str
		"""
		return os.getenv('APP_DRIVEN_ADAPTER', 'memory').lower()


class MqttDriverConfig(Config):
	"""Configuration class for MQTT driver adapters."""

	@property
	def topic(self) -> str:
		"""Returns MQTT topic for subscription.

		Returns
		-------
		topic: str
		"""
		return os.getenv('MQTT_DRIVER_TOPIC', 'app/book/#')

	@property
	def host(self) -> str:
		"""Returns host of the MQTT broker to connect.

		Returns
		-------
		host: str
		"""
		return os.getenv('MQTT_DRIVER_HOST', 'localhost')

	@property
	def port(self) -> int:
		"""Returns port of the MQTT broker to connect.

		Returns
		-------
		port: int
		"""
		try:
			return int(os.getenv('MQTT_DRIVER_PORT'))
		except:
			return 1883

	@property
	def username(self) -> str:
		"""Returns username to use on MQTT connection.

		Returns
		-------
		username: str
		"""
		return os.getenv('MQTT_DRIVER_USERNAME')

	@property
	def password(self) -> str:
		"""Returns password to use on MQTT connection.

		Returns
		-------
		password: str
		"""
		return os.getenv('MQTT_DRIVER_PASSWORD')
