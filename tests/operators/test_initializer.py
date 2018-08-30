# -*- coding: utf-8 -*-
import unittest

from gplib.operators import initializer, RandomInitializer
from gplib.problem import AbstractProblem, FunctionBank
from gplib.solutions import node, solution


def f_non_terminal(n_children=2):
    def print_non_terminal(x):
        print('non_terminal')

    return node.build_func(print_non_terminal, n_children)


def f_terminal():
    def print_terminal(x):
        print('terminal')

    return node.build_func(print_terminal, 0)


class DummyProblem(AbstractProblem):

    def __init__(self):
        super(DummyProblem, self).__init__(function_bank_builder=None)

    def _cal_fitness(self, target_solution):
        return target_solution.root.func_id

    def _function_bank_builder(self):
        func_bank = FunctionBank()
        for i in range(3):
            func_bank.add_function(f_non_terminal())
            func_bank.add_function(f_terminal())
        return func_bank


class TestInitializer(unittest.TestCase):
    def setUp(self):
        self.max_depth = 3
        self.problem = DummyProblem()

    def test_initialize(self):
        t_prob = 0
        initializer = RandomInitializer(t_prob, self.max_depth, self.problem)
        s = initializer()
        self.assertEqual(solution.get_depth(s), self.max_depth)
        self.assertEqual(node._nodes_checker(*node.get_all_node(s.root)), None)

        t_prob = 1
        initializer = RandomInitializer(t_prob, self.max_depth, self.problem)
        s = initializer()
        self.assertEqual(solution.get_depth(s), 0)


if __name__ == '__main__':
    unittest.main()
