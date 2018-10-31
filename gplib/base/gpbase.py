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
    
    def __init__(self, initializer, sequential, observer, terminal_condition, **kwargs):
        """

        :param initializer: population initializer object. initializer of population
        :param sequential: sequential object. genetic operators
        :param observer: Observer object.
        """
        self.initializer = initializer
        self.sequential = sequential
        self.observer = observer
        self.terminal_condition = terminal_condition

    def __call__(self):
        """
        optimize a target problem.
        :return:
        """
        population = self.initializer()
        self.observer.begin()
        gene = 0
        while not self.terminal_condition():
            population = self.sequential(population)
            self.observer.update(gene, population)
            gene += 1

        self.observer.end(population)
