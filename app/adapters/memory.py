"""A memory driven adapter for data storage."""

from ..domain import Book, BookRepository, BookView
from ..controller import UnitOfWorkManager, UnitOfWork


BOOKS_STORAGE = {}


class MemoryBookRepository(BookRepository):
	"""An implementation of a BookRepository with memory storage.

	Methods: save
	"""
	def __init__(self):
		"""MemoryBookRepository's constructor."""
		pass

	def save(self, book: Book):
		"""View @domain.BookRepository."""
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
		"""View @domain.BookView."""
		return [Book(key, value['name'], value['author'], value['content']) \
				for key, value in BOOKS_STORAGE.items()]

	def get_by_isbn(self, isbn: str) -> Book:
		"""View @domain.BookView."""
		book = BOOKS_STORAGE.get(isbn)

		if book is not None:
			return Book(isbn, book['name'], book['author'], book['content'])
		else:
			return None

	def get_by_name(self, name: str) -> list:
		"""View @domain.BookView."""
		books = []
		for key, value in BOOKS_STORAGE.items():
			if value['name'] == name:
				books.append(
					Book(key, value['name'], value['author'], value['content'])
				)

		return books

	def get_by_author(self, author: str) -> list:
		"""View @domain.BookView."""
		books = []
		for key, value in BOOKS_STORAGE.items():
			if value['author'] == author:
				books.append(
					Book(key, value['name'], value['author'], value['content'])
				)

		return books


class MemoryUnitOfWork(UnitOfWork):
	"""An implementation of a UnitOfWork for memory storage.

	Methods: __enter__, __exit__, commit, rollback, books
	"""
	def __init__(self):
		"""MemoryUnitOfWork's constructor."""
		pass

	def __enter__(self):
		"""View @controller.UnitOfWork."""
		return self

	def __exit__(self, type, value, traceback):
		"""View @controller.UnitOfWork."""
		pass

	def commit(self):
		"""View @controller.UnitOfWork."""
		pass

	def rollback(self):
		"""View @controller.UnitOfWork."""
		pass

	@property
	def books(self) -> BookRepository:
		"""View @controller.UnitOfWork."""
		return MemoryBookRepository()


class MemoryUnitOfWorkManager(UnitOfWorkManager):
	"""An implementation of a UnitOfWorkManager for memory storage.

	Methods: start
	"""
	def __init__(self):
		"""MemoryUnitOfWorkManager's constructor."""
		pass

	def start(self) -> UnitOfWork:
		"""View @controller.UnitOfWorkManager."""
		return MemoryUnitOfWork()
