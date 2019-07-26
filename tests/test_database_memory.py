"""Unit tests of the application's adapter memory.py functions."""

import unittest

from app.domain.model import Book
from app.adapters.memory import MemoryDatabase


class TestAdaptersMemoryBookRepository(unittest.TestCase):
	"""Set of unit tests for the memory.py MemoryBookRepository class and its
	implementations.

	Tests: test_save
	"""
	def test_save(self):
		"""Steps:
		1 - Instantiates a MemoryDatabase
		2 - Creates an unit of work to handle the saving of a book
		3 - Verifies through view if the book has been saved
		"""
		memory = MemoryDatabase({})
		memory.set_up()

		uowm = memory.get_uowm()
		view = memory.get_view()

		book = Book('isbn', 'name', 'author', 'content')

		with uowm.start() as uow:
			uow.books.save(book)

		self.assertEqual(book, view.get_by_isbn('isbn'))


class TestAdaptersMemoryBookView(unittest.TestCase):
	"""Set of unit tests for the memory.py MemoryBookView class and its
	implementations.

	Tests: test_get_all, test_get_by_name, test_get_by_author
	"""
	def test_get_all(self):
		"""Steps:
		1 - Instantiates a MemoryDatabase
		2 - Creates an unit of work to handle the saving of three books
		3 - Fetches all books and verifies if they are the same
		"""
		memory = MemoryDatabase({})
		memory.set_up()

		uowm = memory.get_uowm()
		view = memory.get_view()

		book1 = Book('isbn-1234', 'name1', 'author1', 'content1')
		book2 = Book('isbn-2345', 'name1', 'author2', 'content2')
		book3 = Book('isbn-3456', 'name2', 'author1', 'content3')

		with uowm.start() as uow:
			uow.books.save(book1)
			uow.books.save(book2)
			uow.books.save(book3)

		books = view.get_all()
		self.assertTrue(len(books) == 3)

		s_book1, s_book2, s_book3 = books
		self.assertEqual(book1, s_book1)
		self.assertEqual(book2, s_book2)
		self.assertEqual(book3, s_book3)

	def test_get_by_name(self):
		"""Steps:
		1 - Instantiates a MemoryDatabase
		2 - Creates an unit of work to handle the saving of three books
		3 - Fetches books by 'name1' and verifies if they are the same
		3 - Fetches books by 'name2' and verifies if they are the same
		"""
		memory = MemoryDatabase({})
		memory.set_up()

		uowm = memory.get_uowm()
		view = memory.get_view()

		book1 = Book('isbn-1234', 'name1', 'author1', 'content1')
		book2 = Book('isbn-2345', 'name1', 'author2', 'content2')
		book3 = Book('isbn-3456', 'name2', 'author1', 'content3')

		with uowm.start() as uow:
			uow.books.save(book1)
			uow.books.save(book2)
			uow.books.save(book3)

		books = view.get_by_name('name1')
		self.assertEqual(len(books), 2)

		s_book1, s_book2 = books
		self.assertEqual(book1, s_book1)
		self.assertEqual(book2, s_book2)

		books = view.get_by_name('name2')
		self.assertEqual(len(books), 1)

		s_book3 = books[0]
		self.assertEqual(book3, s_book3)

	def test_get_by_author(self):
		"""Steps:
		1 - Instantiates a MemoryDatabase
		2 - Creates an unit of work to handle the saving of three books
		3 - Fetches books by 'author1' and verifies if they are the same
		3 - Fetches books by 'author2' and verifies if they are the same
		"""
		memory = MemoryDatabase({})
		memory.set_up()

		uowm = memory.get_uowm()
		view = memory.get_view()

		book1 = Book('isbn-1234', 'name1', 'author1', 'content1')
		book2 = Book('isbn-2345', 'name1', 'author2', 'content2')
		book3 = Book('isbn-3456', 'name2', 'author1', 'content3')

		with uowm.start() as uow:
			uow.books.save(book1)
			uow.books.save(book2)
			uow.books.save(book3)

		books = view.get_by_author('author1')
		self.assertEqual(len(books), 2)

		s_book1, s_book3 = books
		self.assertEqual(book1, s_book1)
		self.assertEqual(book3, s_book3)

		books = view.get_by_author('author2')
		self.assertEqual(len(books), 1)

		s_book2 = books[0]
		self.assertEqual(book2, s_book2)


if __name__ == '__main__':
	unittest.main()
