"""A SQLite database adapter."""

import logging
import sqlite3

from ..settings import identify
from ..domain.model import Book
from ..domain.ports import BookRepository, BookView, UnitOfWork, \
						   UnitOfWorkManager


LOGGER = logging.getLogger('sample')


class SqliteBookRepository(BookRepository):
	"""An implementation of a BookRepository utilizing SQLite as a database
	for the application.

	Methods: save
	"""
	def __init__(self, cursor):
		"""SqliteBookRepository's constructor."""
		self.cursor = cursor

	def save(self, book: Book):
		"""View @app.domain.ports.BookRepository."""
		LOGGER.debug('Saving book: {0} ...'.format(book.__repr__()))
		self.cursor.execute("""
			INSERT INTO books (isbn, name, author, content)
			VALUES (?, ?, ?, ?);
		""", (book.isbn, book.name, book.author, book.content))


class SqliteBookView(BookView):
	"""An implementation of a BookView reading from a SQLite storage.

	Methods: get_all, get_by_isbn, get_by_name, get_by_author
	"""
	def __init__(self, location):
		"""SqliteBookView's constructor."""
		self.location = location

	def get_all(self) -> list:
		"""View @app.domain.ports.BookView."""
		conn = sqlite3.connect(self.location)
		cursor = conn.cursor()

		books = cursor.execute('SELECT * FROM books;').fetchall()

		conn.close()

		return [Book(i[0], i[1], i[2], i[3]) for i in books]

	def get_by_isbn(self, isbn: str) -> Book:
		"""View @app.domain.ports.BookView."""
		conn = sqlite3.connect(self.location)
		cursor = conn.cursor()

		book = cursor.execute(
			'SELECT * FROM books WHERE isbn=\'{0}\';'.format(isbn)).fetchone()

		conn.close()

		return Book(book[0], book[1], book[2], book[3])

	def get_by_name(self, name: str) -> list:
		"""View @app.domain.ports.BookView."""
		conn = sqlite3.connect(self.location)
		cursor = conn.cursor()

		books = cursor.execute(
			'SELECT * FROM books WHERE name=\'{0}\';'.format(name)).fetchall()

		conn.close()

		return [Book(i[0], i[1], i[2], i[3]) for i in books]

	def get_by_author(self, author: str) -> list:
		"""View @app.domain.ports.BookView."""
		conn = sqlite3.connect(self.location)
		cursor = conn.cursor()

		books = cursor.execute(
			'SELECT * FROM books WHERE author=\'{0}\';'.format(author)
		).fetchall()

		conn.close()

		return [Book(i[0], i[1], i[2], i[3]) for i in books]


class SqliteUnitOfWork(UnitOfWork):
	"""An implementation of a UnitOfWork for a SQLite storage database.

	Methods: __enter__, __exit__, commit, rollback, books
	"""
	def __init__(self, location):
		"""SqliteUnitOfWork's constructor."""
		self.location = location

	def __enter__(self):
		"""View @app.domain.ports.UnitOfWork."""
		self.conn = sqlite3.connect(self.location)
		return self

	def __exit__(self, type, value, traceback):
		"""View @app.domain.ports.UnitOfWork."""
		self.conn.close()

	def commit(self):
		"""View @app.domain.ports.UnitOfWork."""
		self.conn.commit()

	def rollback(self):
		"""View @app.domain.ports.UnitOfWork."""
		self.conn.rollback()

	@property
	def books(self) -> SqliteBookRepository:
		"""View @app.domain.ports.UnitOfWork."""
		return SqliteBookRepository(self.conn.cursor())


class SqliteUnitOfWorkManager(UnitOfWorkManager):
	"""An implementation of a UnitOfWorkManager for SQLite storage.

	Methods: start
	"""
	def __init__(self, location: str):
		"""SqliteUnitOfWorkManager's constructor.

		Params
		------
		location: str -- the location where the adapter should store the
		SQLite database
		"""
		self.location = location

	def start(self) -> SqliteUnitOfWork:
		"""View @app.domain.ports.UnitOfWorkManager."""
		return SqliteUnitOfWork(self.location)


@identify('sqlite', 'database')
class SqliteDatabase(object):
	"""This adapter gives access to each of the SQLite database classes that
	are to be used by the app for data mutation an querying.

	Methods: get_uowm, get_view
	"""
	def __init__(self, cfg: dict):
		"""SqliteDatabase's constructor.

		cfg: dict -- The SQLite database adapter's configuration
		"""
		self.location = cfg['location']

	def set_up(self):
		"""Configures the database creating its tables if necessary."""
		conn = sqlite3.connect(self.location)
		cursor = conn.cursor()

		books = cursor.execute("""
			CREATE TABLE IF NOT EXISTS 'books' (
				isbn TEXT PRIMARY KEY,
				name TEXT NOT NULL,
				author TEXT NOT NULL,
				content TEXT NOT NULL
			);
		""")

		conn.close()

	def get_uowm(self) -> SqliteUnitOfWorkManager:
		"""Returns an instance of a SqliteUnitOfWorkManager."""
		return SqliteUnitOfWorkManager(self.location)

	def get_view(self) -> SqliteBookView:
		"""Returns an instance of a SqliteBookView."""
		return SqliteBookView(self.location)

