# -*- coding: utf-8 -*-

from dependency_manager import Aldo
from tests.functions import without_parameters, with_named_parameters, with_recursive_parameters, Foo, Bar

def test_function_without_parameters():
	aldo = Aldo(without_parameters)
	parameters = aldo.parameters()
	assert(0 == len(parameters))
	assert(True == aldo())


def test_function_with_named_parameters():
	aldo = Aldo(with_named_parameters)
	parameters = aldo.parameters()
	assert(1 == len(parameters))
	response = aldo()
	assert(isinstance(response, Foo))


def test_function_with_recursive_parameters():
	aldo = Aldo(with_recursive_parameters)
	parameters = aldo.parameters()
	assert(1 == len(parameters))
	response = aldo()
	assert(isinstance(response, Bar))
	assert(isinstance(response.foo, Foo))
