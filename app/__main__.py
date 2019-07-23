"""
Micro Service with Ports and Adapters Architecture
==================================================
The application's entry point. Loads, configures and starts the application.

__license__ =  MIT
__author__ = 'Lucas Góes'
__email__ = 'lucas.rd.goes@gmail.com'
"""

import logging

from . import domain, controller, adapters, settings
from .version import __version__


def main():
	"""The application's main function."""
	app_config = settings.ApplicationConfig()

	# Configures application logger
	logging.basicConfig(
		level=app_config.logger_level,
		format='%(asctime) -19s | %(levelname) -8s | %(threadName) -10s |'
			   ' %(funcName) -16s | %(message)s'
	)

	logger = logging.getLogger(app_config.logger_name)
	logger.info('Started sample book managing application v{0}.' \
				.format(__version__))

	# Creates driven adapter
	db_uowm = adapters.MemoryUnitOfWorkManager()
	db_view = adapters.MemoryBookView()

	# Creates CommandBus
	command_bus = controller.CommandBus(db_uowm, db_view)

	# Configures and starts adapters
	driver_adapter = app_config.driver_adapter
	if driver_adapter == 'mqtt':
		driver_config = settings.MqttDriverConfig()
		driver_adapter = adapters.MqttAdapter(driver_config, command_bus)

	# Runs driver adapter and awaits for any external interruption
	try:
		driver_adapter.start()
	except KeyboardInterrupt:
		driver_adapter.stop()
		logger.info('The application has been interrupted.')


if __name__ == '__main__':
	main()
