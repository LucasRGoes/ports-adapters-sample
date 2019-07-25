"""
Messages
========
	Messages are used for domain communication. They are to be used by driver
adapters to talk to the application and for the application to talk with driven
adapters in a technology agnostic way.

Classes: RegisterBookCommand, BookRegisteredEvent
"""

from collections import namedtuple


COMMANDS = ['RegisterBookCommand']
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


"""These are the application's events. They are used to give feedback over
conclusion of certain events to driven adapters like event queues, logging
services, etc...
"""
BookRegisteredEvent = namedtuple('BookRegisteredEvent', ['isbn'])
