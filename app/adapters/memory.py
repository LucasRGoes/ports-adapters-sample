"""A memory database adapter."""

from ..settings import identify
from ..domain.model import Book
from ..domain.ports import BookRepository, BookView, UnitOfWork, \
						   UnitOfWorkManager


BOOKS_STORAGE = {}


class MemoryBookRepository(BookRepository):
	"""An implementation of a BookRepository utilizing memory storage as a
	database for the application.

	Methods: save
	"""
	def __init__(self):
		"""MemoryBookRepository's constructor."""
		pass

	def save(self, book: Book):
		"""View @app.domain.ports.BookRepository."""
		BOOKS_STORAGE[book.isbn] = {'name': book.name, 'author': book.author,
									'content': book.content}


class MemoryBookView(BookView):
	"""An implementation of a BookView reading from a memory storage.

	Methods: get_all, get_by_isbn, get_by_name, get_by_author
	"""
	def __init__(self):
		"""MemoryBookView's constructor."""
		pass

	def get_all(self) -> list:
		"""View @app.domain.ports.BookView."""
		return [Book(key, value['name'], value['author'], value['content']) \
				for key, value in BOOKS_STORAGE.items()]

	def get_by_isbn(self, isbn: str) -> Book:
		"""View @app.domain.ports.BookView."""
		book = BOOKS_STORAGE.get(isbn)

		if book is not None:
			return Book(isbn, book['name'], book['author'], book['content'])
		else:
			return None

	def get_by_name(self, name: str) -> list:
		"""View @app.domain.ports.BookView."""
		books = []
		for key, value in BOOKS_STORAGE.items():
			if value['name'] == name:
				books.append(
					Book(key, value['name'], value['author'], value['content'])
				)

		return books

	def get_by_author(self, author: str) -> list:
		"""View @app.domain.ports.BookView."""
		books = []
		for key, value in BOOKS_STORAGE.items():
			if value['author'] == author:
				books.append(
					Book(key, value['name'], value['author'], value['content'])
				)

		return books


class MemoryUnitOfWork(UnitOfWork):
	"""An implementation of a UnitOfWork for a memory storage database.

	Methods: __enter__, __exit__, commit, rollback, books
	"""
	def __init__(self):
		"""MemoryUnitOfWork's constructor."""
		pass

	def __enter__(self):
		"""View @app.domain.ports.UnitOfWork."""
		return self

	def __exit__(self, type, value, traceback):
		"""View @app.domain.ports.UnitOfWork."""
		pass

	def commit(self):
		"""View @app.domain.ports.UnitOfWork."""
		pass

	def rollback(self):
		"""View @app.domain.ports.UnitOfWork."""
		pass

	@property
	def books(self) -> BookRepository:
		"""View @app.domain.ports.UnitOfWork."""
		return MemoryBookRepository()


class MemoryUnitOfWorkManager(UnitOfWorkManager):
	"""An implementation of a UnitOfWorkManager for memory storage.

	Methods: start
	"""
	def __init__(self):
		"""MemoryUnitOfWorkManager's constructor."""
		pass

	def start(self) -> MemoryUnitOfWork:
		"""View @app.domain.ports.UnitOfWorkManager."""
		return MemoryUnitOfWork()


@identify('memory', 'database')
class MemoryAdapter(object):
	"""The adapter class to be used by the application. It gives access to
	each of the memory database classes that are to be used by the app.

	Methods: get_uowm, get_view
	"""
	def __init__(self, cfg: dict):
		"""MemoryAdapter's constructor.

		cfg: dict -- The memory adapter's configuration
		"""
		pass

	def get_uowm(self):
		"""Returns an instance of a MemoryUnitOfWorkManager.

		Returns
		-------
		uowm: MemoryUnitOfWorkManager
		"""
		return MemoryUnitOfWorkManager()

	def get_view(self):
		"""Returns an instance of a MemoryBookView.

		Returns
		-------
		view: MemoryBookView
		"""
		return MemoryBookView()
