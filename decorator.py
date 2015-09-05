# -*- code: utf-8 -*-

from dependency_manager import Aldo
from functools import wraps

def aldo(func):
	@wraps(func)
	def run(*args, **kwargs):
		return Aldo(func, *args, **kwargs)()

	return run