"""
Micro Service with Ports and Adapters Architecture
==================================================
The application's entry point. Loads, configures and starts the application.

__license__ =  MIT
__author__ = 'Lucas Góes'
__email__ = 'lucas.rd.goes@gmail.com'
"""

import logging

from . import domain, handlers, settings
from .version import __version__


def main():
	"""The application's main function."""
	app = settings.ApplicationConfig()

	# Configuring logger.
	logging.basicConfig(
		level=app.logger_level,
		format='%(asctime) -19s | %(levelname) -8s | %(threadName) -10s |'
			   ' %(funcName) -16s | %(message)s'
	)
	logger = logging.getLogger(app.logger_name)
	logger.info('Started sample book managing application v{0}.' \
				.format(__version__))

	"""Creates message bus for exchange of commands and events with the
	adapters.
	"""
	bus = domain.ports.MessageBus()

	# Creates director and list of builders to make the app's adapters.
	director = settings.Director(bus)
	builders = settings.Builder.__subclasses__()

	# Configuring senders.
	# sender_builders = app.senders

	# Configuring database.
	database = app.database
	database_builder = next(
		b for b in builders if b.tech == database and b.ctx == 'database')
	director.set_builder(database_builder())
	database_adapter = director.get_adapter()

	# Creates handlers and subscribtions to its commands and events.
	bus.subscribe(
		domain.messages.RegisterBookCommand,
		handlers.RegisterBookHandler(database_adapter.get_uowm())
	)
	bus.subscribe(
		domain.messages.ReadBookCommand,
		handlers.ReadBookHandler(database_adapter.get_view())
	)
	bus.subscribe(
		domain.messages.ViewBooksCommand,
		handlers.ViewBooksHandler(database_adapter.get_view())
	)
	bus.subscribe(
		domain.messages.ViewBookByIsbnCommand,
		handlers.ViewBookByIsbnHandler(database_adapter.get_view())
	)
	bus.subscribe(
		domain.messages.ViewBooksByNameCommand,
		handlers.ViewBooksByNameHandler(database_adapter.get_view())
	)
	bus.subscribe(
		domain.messages.ViewBooksByAuthorCommand,
		handlers.ViewBooksByAuthorHandler(database_adapter.get_view())
	)

	# Configuring interfaces.
	interfaces = app.interfaces
	interface_adapters = []
	for interface in interfaces:
		interface_builder = next(
			b for b in builders if b.tech == interface and b.ctx == 'interface'
		)
		director.set_builder(interface_builder())
		interface_adapters.append(director.get_adapter())

	# Starting application.
	try:
		for interface_adapter in interface_adapters:
			interface_adapter.start()
	except KeyboardInterrupt:
		for interface_adapter in interface_adapters:
			interface_adapter.stop()
		logger.info('The application has been interrupted.')


if __name__ == '__main__':
	main()
