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
from .domain.ports import BookView, UnitOfWorkManager, QueueSender, MessageBus
from .domain.messages import RegisterBookCommand, BookRegisteredEvent


class RegisterBookHandler(object):
	"""Created to handle the command RegisterBookCommand.

	Methods: handle
	"""
	def __init__(self, bus: MessageBus, uowm: UnitOfWorkManager):
		"""RegisterBookHandler's constructor.

		Params
		------
		bus: MessageBus -- the message bus that can handle generated events
		uowm: UnitOfWorkManager -- the manager used to create new units of work
		"""
		self.bus = bus
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

		self.bus.handle(BookRegisteredEvent(book.isbn))


class BookRegisteredHandler(object):
	"""Created to handle the event BookRegisteredEvent.

	Methods: handle
	"""
	def __init__(self, view: BookView, sender: QueueSender):
		"""BookRegisteredHandler's constructor.

		Params
		------
		view: BookView -- the view used to query the database
		sender: QueueSender -- the sender to dispatch messages
		"""
		self.view = view
		self.sender = sender

	def handle(self, event: BookRegisteredEvent):
		"""Handles sending the book registered event.

		Params
		------
		event: BookRegisteredEvent -- the expected book registered event
		"""
		book = self.view.get_by_isbn(event.isbn)
		self.sender.send('{0} has been successfully registered.' \
						 .format(book.__repr__()))
