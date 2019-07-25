"""
Micro Service with Ports and Adapters Architecture
==================================================
The application's entry point. Loads, configures and starts the application.

__license__ =  MIT
__author__ = 'Lucas Góes'
__email__ = 'lucas.rd.goes@gmail.com'
"""

import sys
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
	logger = logging.getLogger(__name__)
	logger.info('Started sample book managing application v{0}' \
				.format(__version__))

	# Creates director and list of builders to make the app's adapters.
	logger.debug('Creating director and fetching builders to create the app\'s'
				 ' adapters')
	director = settings.Director()
	builders = settings.Builder.__subclasses__()

	# Configuring senders.
	logger.debug('Configuring senders ...')

	# Configuring database.
	logger.debug('Configuring database ...')

	try:
		database = app.database
		database_builder = next(
			b for b in builders if b.tech == database and b.ctx == 'database')
		director.set_builder(database_builder())

		# Retrieving adapter and configuring it.
		database_adapter = director.get_adapter()
		database_adapter.set_up()

	except StopIteration as err:
		logger.error(
			'The chosen database \'{0}\' has no builder or adapter'
			' implementation or one of them is not decorated with @identify' \
			.format(database)
		)
		sys.exit(1)

	logger.info('Using \'{0}\' adapter for database' \
				.format(type(database_adapter).__name__))

	"""Creates message bus for exchange of commands and events with the
	adapters. Also creates handlers and subscribes them to their commands and
	events.
	"""
	bus = domain.ports.MessageBus()
	bus.subscribe(
		domain.messages.RegisterBookCommand,
		handlers.RegisterBookHandler(database_adapter.get_uowm())
	)

	# Configuring interfaces.
	logger.debug('Configuring interfaces ...')

	try:
		interfaces = app.interfaces
		interface_adapters = []
		for interface in interfaces:

			interface_builder = next(
				b for b in builders if b.tech == interface \
									and b.ctx == 'interface'
			)
			
			# Retrieving adapter and configuring it.
			director.set_builder(interface_builder())
			interface_adapter = director.get_adapter()
			interface_adapter.set_message_bus(bus)
			interface_adapter.set_view(database_adapter.get_view())

			interface_adapters.append(interface_adapter)

	except StopIteration as err:
		logger.error(
			'The chosen interface \'{0}\' has no builder or adapter'
			' implementation or one of them is not decorated with @identify' \
			.format(interface)
		)
		sys.exit(1)

	logger.info('Using \'{0}\' adapter(s) for the interface(s)' \
				.format([type(i).__name__ for i in interface_adapters]))

	# Starting application.
	try:
		for interface_adapter in interface_adapters:
			interface_adapter.start()
	except KeyboardInterrupt:
		for interface_adapter in interface_adapters:
			interface_adapter.stop()
		logger.info('The application has been interrupted')


if __name__ == '__main__':
	main()
