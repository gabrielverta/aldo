# -*- cod: utf-8 -*-

from decorator import aldo


@aldo
def without_parameters():
	"""
		Function without parameters with comments
	"""
	return True

class Foo:
	pass

class Bar:
	def __init__(self, foo: Foo):
		self.foo = foo

class Baz:
	pass

@aldo
def with_parameters(foo: Foo):
	return foo


@aldo
def with_parameters_forever(bar: Bar, baz: Baz):
	return (bar, baz)

def test_without_parameters():
	func = without_parameters
	assert("""
		Function without parameters with comments
	""" == func.__doc__)
	assert("without_parameters" == func.__name__)
	assert(True == func())


def test_with_parameters():
	response = with_parameters()
	assert(isinstance(response, Foo))


def test_with_parameters_forever():
	bar, baz = with_parameters_forever()
	assert(isinstance(bar, Bar))
	assert(isinstance(bar.foo, Foo))
	assert(isinstance(baz, Baz))

