"""The application's source of exception classes.

Classes: GenericApplicationError, CommandNotFoundError
"""

class GenericApplicationError(Exception):
	"""Generic error to be implemented by further classes in order to uncouple
	the application's exceptions from others.

	Extends: Exception
	"""
	pass


class CommandNotFoundError(GenericApplicationError):
	"""To be raised when a non existant command is inserted into the command
	bus.

	Extends: GenericApplicationError
	"""
	pass
