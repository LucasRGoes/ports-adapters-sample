"""
Handlers
========
	The handlers are the "glue" code of the application. They are the ones
that are associated to commands and events and know how to handle them.

Classes: RegisterBookHandler, ReadBookHandler, ViewBooksHandler,
ViewBookByIsbnHandler, ViewBooksByNameHandler, ViewBooksByAuthorHandler,
BookRegisteredHandler
"""

from .domain.model import Book
from .domain.ports import BookView, UnitOfWorkManager
from .domain.messages import RegisterBookCommand, BookRegisteredEvent


class RegisterBookHandler(object):
	"""Created to handle the command RegisterBookCommand.

	Methods: handle
	"""
	def __init__(self, uowm: UnitOfWorkManager):
		"""RegisterBookHandler's constructor.

		Params
		------
		uowm: UnitOfWorkManager -- the manager used to create new units of work
		"""
		self.uowm = uowm

	def handle(self, cmd: RegisterBookCommand):
		"""Handles the registering of a new book.

		Params
		------
		cmd: RegisterBookCommand -- the expected register book command
		"""
		book = Book(cmd.isbn, cmd.name, cmd.author, cmd.content)

		with self.uowm.start() as uow:
			uow.books.save(book)
			uow.commit()

		return book


class BookRegisteredHandler(object):
	"""Created to handle the event BookRegisteredEvent.

	Methods: handle
	"""
	def __init__(self, view: BookView):
		"""BookRegisteredHandler's constructor.

		Params
		------
		view: BookView -- the view used to query the database
		"""
		self.view = view

	def handle(self, event: BookRegisteredEvent):
		"""Handles sending the book registered event.

		Params
		------
		event: BookRegisteredEvent -- the expected book registered event
		"""
		return None


# class ReadBookHandler(object):
# 	"""Created to handle the command ReadBookHandler.

# 	Methods: handle
# 	"""
# 	def __init__(self, view: BookView):
# 		"""RegisterBookHandler's constructor.

# 		Params
# 		------
# 		view: BookView -- the view used to query the database
# 		"""
# 		self.view = view

# 	def handle(self, cmd: ReadBookCommand):
# 		"""Handles getting the content of a chosen book.

# 		Params
# 		------
# 		cmd: ReadBookCommand -- the expected read book command
# 		"""
# 		book = self.view.get_by_isbn(cmd.isbn)

# 		if book is not None:
# 			return book.content
# 		else:
# 			return None


# class ViewBooksHandler(object):
# 	"""Created to handle the command ViewBooksHandler.

# 	Methods: handle
# 	"""
# 	def __init__(self, view: BookView):
# 		"""ViewBooksHandler's constructor.

# 		Params
# 		------
# 		view: BookView -- the view used to query the database
# 		"""
# 		self.view = view

# 	def handle(self, cmd: ViewBooksCommand):
# 		"""Handles getting all books.

# 		Params
# 		------
# 		cmd: ViewBooksCommand -- the expected view books command
# 		"""
# 		return self.view.get_all()


# class ViewBookByIsbnHandler(object):
# 	"""Created to handle the command ViewBookByIsbnCommand.

# 	Methods: handle
# 	"""
# 	def __init__(self, view: BookView):
# 		"""ViewBookByIsbnHandler's constructor.

# 		Params
# 		------
# 		view: BookView -- the view used to query the database
# 		"""
# 		self.view = view

# 	def handle(self, cmd: ViewBookByIsbnCommand):
# 		"""Handles getting a book by its ISBN.

# 		Params
# 		------
# 		cmd: ViewBookByIsbnCommand -- the expected view book by ISBN command
# 		"""
# 		return self.view.get_by_isbn(cmd.isbn)


# class ViewBooksByNameHandler(object):
# 	"""Created to handle the command ViewBooksByNameCommand.

# 	Methods: handle
# 	"""
# 	def __init__(self, view: BookView):
# 		"""ViewBooksByNameHandler's constructor.

# 		Params
# 		------
# 		view: BookView -- the view used to query the database
# 		"""
# 		self.view = view

# 	def handle(self, cmd: ViewBooksByNameCommand):
# 		"""Handles getting all books by their names.

# 		Params
# 		------
# 		cmd: ViewBooksByNameCommand -- the expected view books by name command
# 		"""
# 		return self.view.get_by_name(cmd.name)


# class ViewBooksByAuthorHandler(object):
# 	"""Created to handle the command ViewBooksByAuthorCommand.

# 	Methods: handle
# 	"""
# 	def __init__(self, view: BookView):
# 		"""ViewBooksByAuthorHandler's constructor.

# 		Params
# 		------
# 		view: BookView -- the view used to query the database
# 		"""
# 		self.view = view

# 	def handle(self, cmd: ViewBooksByAuthorCommand):
# 		"""Handles getting all books by their author.

# 		Params
# 		------
# 		cmd: ViewBooksByAuthorCommand -- the expected view books by author
# 		command
# 		"""
# 		return self.view.get_by_author(cmd.author)
