# -*- coding: utf-8 -*-

from aldo.dependency_manager import Aldo
from aldo.exceptions import AldoRedirect
from functools import wraps


def aldo(func):
    """
        Aldo dependency manager decorator
        :param func: function or class that needs to be handled
        :return: execute func filling parameters
    """
    @wraps(func)
    def run(*args, **kwargs):
        try:
            return Aldo(func, *args, **kwargs)()
        except AldoRedirect as redirect:
            return redirect.response
    run._original_ = func
    return run


def teach(klass, params=False):
    """
        Decorator to teach aldo how to create an instance of a class
        :param klass: class to create an instance
        :param params: either to remove aldo parameters when calling function or not
            (history of instances created and function or class being resolved)
        :return: view
    """
    def execute(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not params:
                remove_parameters(kwargs)
            return func(*args, **kwargs)
        Aldo.bind(klass, wrapper)
        return wrapper

    return execute

def remove_parameters(kwargs):
    """
    Remove aldo parameters (history and function/class being handled
    :param kwargs: parameters
    :return: None
    """
    try:
        del(kwargs['__origin'])
    except KeyError:
        pass

    try:
        del(kwargs['aldo_context'])
    except KeyError:
        pass

