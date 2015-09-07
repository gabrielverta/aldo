# -*- coding: utf-8 -*-

import inspect


class Aldo:
	"""
		Aldo dependency manager
	"""

	def __init__(self, func, *args, **kwargs):
		"""
			Function to handle dependencies
		"""
		self.func = func
		self.args = args
		self.kwargs = kwargs
		self.bindings = {}

	def bind(self, klass, factory):
		"""
			Add a factory for new instances of klass
		"""
		self.bindings[klass] = factory

	def parameters(self):
		"""
			Returns list of parameters required for func
		"""
		return inspect.getfullargspec(self.func)

	def __call__(self):
		"""
			Call handled function using parameters
		"""
		for bind in self.bindings:
			if issubclass(self.func, bind):
				return self.bindings[bind](*self.args, **self.kwargs)

		kwargs = {}
		args = []

		parameters = self.parameters()
		for key in parameters.annotations:
			kwargs[key] = self.handle(parameters.annotations[key])

		pending = [arg for arg in parameters.args if not arg in kwargs]
		for arg in pending:
			if arg in self.kwargs:
				kwargs[arg] = self.kwargs[arg]

		args = self.args[:len(pending)]

		return self.func(*args, **kwargs)


	def handle(self, klass):
		"""
			Handle new instances of klass and dependencies
		"""
		return Aldo(klass, *self.args, **self.kwargs)()
