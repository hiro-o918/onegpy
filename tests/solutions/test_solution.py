# -*- coding: utf-8 -*-
"""
Created on 20 4 2018/04/20 0:14 2018

@author: Hironori Yamamoto
"""
from unittest import TestCase

from gplib.solutions import node, solution


class TestSolutionFunctions(TestCase):
    def setUp(self):
        self.n1 = node.Node()
        self.n2 = node.Node()
        self.n3 = node.Node()
        self.n4 = node.Node()
        self.n5 = node.Node()
        self.n6 = node.Node()

        self.f1 = node.Function(2)
        self.f2 = node.Function(3)
        # ``function_dict'' is not separated based on kinds of nodes
        # such as non-terminal nodes or terminal nodes here.
        self.function_dict = {0: self.f1, 1: self.f2}

        node.set_id(self.n1, 0)
        node.set_id(self.n2, 1)
        node.set_children(self.n1, [self.n2, self.n3])
        node.set_children(self.n2, [self.n4, self.n5, self.n6])

        self.n = solution.Solution(self.n1)

    def test_get_depth(self):
        self.assertEqual(solution.get_depth(self.n), 2)
