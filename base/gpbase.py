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


class GP(object):

    def __init__(self, operators, problem, func_dict):
        self.operators = operators
        self.problem = problem
        self.func_dict = func_dict

    def __call__(self, population):
        for op in self.operators:
            op(population)