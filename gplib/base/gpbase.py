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


class PopulationGP(object):

    def __init__(self, initializer, sequential, viewer, t_condition):
        self.initializer = initializer
        self.sequential = sequential
        self.viewer = viewer
        self.t_condition = t_condition

    def __call__(self):
        population = self.initializer()
        self.viewer.begin()
        gene = 0
        while self.t_condition():
            population = self.sequential(population)
            self.viewer.update(gene, population)
            gene += 1

        self.viewer.end(population)
