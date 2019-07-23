"""
Domain
======
	The domain covers all aspects of the application's business logic, holding
book models, the commands associated with the application and interfaces for
repositories and events.

OBS: A good practice is remembering that business logic should always consider
all of the business problems, so being able to solve every aspect of those
problems in the domain and not raising errors so that other modules solve them
is important.

Models: Book

Commands: RegisterBookCommand, ReadBookCommand, ViewBooksCommand,
ViewBookByIsbnCommand, ViewBooksByNameCommand, ViewBooksByAuthorCommand

Interfaces: BookRepository, BookView
"""

from collections import namedtuple


class Book(object):
	"""Model class to represent the main business aspect of this sample
	application: books.
	"""
	def __init__(self, isbn: str, name: str, author: str, content: str):
		"""Book's constructor.

		Params
		------
		isbn: str -- book's unique identification
		name: str -- book's title
		author: str -- the name of the person who wrote the book
		content: str -- whats written on the book
		"""
		self.isbn = isbn
		self.name = name
		self.author = author
		self.content = content


"""
	These are the application's commands, or its API (Application Programming
Interface). Simple objects that holds the necessary information for the
commands to be executed following the Commands and Handlers design pattern.

	The commands are the application's ports for driver actors and driver
adapters, so they should always be named by actions that represent important
use cases of the application.

	The idea is that driver adapters communicate with the application in a 
technology agnostic way by utilizing these commands.
"""
RegisterBookCommand = namedtuple(
	'RegisterBookCommand', ['isbn', 'name', 'author', 'content'])

ReadBookCommand = namedtuple('ReadBookCommand', ['isbn'])

ViewBooksCommand = namedtuple('ViewBooksCommand', [])

ViewBookByIsbnCommand = namedtuple('ViewBookByIsbnCommand', ['isbn'])

ViewBooksByNameCommand = namedtuple('ViewBooksByNameCommand', ['name'])

ViewBooksByAuthorCommand = namedtuple('ViewBooksByAuthorCommand', ['author'])


"""
	These are the interfaces for repository driven adapters to implement, or
the application's SPI for data storage and query.

	For data storage the Repository design pattern is used, while for data
querying the CQRS design pattern is considered, separating queries from data
creation, update and deletion.
"""
class BookRepository(object):
	"""BookRepository is an interface for driven adapters that communicate with
	databases concerning data mutation methods.

	Methods: save
	"""
	def save(self, book: Book):
		"""Method to be implemented to save books to the database.

		Params
		------
		book: Book -- the book to be inserted on the application's database
		"""
		pass


class BookView(object):
	"""BookView is an interface for driven adapters that communicate with
	databases concerning data querying methods.

	Methdos: get_all, get_by_isbn, get_by_name, get_by_author
	"""
	def get_all(self) -> list:
		"""Method to be implemented to fetch all books from the database.

		Returns
		-------
		books: list -- a list of all books at database
		"""
		pass

	def get_by_isbn(self, isbn: str) -> Book:
		"""Method to be implemented to fetch a book by its ISBN from the
		database.

		Params
		------
		isbn: str -- the ISBN of the book to be fetched

		Returns
		-------
		book: Book -- the book with the chosen ISBN
		"""
		pass

	def get_by_name(self, name: str) -> list:
		"""Method to be implemented to fetch all books with a certain name
		from the database.

		Params
		------
		name: str -- the name of the books to be fetched

		Returns
		-------
		books: list -- a list of all books with the chosen name at database
		"""
		pass

	def get_by_author(self, author: str) -> list:
		"""Method to be implemented to fetch all books of a certain author
		from the database.

		Params
		------
		author: str -- the name of the author from the books to be fetched

		Returns
		-------
		books: list -- a list of all books written by the author at database
		"""
		pass
