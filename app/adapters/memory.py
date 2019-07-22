"""A memory driver adapter for data storage."""

from ..logic import Book
from ..ports import BookStorage

class MemoryAdapter(BookStorage):
	"""A memory adapter class that implements the BookStorage from ports using the Repository pattern."""
	def __init__(self):
		"""MemoryAdapter's constructor."""
		self.books = {}

	def register(self, book: Book):
		"""Registers a new book at database.
	
		Params
		------
		book: Book -- the book to be stored
		"""
		has_book = self.books.get(book.isbn)

		if has_book is not None:
			self.books[book.isbn]['total'] += 1
		else:
			self.books[book.isbn] = {'author': book.author, 'name': book.name,
									 'total': 1, 'lent': 0}

	def borrow(self, isbn: str):
		"""'Borrows' a book from database.

		Params
		------
		isbn: str -- the isbn of the book to borrow
		"""