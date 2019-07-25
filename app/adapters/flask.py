"""A Flask REST adapter to use as an interface for the application."""

from multiprocessing import Process

from flask import Flask
from flask_restful import Resource, Api, reqparse

from ..settings import identify
from ..domain.messages import RegisterBookCommand


class BookResource(Resource):
	"""Class to handle incoming REST requests concerning books.

	Extends: Resource
	"""
	def __init__(self, bus, view):
		"""BookResource's constructor.

		Params
		------
		bus -- the message bus to dispatch commands
		view -- the database view to access data
		"""
		self.bus = bus
		self.view = view

	def get(self) -> list:
		"""Returns list of all registered books at database."""
		return [b.__dict__ for b in self.view.get_all()]

	def post(self):
		"""Registers new book at database."""
		parser = reqparse.RequestParser()

		parser.add_argument(
			'isbn', type=str, help='book\'s unique identification'
		)
		parser.add_argument(
			'name', type=str, help='book\'s title'
		)
		parser.add_argument(
			'author', type=str,
			help='the name of the person who wrote the book'
		)
		parser.add_argument(
			'content', type=str, help='whats written on the book'
		)

		args = parser.parse_args(strict=True)

		cmd = RegisterBookCommand(
			args['isbn'], args['name'], args['author'], args['content'])

		try:
			self.bus.handle(cmd)
			return {'message': 'New book registered'}
		except:
			return {'error': 'ISBN already registered into another book'}, 401


@identify('flask', 'interface')
class Rest(object):
	"""Listens to incoming HTTP packages and executes the associated commands.

	Methods: set_message_bus, set_view, start, stop"""
	def __init__(self, cfg):
		"""Rest's constructor.

		Params
		------
		cfg: dict -- the REST adapter's configuration
		"""
		self.host = cfg['host']
		self.port = cfg['port']
		self.debug = cfg['debug']

		app = Flask(__name__)
		self.server = Process(target=app.run,
							  args=(self.host, self.port, self.debug))
		self.api = Api(app)

	def set_message_bus(self, bus):
		"""Sets the message bus to be used by the adapter to execute commands.

		Params
		------
		bus -- the message bus
		"""
		self.bus = bus

	def set_view(self, view):
		"""Sets the view used to read the database.

		Params
		------
		view -- the database view
		"""
		self.view = view

	def run(self):
		"""Method to initialize the adapter by starting the HTTP server."""
		self.api.add_resource(
			BookResource, '/books',
			resource_class_kwargs={'bus': self.bus, 'view': self.view}
		)

		self.server.start()
