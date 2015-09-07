# -*- coding: utf-8 -*-

import os, sys

sys.path.insert(0, os.path.realpath('..'))

import pytest
from aldo.dependency_manager import Aldo


class Bar:
	def __init__(self, place):
		self.place = place


def bar_binding(*args, **kwargs):
	return Bar('Osasco')


def test_binding_class_instance():
	aldo = Aldo(Bar)
	aldo.bind(Bar, bar_binding)
	bar = aldo()
	assert('Osasco' == bar.place)
