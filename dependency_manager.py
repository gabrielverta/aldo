# -*- cod: utf-8 -*-

class Aldo:
	"""
		Aldo dependency manager
	"""

	def __init__(self, func):
		"""
			Function to handle dependencies
		"""
		self.func = func

	def parameters(self):
		"""
			Returns list of parameters required for func
		"""
		try:
			return self.func.__annotations__
		except AttributeError:
			pass

		try:
			return self.func.__init__.__annotations__
		except AttributeError:
			pass

		return {}

	def __call__(self):
		"""
			Call handled function using parameters
		"""
		args = []
		kwargs = {}

		parameters = self.parameters()
		for key in parameters:
			kwargs[key] = self.handle(parameters[key])

		return self.func(*args, **kwargs)

	def handle(self, klass):
		"""
			Handle new instances of klass and dependencies
		"""
		return Aldo(klass)()
