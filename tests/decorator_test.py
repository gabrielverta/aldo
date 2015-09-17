# -*- coding: utf-8 -*-

import os, sys

sys.path.insert(0, os.path.realpath('../.'))

from aldo.decorator import aldo, teach, Aldo


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
	@aldo
	def save(self, foo: Foo):
		return foo

	@aldo
	def extra(self, bar, foo: Foo):
		return foo, bar


class Cache:
    pass

class RedisCache(Cache):
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


def test_with_class_method():
	baz = Baz()
	foo = baz.save()
	assert(isinstance(foo, Foo))

	foo, bar = baz.extra('bla')
	assert(isinstance(foo, Foo))
	assert('bla' == bar)

	foo, bar = baz.extra(bar='bla')
	assert(isinstance(foo, Foo))
	assert('bla' == bar)


def test_with_all_parameters_sent():
	baz = Baz()
	foo, bar = baz.extra('bar', 'foo')
	assert('foo' == foo)
	assert('bar' == bar)


def test_teach_decorator():
    Aldo.bindings = {}

    @teach(Cache)
    def cache_factory(*args, **kwargs):
        return RedisCache()

    manager = Aldo(Cache)
    cache = manager()
    assert(isinstance(cache, RedisCache))