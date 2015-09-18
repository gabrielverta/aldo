# -*- coding: utf-8 -*-

import os, sys

sys.path.insert(0, os.path.realpath('../.'))

from aldo.decorator import aldo, teach, Aldo
from aldo.exceptions import AldoRedirect


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
        assert(not "aldo_context" in kwargs)
        return RedisCache()

    manager = Aldo(Cache)
    cache = manager()
    assert(isinstance(cache, RedisCache))


def test_teaching_with_context():
    Aldo.bindings = {}

    @aldo
    def my_view(foo: Foo, bar: Bar):
        return foo, bar

    @teach(Bar, params=True)
    def bar_factory(aldo_context, *args, **kwargs):
        return Bar(aldo_context['foo'])

    foo, bar = my_view()
    assert(isinstance(bar, Bar))
    assert(isinstance(foo, Foo))
    assert(foo == bar.foo)


def test_redirect():
    Aldo.bindings = {}

    @aldo
    def my_view(foo: Foo):
        return foo

    @teach(Foo)
    def foo_factory(*args, **kwargs):
        raise AldoRedirect("BAR")

    response = my_view()
    assert("BAR" == response)


def test_aldo_on_a_function_with_aldo():
    Aldo.bindings = {}

    @aldo
    def my_view(foo: Foo):
        return foo

    handler = Aldo(my_view)
    response = handler()
    assert(isinstance(response, Foo))


def test_aldo_after_redirect():
    Aldo.bindings = {}

    @aldo
    def first_view(request, foo: Foo):
        raise Exception("Flow should not enter here")

    @aldo
    def second_view(request):
        return 'second view {}'.format(request)

    def redirect(*args, **kwargs):
        assert(len(args) == 1)
        assert(args[0] == 'title')
        handler = Aldo(second_view, *args, **kwargs)
        response = handler()
        assert('second view title' == response)
        return response

    @teach(Foo)
    def foo_factory(request, *args, **kwargs):
        raise AldoRedirect(redirect(request, *args, **kwargs))


    response = first_view('title')
    assert(isinstance(response, str))
    assert('second view title' == response)