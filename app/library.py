"""
	This module holds the application's business logic (the handling of books)
and has tools to deal with the 'ports' aspect of the architecture by using
development patterns like CommandBus and CQRS.
	As both business logic and ports are aspects of the application it is
difficult to create a logical separation.
"""

class Book(object):
	"""A model class for the creation of Book objects."""
	def __init__(self, name, author):
		"""Book class constructor."""
		self.name = name
		self.author = author

class QueryBook(Book):
	"""A query model class for Book objects."""
