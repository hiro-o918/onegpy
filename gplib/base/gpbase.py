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
    
    def __init__(self, n_generations, initializer, sequential, observer, **kwargs):
        """

        :param n_generations: int. the number of generations
        :param initializer: population initializer object. initializer of population
        :param sequential: sequential object. genetic operators
        :param observer: Observer object.
        """
        self.n_generations = n_generations
        self.initializer = initializer
        self.sequential = sequential
        self.observer = observer

    def __call__(self):
        """
        optimize a target problem.
        :return:
        """
        population = self.initializer()
        self.observer.begin()
        for gene in range(self.n_generations):
            population = self.sequential(population)
            self.observer.update(gene, population)

        self.observer.end(population)
