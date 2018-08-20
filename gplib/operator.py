# -*- coding: utf-8 -*-


class AbstractOperator(object):
    """
        This is the base class for operators.
    """

    def __call__(self, *args, **kwargs):
        raise NotImplementedError
