"""
Business Logic
==============
	The business logic is the domain of the application as it contains models
and logic concerning the application's problems.
"""


class Book:
	"""Model class to represent the main business aspect of this sample
	application: books.
	"""
	def __init__(self, author: str, isbn: str, name: str):
		"""Book's constructor.

		Params
		------
		author: str -- the book's author
		isbn: str -- the book's unique identification
		name: str -- the book's name
		"""
		self.author = author
		self.isbn = isbn
		self.name = name
