"""
Messages
========
	Messages are used for domain communication. They are to be used by driver
adapters to talk to the application and for the application to talk with driven
adapters in a technology agnostic way.

Classes: RegisterBookCommand, ReadBookCommand, ViewBooksCommand,
ViewBookByIsbnCommand, ViewBooksByNameCommand, ViewBooksByAuthorCommand,
BookRegisteredEvent
"""

from collections import namedtuple


COMMANDS = ['RegisterBookCommand', 'ReadBookCommand', 'ViewBooksCommand',
			'ViewBookByIsbnCommand', 'ViewBooksByNameCommand',
			'ViewBooksByAuthorCommand']

EVENTS = ['BookRegisteredEvent']


"""
	These are the application's commands, or its API (Application Programming
Interface). Simple objects that holds the necessary information for the
commands to be executed following the Command Handler design pattern.

	The commands are the application's ports for driver actors and driver
adapters, so they should always be named by actions that represent important
use cases of the application.
"""
RegisterBookCommand = namedtuple(
	'RegisterBookCommand', ['isbn', 'name', 'author', 'content'])

ReadBookCommand = namedtuple('ReadBookCommand', ['isbn'])

ViewBooksCommand = namedtuple('ViewBooksCommand', [])

ViewBookByIsbnCommand = namedtuple('ViewBookByIsbnCommand', ['isbn'])

ViewBooksByNameCommand = namedtuple('ViewBooksByNameCommand', ['name'])

ViewBooksByAuthorCommand = namedtuple('ViewBooksByAuthorCommand', ['author'])


"""These are the application's events. They are used to give feedback over
conclusion of certain events to driven adapters like event queues, logging
services, etc...
"""
BookRegisteredEvent = namedtuple(
	'BookRegisteredEvent', ['isbn', 'name', 'author', 'content'])
