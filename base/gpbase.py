#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GP Library

Copyright (c) 2018, Taku Hasegawa.
License: MIT (see LICENSE for details)
"""

__author__ = 'Taku Hasegawa'
__version__ = '0.0.1-alpha'
__license__ = 'MIT'


class AbstractGP(object):

    def __init__(self):
        self.operators = []
        self.population = []
        self.problem = None

    def __call__(self, *args, **kwargs):
        for op in self.operators:
            op(self.population)

    def add_operator(self):
        raise NotImplementedError


class SGP(AbstractGP):

    def __init__(self, init='random', operators = None):
        super().__init__()
        if type(init, str):
            if init == 'random':
                pass

    def search(self):
        for op in self.operators:
            op(self.population)

    def build(self):
        self.population = []

    def set_operators(self):
        pass