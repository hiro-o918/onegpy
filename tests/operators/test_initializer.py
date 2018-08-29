# -*- coding: utf-8 -*-
import unittest

from gplib.operators import initializer, RandomInitializer
from gplib.problem import AbstractProblem
from gplib.solutions import node, solution


def f_non_terminal(n_children=2):
    def print_non_terminal(x):
        print('non_terminal')

    return node.build_func(print_non_terminal, n_children)


def f_terminal(n_children=2):
    def print_terminal(x):
        print('terminal')

    return node.build_func(print_terminal, n_children)


class DummyProblem(AbstractProblem):

    def __init__(self):
        super(DummyProblem, self).__init__()

    def _cal_fitness(self, target_solution):
        pass

    def _function_dicts_builder(self):
        func_dicts = ({0: f_non_terminal()}, {0: f_terminal()})
        return func_dicts


class TestInitializer(unittest.TestCase):
    def setUp(self):
        self.max_depth = 3
        self.problem = DummyProblem()

    def test_initialize(self):
        t_prob = 0
        initializer = RandomInitializer(t_prob, self.max_depth, self.problem)
        s = initializer()
        self.assertEqual(solution.calc_solution_depth(s), self.max_depth)
        self.assertEqual(node._nodes_checker(*node.get_all_node(s.root)), None)

        t_prob = 1
        initializer = RandomInitializer(t_prob, self.max_depth, self.problem)
        s = initializer()
        self.assertEqual(solution.calc_solution_depth(s), 0)


if __name__ == '__main__':
    unittest.main()
