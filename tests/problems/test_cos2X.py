# -*- coding: utf-8 -*-
import unittest

import numpy as np

from gplib.problems import arithmetic
from gplib.solutions import node, solution

import math


class TestEvenParity(unittest.TestCase):
    def setUp(self):
        self.data = 5
        self.cos2X = arithmetic.Cos2XProblem(self.data)

        self.n1 = node.Node(0)
        self.n2 = node.Node(1)
        self.n3 = node.Node(4)
        self.n4 = node.Node(4)
        self.n5 = node.Node(4)
        node.set_children(self.n1, [self.n2, self.n3])
        node.set_children(self.n2, [self.n4, self.n5])

    def test__make_data(self):
        x_, y_ = self.cos2X._make_data(2)

        # the results are checked separately,
        # because ``np.array_equal'' does not work for tuple whose elements have different length.
        self.assertEqual(math.cos(2*x_[0]), y_[0])
        self.assertEqual(math.cos(2 * x_[1]), y_[1])

    def test_fitness(self):
        s = solution.Solution(self.n1)
        print(self.cos2X.fitness(s))

    def test__eval(self):
        self.assertEqual(self.cos2X._eval(self.n1, 1), 1)


class TestBooleanFunctions(unittest.TestCase):
    def setUp(self):
        self.x1 = 1.0
        self.x2 = -1.0

    def test_sin_func(self):
        self.assertEqual(arithmetic.get_sin()(self.x1), math.sin(self.x1))

    def test_cos_func(self):
        self.assertEqual(arithmetic.get_sin()(self.x1), math.cos(self.x1))

    def test_add_func(self):
        self.assertEqual(arithmetic.get_add()([self.x1, self.x2]), self.x1+self.x2)

    def test_sub_func(self):
        self.assertEqual(arithmetic.get_sub()([self.x1, self.x2]), self.x1-self.x2)

    def test_mul_func(self):
        self.assertEqual(arithmetic.get_mul()([self.x1, self.x2]), self.x1*self.x2)

    def test_div_func(self):
        self.assertEqual(arithmetic.get_div()([self.x1, self.x2]), self.x1/self.x2)

    def test_get_x_func(self):
        self.assertEqual(arithmetic.get_x()(self.x1), self.x1)

    def test_get_val_func(self):
        self.assertEqual(arithmetic.get_x()(self.x1), 1.0)

if __name__ == '__main__':
    unittest.main()
