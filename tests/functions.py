# -*- coding: utf-8 -*-

def without_parameters():
	return True


class Foo:
	pass

class Bar:
	def __init__(self, foo: Foo):
		self.foo = foo

def with_named_parameters(foo: Foo):
	return foo

def with_recursive_parameters(bar: Bar):
	return bar