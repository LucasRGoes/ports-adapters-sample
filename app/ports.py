""""""

class BookCommand(object):
	"""Generic command that handles books. Further command classes should
	extend this class."""
	def __init__(self):
		"""BookCommand's constructor."""
		pass


class RegisterBookCommand(BookCommand):
	"""Command for registering a new book at the library."""
	def __init__(self, author: str, isbn: str, name: str):
		"""RegisterBookCommand's constructor."""
		self.author = author
		self.isbn = isbn
		self.name = name


class BorrowBookCommand(BookCommand):
	"""Command for borrowing a book from the library."""
	def __init__(self, isbn: str):
		"""BorrowBookCommand's constructor."""
		self.isbn = isbn


class ReturnBookCommand(BookCommand):
	"""Command for returning a book to the library."""
	def __init__(self, isbn: str):
		"""ReturnBookCommand's constructor."""
		self.isbn = isbn


def register_book_handler(command: RegisterBookCommand):
	"""Handler for the registering of a new book at the library."""
	print('Hello 1')
	return True


def borrow_book_handler(command: BorrowBookCommand):
	"""Handler for the borrowing of a book from the library."""
	print('Hello 2')
	return True


def return_book_handler(command: ReturnBookCommand):
	"""Handler for the returning of a book to the library."""
	print('Hello 3')
	return True


class StandardCommandBus(object):
	"""The command bus is responsible for all of the commands to be executed.
	"""
	def __init__(self):
		"""StandardCommandBus's constructor. Creates a command handler map to
		know which handler can work with which command. The relationship is
		always 1:1."""
		self.command_handler_map = {
			'RegisterBookCommand': register_book_handler,
			'BorrowBookCommand': borrow_book_handler,
			'ReturnBookCommand': return_book_handler
		}

	def dispatch(self, command: BookCommand):
		handler = self.command_handler_map[command.__class__.__name__]
		return handler(command)
