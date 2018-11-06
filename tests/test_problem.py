import unittest

from onegpy.problem import AbstractProblem, FunctionBank, problem_checker
from onegpy.solutions import node


def f_non_terminal(n_children=2):
    def print_non_terminal(x):
        print('non_terminal')

    return node.Function(n_children, print_non_terminal)


def f_terminal(n_children=0):
    def print_terminal(x):
        print('terminal')

    return node.Function(n_children, print_terminal)


class EmptyProblem(AbstractProblem):
    def __init__(self):
        super().__init__(function_bank_builder=None)

    def _function_bank_builder(self):
        func_bank = FunctionBank()
        for i in range(3):
            func_bank.add_function(f_non_terminal())
            func_bank.add_function(f_terminal())
        return func_bank

    def _cal_fitness(self, target_solution):
        return target_solution.root.func_id


class TestProblem(unittest.TestCase):
    def setUp(self):
        self.p = EmptyProblem()

    def test_problem_checker(self):
        with self.assertRaises(TypeError):
            problem_checker(1)

        problem_checker(self.p)
