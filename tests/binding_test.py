# -*- coding: utf-8 -*-

import os, sys

sys.path.insert(0, os.path.realpath('..'))

import pytest
from aldo.dependency_manager import Aldo


class Bar:
	def __init__(self, place):
		self.place = place

class Foo(Bar):
	pass


def binding_dependency(foo: Foo):
	return foo.place


def bar_binding(klass, *args, **kwargs):
	return klass('Osasco')


def test_binding_class_instance():
	aldo = Aldo(Bar)
	aldo.bind(Bar, bar_binding)
	bar = aldo()
	assert(isinstance(bar, Bar))
	assert('Osasco' == bar.place)


def test_subclass_instance():
	aldo = Aldo(Foo)
	aldo.bind(Bar, bar_binding)
	bar = aldo()
	assert(isinstance(bar, Foo))
	assert('Osasco' == bar.place)


def test_subclass_instance():
	aldo = Aldo(binding_dependency)
	aldo.bind(Bar, bar_binding)
	response = aldo()
	assert('Osasco' == response)
