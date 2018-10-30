#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GP Library

Copyright (c) 2018, Taku Hasegawa.
License: MIT (see LICENSE for details)
"""

__author__ = 'Taku Hasegawa, '
__version__ = '0.1.0-beta'
__license__ = 'MIT'


class PopulationGP(object):
    """
    base class of population based GP
    """

    def __init__(self, initializer, sequential, viewer, terminal_condition, **kwargs):
        """
        :param n_generations: int. the number of generations
        :param initializer: population initializer object. initializer of population
        :param sequential: sequential object. genetic operators
        :param viewer: viewer object. viewer for population based GP
        """
        self.initializer = initializer
        self.sequential = sequential
        self.viewer = viewer
        self.terminal_condition = terminal_condition

    def __call__(self):
        """
        optimize a target problem.
        :return:
        """
        population = self.initializer()
        self.viewer.begin()
        gene = 0
        while self.terminal_condition():
            population = self.sequential(population)
            self.viewer.update(gene, population)
            gene += 1

        self.viewer.end(population)
