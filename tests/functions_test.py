# -*- coding: utf-8 -*-

import pytest
from dependency_manager import Aldo
from tests.functions import without_parameters, with_named_parameters, with_recursive_parameters, with_positional_parameters, Foo, Bar

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


def test_class_without_parameters():
	aldo = Aldo(Foo)
	parameters = aldo.parameters()
	assert(0 == len(parameters))
	response = aldo()
	assert(isinstance(response, Foo))


def test_class_without_parameters():
	aldo = Aldo(Bar)
	parameters = aldo.parameters()
	assert(1 == len(parameters))
	response = aldo()
	assert(isinstance(response, Bar))
	assert(isinstance(response.foo, Foo))


def test_with_positional_parameters():
	aldo = Aldo(with_positional_parameters)
	parameters = aldo.parameters()
	assert(0 == len(parameters))
	with pytest.raises(TypeError):
		aldo()


def test_with_known_positional_parameters():
	aldo = Aldo(with_positional_parameters, first = 10, second = 20)
	parameters = aldo.parameters()
	assert(0 == len(parameters))
	first, second = aldo()
	assert(10 == first)
	assert(20 == second)