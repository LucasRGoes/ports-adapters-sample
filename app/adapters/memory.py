"""A memory driven adapter for data storage."""

from ..logic import Book
from ..ports import BookRepository


class MemoryRepository(BookRepository):
	"""A memory adapter class that implements the BookRepository from ports
	that uses the Repository pattern.

	Extends: BookRepository

	Methods: add_new_book, borrow_book, return_book
	"""
	def __init__(self):
		"""MemoryRepository's constructor."""
		self.books = {}

	def add_new_book(self, book: Book):
		"""View @BookRepository.add_new_book"""
		has_book = self.books.get(book.isbn)

		if has_book is not None:
			self.books[book.isbn]['total'] += 1
		else:
			self.books[book.isbn] = {'author': book.author, 'name': book.name,
									 'total': 1, 'lent': 0}

	def borrow_book(self, isbn: str):
		"""View @BookRepository.borrow_book"""
		book_data = self.books.get(book.isbn)

		if book_data is not None and :
			self.books[book.isbn]['lent'] += 1
			return Book(book_data.get('author'), isbn, book_data.get('name'))
		else:
			return None


	def return_book(self, isbn: str):
		"""View @BookRepository.return_book"""
		pass
