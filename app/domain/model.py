"""
Model
=====
	These are the models of the application. They should hold important data
and methods concerning the business logic.

Classes: Book
"""

class Book(object):
	"""Model class to represent the main business aspect of this sample
	application: books.
	"""
	def __init__(self, isbn: str, name: str, author: str, content: str):
		"""Book's constructor.

		Params
		------
		isbn: str -- book's unique identification
		name: str -- book's title
		author: str -- the name of the person who wrote the book
		content: str -- whats written on the book
		"""
		self.isbn = isbn
		self.name = name
		self.author = author
		self.content = content

	def __str__(self) -> str:
		"""End user's representation."""
		return ('My name is {0}, a book written by {1} with ISBN: {2}.'
				' Here is my content: {3}' \
				.format(self.name, self.author, self.isbn, self.content))

	def __repr__(self) -> str:
		"""Programmer's representation."""
		return 'Book(isbn={0}, name={1}, author={2}, content={3})' \
			   .format(self.isbn, self.name, self.author, self.content)
