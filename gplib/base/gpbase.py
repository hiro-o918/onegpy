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
    
    def __init__(self, n_generations, initializer, sequential, logger, **kwargs):
        """

        :param n_generations: int. the number of generations
        :param initializer: population initializer object. initializer of population
        :param sequential: sequential object. genetic operators
        :param logger: logger object. logger for population based GP
        """
        self.n_generations = n_generations
        self.initializer = initializer
        self.sequential = sequential
        self.logger = logger

    def __call__(self):
        """
        optimize a target problem.
        :return:
        """
        population = self.initializer()
        self.logger.begin()
        for gene in range(self.n_generations):
            population = self.sequential(population)
            self.logger.update(gene, population)

        self.logger.end(population)
