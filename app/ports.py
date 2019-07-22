"""
Ports
=====
	It presents commands for usage of driver adapters to communicate with the
application, an API (application programming interface) of sorts to interface
with it in a technology agnostic way.
	It also has interfaces for driven adapters to implement so that it can
communicate with them, like Java's SPI (service provider interface).
"""

from collections import namedtuple

from .errors import CommandNotFoundError


"""
	These are the application's commands or API. Simple (key: value) objects
that holds the necessary information for the commands to be executed.
	The commands are the application's ports for driver adapters, so they
should always be named by actions that represent interaction with the service.
	For each command there is a unique handler that can resolve it.
"""
RegisterBookCommand = namedtuple(
	'RegisterBookCommand', ['author', 'isbn', 'name'])

BorrowBookCommand = namedtuple('BorrowBookCommand', ['isbn'])

ReturnBookCommand = namedtuple('ReturnBookCommand', ['isbn'])


def register_book_command_handler(command: RegisterBookCommand):
	"""Handler for the registering of a new book at the library.

	Params
	------
	command: RegisterBookCommand -- the expected command to register a book
	"""
	print('Registering book: {0}'.format(command))


def borrow_book_command_handler(command: BorrowBookCommand):
	"""Handler for the borrowing of a book from the library.

	Params
	------
	command: BorrowBookCommand -- the expected command to borrow a book
	"""
	print('Borrowing book: {0}'.format(command))


def return_book_command_handler(command: ReturnBookCommand):
	"""Handler for the returning of a book to the library.

	Params
	------
	command: ReturnBookCommand -- the expected command to return a book
	"""
	print('Returning book: {0}'.format(command))


class CommandBus(object):
	"""The command bus was developed following the Command Bus design pattern.
	It is responsible for the execution of commands by running the
	corresponding handler of a chosen command.
	"""
	def __init__(self):
		"""CommandBus's constructor."""
		self.command_handler_map = {
			'RegisterBookCommand': register_book_command_handler,
			'BorrowBookCommand': borrow_book_command_handler,
			'ReturnBookCommand': return_book_command_handler
		}

	def dispatch(self, command):
		"""CommandBus's dispatcher, responsible for mapping the chosen command
		to a handler and executing it.

		Params
		------
		command -- an existing command of the application's API 
		"""
		command_name = command.__class__.__name__
		handler = self.command_handler_map.get(command_name)

		if handler is not None:
			handler(command)
		else:
			raise CommandNotFoundError('the command \'{0}\' doesn\'t exist.' \
									   .format(command_name))


"""
	These are the interfaces for the driven adapters to implement, or the
application's SPI.
"""
class BookStorage(object):
	"""BookStorage is an interface for driven adapters that communicate with
	databases."""
	def register(self, book):
		"""Method to be implemented to register books to the application.

		Params
		------
		book -- the book to be inserted on the application
		"""
		pass

	def borrow(self, isbn):
		"""Method to be implemented to borrow books from the application.

		Params
		------
		isbn -- the isbn from the book to be borrowed from the application
		"""
		pass

	def return_(self, isbn):
		"""Method to be implemented to return books to the application.

		Params
		------
		isbn -- the isbn from the book to be returned to the application
		"""
		pass
