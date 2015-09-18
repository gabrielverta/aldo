# -*- coding: utf-8 -*-

class AldoClassNotBindedException(Exception):
    pass


class AldoRedirect(Exception):
    def __init__(self, response):
        super(Exception, self).__init__()
        self.response = response
