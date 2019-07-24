"""
Errors
======
	The application's source of exception classes.

Classes: CommandAlreadySubscribedError
"""

class CommandAlreadySubscribedError(Exception):
	"""To be raised when a handler subscribes to a command that a message bus has already associated with another handler.

	Extends: Exception
	"""
	pass
