"""The application's source of exception classes.

Classes: SampleError, CommandNotFoundError.
"""

class SampleError(Exception):
	"""Generic error to be implemented by further classes in order to uncouple
	the application's exceptions from others.
	"""
	pass


class CommandNotFoundError(SampleError):
	"""To be raised when a non existant command is inserted into the command
	bus.

	Extends: SampleError.
	"""
	pass
