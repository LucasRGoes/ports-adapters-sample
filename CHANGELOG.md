Changelog
=========

## v0.1.0

* __06-19-2019__:
	* Created projected structure;
	* Created README.md file;
	* Started creation of the app's driven ports;

* __06-22-2019__:
	* Started organizing the project's modules based on the architecture;
	* Created logic.py to hold business logic;
	* Created ports.py to hold the application's API and SPI;
	* Created errors.py to hold the application's errors;
	* Created commands and handlers at ports.py;
	* Created command bus;
	* Started creation of a MQTT driver adapter;
	* Organizing settings.py to use configuration classes;
	* Started usage of DI and configuration at __main__;
	* Created memory driver adapter for storage;

* __06-23-2019__:
	* Reorganized modules logic.py and ports.py to domain.py and controller.py;
	* Rethinked the application's ports;
	* Created UnitOfWorkManager and UnitOfWork for the usage of the Unit of Work design pattern;
	* Implemented the memory storage adapter's classes;
 	* First working example completed;

* __06-24-2019__:
	* Using abstact base classes at the application's interfaces;
	* Created new directories and renamed some modules to reorganize the project for simplicity;
	* Renamed error classes;
	* Started using Message Bus design pattern instead of the Command Bus design pattern;
	* Started creation of events;
	* Deleted domain.py and controller.py and added all of their content to the new domain dir and the handlers.py file;
