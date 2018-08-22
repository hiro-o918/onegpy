import unittest

from gplib.operator import AbstractOperator
from gplib.operators.crossover import RandomSelection, PopulationOnePointCrossover, OnePointCrossover
from gplib.sequential import Sequential
from gplib.solutions.node import Node
from gplib.solutions.solution import Solution
from gplib.base import gpbase
from gplib.viewer import viewer
from gplib.solutions import node


def f_non_terminal(n_children=2):
    def print_non_terminal(x):
        print('non_terminal')

    return node.build_func(print_non_terminal, n_children)


def f_terminal(n_children=2):
    def print_terminal(x):
        print('terminal')

    return node.build_func(print_terminal, n_children)


class TestSequential(unittest.TestCase):
    def setUp(self):
        self.sequential = Sequential([PopulationOnePointCrossover(c_rate=1)])

        self.func_dicts = ({0: f_non_terminal()}, {0: f_terminal()})


    def test_gp(self):
        # self.sequential.add(self.sl)
        # self.sequential.add(self.co)

        gp = gpbase.PopulationGP(sequential=self.sequential, n_generations=10, viewer=viewer.DefaultViewer())

        gp.__call__(0.9, 3, 50, self.func_dicts)


if __name__ == '__main__':
    unittest.main()