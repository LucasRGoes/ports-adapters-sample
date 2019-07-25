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

import coloredlogs

from . import domain, handlers, settings
from .version import __version__


def main():
	"""The application's main function."""
	app = settings.ApplicationConfig()

	# Configuring logger.
	logger = logging.getLogger('sample')
	coloredlogs.install(
	    fmt=app.logger_format,
	    level_styles=coloredlogs.parse_encoded_styles(app.logger_styles),
	    level=app.logger_level, logger=logger, milliseconds=True
	)
	logger.info('Started sample book managing application v{0}' \
				.format(__version__))

	# Creates director and list of builders to make the app's adapters.
	logger.debug('Creating director and fetching builders to create the app\'s'
				 ' adapters')
	director = settings.Director()
	builders = settings.Builder.__subclasses__()

	# Configuring senders.
	logger.debug('Configuring senders ...')

	try:
		senders = app.senders
		sender_adapters = []
		for sender in senders:

			sender_builder = next(
				b for b in builders if b.tech == sender \
									and b.ctx == 'sender'
			)
			
			# Retrieving adapter and configuring it.
			director.set_builder(sender_builder())
			sender_adapters.append(director.get_adapter())

	except StopIteration as err:
		logger.error(
			'The chosen sender \'{0}\' has no builder or adapter'
			' implementation or one of them is not decorated with @identify' \
			.format(sender)
		)
		sys.exit(1)

	logger.info('Using \'{0}\' adapter(s) for the sender(s)' \
				.format([type(i).__name__ for i in sender_adapters]))

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

	# Subscribes commands.
	bus.subscribe(
		domain.messages.RegisterBookCommand,
		handlers.RegisterBookHandler(bus, database_adapter.get_uowm())
	)

	# Subscribes events.
	for sender_adapter in sender_adapters:
		bus.subscribe(
			domain.messages.BookRegisteredEvent,
			handlers.BookRegisteredHandler(
				database_adapter.get_view(), sender_adapter
			)
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
	logger.debug('Starting application ...')
	for interface_adapter in interface_adapters:
		interface_adapter.run()


if __name__ == '__main__':
	main()
