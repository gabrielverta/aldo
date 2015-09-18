from .decorator import  *
from .exceptions import AldoRedirect


def manage(func, *args, **kwargs):
    """
        Shortcut to aldo manager

    :param func: function or class to be handled by aldo dependency manager
    :param args:
    :param kwargs:
    :return:
    """
    aldo = Aldo(func, *args, **kwargs)
    aldo.debug = True
    return aldo()