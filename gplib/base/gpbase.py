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

    def __init__(self, n_generations, initializer, sequential,  viewer, **kwargs):
        self.n_generations = n_generations
        self.initializer = initializer
        self.sequential = sequential
        self.viewer = viewer

    def __call__(self):
        population = self.initializer()
        self.viewer.begin()
        for gene in range(self.n_generations):
            population = self.sequential(population)
            self.viewer.update(gene, population)

        self.viewer.end(population)
