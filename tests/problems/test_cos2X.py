# -*- coding: utf-8 -*-
import unittest

import numpy as np

from onegpy.problems import arithmetic
from onegpy.solutions import node, solution

import math


class TestCos2XParity(unittest.TestCase):
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
        self.assertEqual(self.cos2X._eval(self.n1, [[1]]), 1)


class TestArithmeticFunctions(unittest.TestCase):
    def setUp(self):
        self.x1 = np.array([0.0, -1.0], float)
        self.x2 = np.array([-1.0, 1.0], float)

    def test_sin_func(self):
        self.assertTrue(np.array_equal(arithmetic.get_sin()([self.x1]), np.sin(self.x1)))

    def test_add_func(self):
        self.assertTrue(np.array_equal(arithmetic.get_add()(np.array([self.x1, self.x2])).T, self.x1+self.x2))

    def test_sub_func(self):
        self.assertTrue(np.array_equal(arithmetic.get_sub()(np.array([self.x1, self.x2])).T, self.x1-self.x2))

    def test_mul_func(self):
        self.assertTrue(np.array_equal(arithmetic.get_mul()(np.array([self.x1, self.x2])).T, self.x1*self.x2))

    def test_div_func(self):
        self.assertTrue(np.array_equal(arithmetic.get_div()(np.array([self.x1, self.x2])).T, self.x1/self.x2))

    def test_x_func(self):
        self.assertTrue(np.array_equal(arithmetic.get_x(0)(np.array([self.x1]).T), self.x1))

    def test_val_func(self):
        self.assertTrue(np.array_equal(arithmetic.get_val()(self.x1), np.array([1.0, 1.0], float)))


if __name__ == '__main__':
    unittest.main()
