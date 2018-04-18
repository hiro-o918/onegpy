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


from gplib.solutions import solution
import numpy as np

class GP(object):

    def __init__(self, operators, problem, func_dicts, n_generations):
        self.operators = operators
        self.problem = problem
        self.func_dicts = func_dicts
        self.n_generations = n_generations

    def __call__(self, population):
        print('{}, {}, {}'.format('generation', 'best', 'average'))
        for gene in range(self.n_generations):
            for op in self.operators:
                population = op(population)

            fitness_list = []
            depth_list = []
            for s in population:
                fitness_list.append(s.previous_fitness)
                depth_list.append(solution.get_depth(s))

            print('{}, {}, {}, {}, {}, {}'.format(gene, max(fitness_list), np.average(fitness_list), max(depth_list),
                                              np.average(depth_list), len(population)))

