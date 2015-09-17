# -*- coding: utf-8 -*-

from aldo.exceptions import AldoClassNotBindedException
import inspect


class Aldo:
    """
        Aldo dependency manager
    """
    bindings = {}

    def __init__(self, func, *args, **kwargs):
        """
            Function to handle dependencies
        """
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.handled = {}

    @staticmethod
    def bind(klass, factory):
        """
            Add a factory for new instances of klass
        """
        Aldo.bindings[klass] = factory

    def __call__(self):
        """
            Call handled function using parameters
        """
        try:
            return self._binded()
        except AldoClassNotBindedException:
            pass

        args, kwargs = self._parse_args_and_kwargs()

        return self.func(*args, **kwargs)

    def parameters(self):
        """
            Returns list of parameters required for func
        """
        return inspect.getfullargspec(self.func)

    def _binded(self):
        """
            Returns binded class if it exists
        """
        if inspect.isclass(self.func):
            for bind in self.bindings:
                if issubclass(self.func, bind):
                    args = list(self.args)
                    kwargs = dict(**self.kwargs)
                    kwargs['klass'] = self.func
                    return self.bindings[bind](*args, **kwargs)

        raise AldoClassNotBindedException

    def _parse_args_and_kwargs(self):
        """
            Inspect parameters and create instances of dependencies when it is necessary
        """
        kwargs = {}
        args = []
        parameters = self.parameters()

        if self._args_not_filled_yet(parameters.args):
            print("not filled yet")
            for key in parameters.args:
                if not key in parameters.annotations:
                    continue

                kwargs[key] = self._handle_class(parameters.annotations[key])
                self.handled[key] = kwargs[key]

            pending = [arg for arg in parameters.args if not arg in kwargs]
            for arg in pending:
                if arg in self.kwargs:
                    kwargs[arg] = self.kwargs[arg]

            args = self.args[:len(pending)]
        else:
            args = list(self.args)

        return args, kwargs

    def _handle_class(self, klass):
        """
            Handle new instances of klass and dependencies
        """
        kwargs = dict(**self.kwargs)
        kwargs['__origin'] = self.func
        kwargs['aldo_context'] = self.handled
        aldo = Aldo(klass, *self.args, **kwargs)
        aldo.handled = self.handled
        return aldo()

    def _args_not_filled_yet(self, args):
        """
            Compare if current number of args fill in method or class dependencies
        """
        return len(args) != len(self.args)
