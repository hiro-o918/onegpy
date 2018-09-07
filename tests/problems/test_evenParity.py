# -*- coding: utf-8 -*-
import unittest

import numpy as np

from gplib.problems import boolean
from gplib.solutions import node, solution


class TestEvenParity(unittest.TestCase):
    def setUp(self):
        self.dim = 2
        self.even_parity = boolean.EvenParity(self.dim)
        self.x = np.array([[False, False],
                           [True, False],
                           [False, True],
                           [True, True]], dtype=bool)
        self.y = np.array([False, True, True, False], dtype=bool)

        self.n1 = node.Node(0)
        self.n2 = node.Node(1)
        self.n3 = node.Node(4)
        self.n4 = node.Node(4)
        self.n5 = node.Node(4)
        node.set_children(self.n1, [self.n2, self.n3])
        node.set_children(self.n2, [self.n4, self.n5])

    def test__make_data(self):
        x_, y_ = self.even_parity._make_data()

        # the results are checked separately,
        # because ``np.array_equal'' does not work for tuple whose elements have different length.
        self.assertTrue(np.array_equal(self.x, x_))
        self.assertTrue(np.array_equal(self.y, y_))

    def test_fitness(self):
        s = solution.Solution(self.n1)
        print(self.even_parity.fitness(s))

    def test__eval(self):
        self.assertTrue(np.array_equal(
            self.even_parity._eval(self.n1, self.x), (False, True, False, True)))


class TestBooleanFunctions(unittest.TestCase):
    def setUp(self):
        self.x = np.array([[False, False],
                           [True, False],
                           [False, True],
                           [True, True]], dtype=bool)

    def test_and_func(self):
        self.assertTrue(np.array_equal(boolean.get_and()(self.x.T), [False, False, False, True]))

    def test_or_func(self):
        self.assertTrue(np.array_equal(boolean.get_or()(self.x.T), [False, True, True, True]))

    def test_nand_func(self):
        self.assertTrue(np.array_equal(boolean.get_nand()(self.x.T), [True, True, True, False]))

    def test_nor_func(self):
        self.assertTrue(np.array_equal(boolean.get_nor()(self.x.T), [True, False, False, False]))

    def test_x_func(self):
        self.assertTrue(np.array_equal(boolean.get_x(0)(self.x), [False, True, False, True]))


if __name__ == '__main__':
    unittest.main()
