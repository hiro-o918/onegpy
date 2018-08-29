from gplib.problem import AbstractProblem
from gplib.solutions import node


def f_non_terminal(n_children=2):
    def print_non_terminal(x):
        print('non_terminal')

    return node.build_func(print_non_terminal, n_children)


def f_terminal(n_children=2):
    def print_terminal(x):
        print('terminal')

    return node.build_func(print_terminal, n_children)


class EmptyProblem(AbstractProblem):
    def _function_dicts_builder(self):
        return [({0: f_non_terminal(), 1: f_non_terminal()}),
                ({2: f_terminal(), 3: f_terminal()})]

    def _cal_fitness(self, target_solution):
        return target_solution.root.func_id