# -*- coding: utf-8 -*-
"""
Created on 22 4 2018/04/22 23:31 2018

@author: Hironori Yamamoto
"""
import unittest

from gplib.operator import initializer
from gplib.solutions import node, solution


def f_non_terminal(n_children=2):
    def print_non_terminal(x):
        print('non_terminal')

    return node.build_func(print_non_terminal, n_children)


def f_terminal(n_children=2):
    def print_terminal(x):
        print('terminal')

    return node.build_func(print_terminal, n_children)


class TestInitializerFunctions(unittest.TestCase):
    def setUp(self):
        self.max_depth = 3
        self.function_dicts = ({0: f_non_terminal()}, {0: f_terminal()})

    def test_initialize(self):
        s = initializer.initialize(0, self.max_depth, self.function_dicts)
        self.assertEqual(solution.get_depth(s), self.max_depth)
        self.assertEqual(node._nodes_checker(*node.get_all_node(s.root)), None)

        s = initializer.initialize(1, self.max_depth, self.function_dicts)
        self.assertEqual(solution.get_depth(s), 0)
