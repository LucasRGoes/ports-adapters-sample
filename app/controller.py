"""
Controller
==========
	The controller module is responsible for the orchestration of the
application. By utilizing the domain's tools and its own 'glue' code it
handles each incoming request and outgoing response.

Classes: UnitOfWork, UnitOfWorkManager, CommandBus

Functions: register_book_command_handler, read_book_command_handler,
view_books_command_handler, view_book_by_isbn_command_handler,
view_book_by_name_command_handler, view_book_by_author_command_handler
"""

from .domain import Book, BookRepository, BookView
from .domain import RegisterBookCommand, ReadBookCommand, ViewBooksCommand, \
					ViewBookByIsbnCommand, ViewBooksByNameCommand, \
					ViewBooksByAuthorCommand
from .errors import CommandNotFoundError


class UnitOfWork(object):
	"""The unit of work is an interface for the usage of the Unit of
	Work design pattern. Used to represent a bunch of commands that are to be
	executed together.

	Methods: __enter__, __exit__, commit, rollback, books
	"""
	def __enter__(self):
		"""Magic method for Python's 'with' usage. This command is executed
		whenever a new with is created for a unit of work."""
		pass

	def __exit__(self, type, value, traceback):
		"""Magic method for Python's 'with' usage. This command is executed
		whenever a with ends from a unit of work."""
		pass

	def commit(self):
		"""Used to store all changed data at database."""
		pass

	def rollback(self):
		"""Used to clear uncommited data."""
		pass

	@property
	def books(self) -> BookRepository:
		"""A convenient access for the Book repository.

		Returns
		-------
		book_repository: BookRepository -- an instance of a BookRepository for
		data mutation
		"""
		pass


class UnitOfWorkManager(object):
	"""The unit of work manager is an interface for the usage of the Unit of
	Work design pattern. Used to instantiate new units of work.

	Methods: start
	"""
	def start(self) -> UnitOfWork:
		"""The manager creates an instance of a UnitOfWork for database usage.

		Returns
		-------
		unit_of_work: UnitOfWork -- a unit of work for database context
		management
		"""
		pass


"""The handlers are responsible for the command's logic. For each command
there is a handler that can solve it using its parameters.
"""
def register_book_command_handler(uowm: UnitOfWorkManager,
								  cmd: RegisterBookCommand):
	"""Handler for the registering of a new book.

	Params
	------
	uowm: UnitOfWorkManager -- a unit of work manager to handle database access
	cmd: RegisterBookCommand -- the expected register book command
	"""
	with uowm.start() as uow:
		book = Book(cmd.isbn, cmd.name, cmd.author, cmd.content)
		uow.books.save(book)
		uow.commit()


def read_book_command_handler(view: BookView, cmd: ReadBookCommand):
	"""Handler for getting the content of a chosen book.

	Params
	------
	view: BookView -- a view to handle database queries
	cmd: ReadBookCommand -- the expected read book command
	"""
	book = view.get_by_isbn(cmd.isbn)

	if book is not None:
		return book.content
	else:
		return None


def view_books_command_handler(view: BookView, cmd: ViewBooksCommand):
	"""Handler for getting all books.

	Params
	------
	view: BookView -- a view to handle database queries
	cmd: ViewBooksCommand -- the expected view books command
	"""
	return view.get_all()


def view_book_by_isbn_command_handler(view: BookView,
									  cmd: ViewBookByIsbnCommand):
	"""Handler for getting a book by its ISBN.

	Params
	------
	view: BookView -- a view to handle database queries
	cmd: ViewBookByIsbnCommand -- the expected view book by ISBN command
	"""
	return view.get_by_isbn(cmd.isbn)


def view_book_by_name_command_handler(view: BookView,
									  cmd: ViewBooksByNameCommand):
	"""Handler for getting all books by their names.

	Params
	------
	view: BookView -- a view to handle database queries
	cmd: ViewBooksByNameCommand -- the expected view books by name command
	"""
	return view.get_by_name(cmd.name)


def view_book_by_author_command_handler(view: BookView,
										cmd: ViewBooksByAuthorCommand):
	"""Handler for getting all books by their author.

	Params
	------
	view: BookView -- a view to handle database queries
	cmd: ViewBooksByAuthorCommand -- the expected view books by author command
	"""
	return view.get_by_author(cmd.author)


class CommandBus(object):
	"""The command bus was developed following the Command Bus design pattern.
	It is responsible for the execution of commands by running the
	corresponding handler of a chosen command.

	Methods: dispatch
	"""
	def __init__(self, uowm: UnitOfWorkManager, view: BookView):
		"""CommandBus's constructor. Creates a map of 1:1 command to handler
		relationships.

		Params
		------
		uowm: UnitOfWorkManager -- an implementation of UnitOfWorkManager for
		data mutation
		view: BookView -- an implementation of BookView for data querying
		"""
		self.uowm = uowm
		self.view = view

		self.command_handler_map = {
			'RegisterBookCommand': register_book_command_handler,
			'ReadBookCommand': read_book_command_handler,
			'ViewBooksCommand': view_books_command_handler,
			'ViewBookByIsbnCommand': view_book_by_isbn_command_handler,
			'ViewBooksByNameCommand': view_book_by_name_command_handler,
			'ViewBooksByAuthorCommand': view_book_by_author_command_handler
		}

	def dispatch(self, command):
		"""Responsible for mapping the chosen command to a handler and
		executing it.

		Params
		------
		command -- an existing command of the application's API 
		"""
		command_name = command.__class__.__name__
		handler = self.command_handler_map.get(command_name)

		if handler is not None:
			if command_name == 'RegisterBookCommand':
				handler(self.uowm, command)
			else:
				return handler(self.view, command)
		else:
			raise CommandNotFoundError('the command \'{0}\' doesn\'t exist.' \
									   .format(command_name))
