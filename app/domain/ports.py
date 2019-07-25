"""
Ports
=====
	These are the tools used by the application to communicate with external
services (or adapters on the architecture terms). It offers messages buses for
the exchange of commands with driver adapters and events with driven adapters.
It also offers interfaces for repositories to implement for database storage
and querying.

ABCs: BookRepository, BookView, UnitOfWork, UnitOfWorkManager

Classes: MessageBus
"""

import abc
from collections import defaultdict

from .model import Book
from .errors import CommandAlreadySubscribedError
from .messages import COMMANDS


"""
	These are the abstract base class for repository driven adapters to
implement, or you could say it is the application's SPI for data storage and
query.

	For data storage the Repository design pattern is used, while for data
querying the CQRS design pattern is considered, separating queries from data
creation, update and deletion.
"""
class BookRepository(abc.ABC):
	"""BookRepository is an abstract base class for repositories concerning
	data mutation methods.

	Methods: save
	"""
	@abc.abstractmethod
	def save(self, book: Book):
		"""Method to be implemented to save books to the database.

		Params
		------
		book: Book -- the book to be inserted on the application's database
		"""
		pass


class BookView(abc.ABC):
	"""BookView is an abstract base class for repositories concerning data
	querying methods.

	Methods: get_all, get_by_isbn, get_by_name, get_by_author
	"""
	@abc.abstractmethod
	def get_all(self) -> list:
		"""Fetches all books from the database.

		Returns
		-------
		books: list -- a list of all books at database
		"""
		pass

	@abc.abstractmethod
	def get_by_isbn(self, isbn: str) -> Book:
		"""Fetches a book by its ISBN from the database.

		Params
		------
		isbn: str -- the ISBN of the book to be fetched

		Returns
		-------
		book: Book -- the book with the chosen ISBN
		"""
		pass

	@abc.abstractmethod
	def get_by_name(self, name: str) -> list:
		"""Fetches all books with a certain name from the database.

		Params
		------
		name: str -- the name of the books to be fetched

		Returns
		-------
		books: list -- a list of all books with the chosen name at database
		"""
		pass

	@abc.abstractmethod
	def get_by_author(self, author: str) -> list:
		"""Fetches all books of a certain author from the database.

		Params
		------
		author: str -- the name of the author from the books to be fetched

		Returns
		-------
		books: list -- a list of all books written by the author at database
		"""
		pass


class UnitOfWork(abc.ABC):
	"""The unit of work is an abstract base class for the usage of the Unit of
	Work design pattern. Used to represent a bunch of commands that are to be
	executed together.

	Methods: __enter__, __exit__, commit, rollback, books
	"""
	@abc.abstractmethod
	def __enter__(self):
		"""Magic method for Python's 'with' usage. This command is executed
		whenever a new with is created for a unit of work.
		"""
		pass

	@abc.abstractmethod
	def __exit__(self, type, value, traceback):
		"""Magic method for Python's 'with' usage. This command is executed
		whenever a with ends from a unit of work.
		"""
		pass

	@abc.abstractmethod
	def commit(self):
		"""Used to store all changed data at database."""
		pass

	@abc.abstractmethod
	def rollback(self):
		"""Used to clear uncommited data."""
		pass

	@property
	@abc.abstractmethod
	def books(self) -> BookRepository:
		"""A convenient access for an instance of a BookRepository.

		Returns
		-------
		books: BookRepository -- an instance of a BookRepository for data
		mutation
		"""
		pass


class UnitOfWorkManager(abc.ABC):
	"""The unit of work manager is an abstract base class for the usage of the
	Unit of Work design pattern. Used to instantiate new units of work.

	Methods: start
	"""
	@abc.abstractmethod
	def start(self) -> UnitOfWork:
		"""The manager creates an instance of a UnitOfWork for database usage.

		Returns
		-------
		unit_of_work: UnitOfWork -- a unit of work for database usage
		"""
		pass


class MessageBus(object):
	"""The message bus was developed following the Message Bus design pattern.
	It is responsible for the execution of handlers subscribed to commands or
	events. When a message concerning these commands and events arrives the
	subscribed handlers are executed.

	Methods: handle, subscribe
	"""
	def __init__(self):
		"""MessageBus' constructor. Creates a list of subscribers."""
		self.subscribers = defaultdict(list)

	def handle(self, msg):
		"""Handles the incoming message by executing the handlers associated
		with it.

		Params
		------
		msg -- a command or event that need to be handled
		"""
		subscribers = self.subscribers[type(msg).__name__]
		for subscriber in subscribers:
			subscriber.handle(msg)

	def subscribe(self, msg, handler):
		"""Subscribes a handler to a command or event.

		Params
		------
		msg -- the command or event that the handler wants to subscribe to
		handler -- the handler that wants to subscribe
		"""
		subscribers = self.subscribers[msg.__name__]

		# Commands should have a 1:1 relationship with handlers.
		if type(msg).__name__ in COMMANDS and len(subscribers) > 0:
			raise CommandAlreadySubscribedError(
				'The command \'{0}\' already has a handler subscribed to it.' \
				.format(type(msg).__name__))

		subscribers.append(handler)
