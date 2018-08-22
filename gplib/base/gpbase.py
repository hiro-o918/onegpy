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


from gplib.operators import initializer


class PopulationGP(object):

    def __init__(self, sequential, n_generations, viewer):
        self.sequential = sequential
        self.n_generations = n_generations
        self.viewer = viewer

    def __call__(self, t_prob, max_depth, pop_size, function_dicts):
        population = initializer.population_initialize(t_prob, max_depth, pop_size, function_dicts)
        self.viewer.begin()
        for gene in range(self.n_generations):
            population = self.sequential(population)
            self.viewer.update(gene, population)

        self.viewer.end(population)
