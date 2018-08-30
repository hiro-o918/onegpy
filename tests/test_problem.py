from gplib.problem import AbstractProblem, FunctionBank
from gplib.solutions import node


def f_non_terminal(n_children=2):
    def print_non_terminal(x):
        print('non_terminal')

    return node.build_func(print_non_terminal, n_children)


def f_terminal(n_children=0):
    def print_terminal(x):
        print('terminal')

    return node.build_func(print_terminal, n_children)


class EmptyProblem(AbstractProblem):
    def _function_bank_builder(self):
        func_bank = FunctionBank()
        for i in range(3):
            func_bank.add_function(f_non_terminal())
            func_bank.add_function(f_terminal())
        return func_bank

    def _cal_fitness(self, target_solution):
        return target_solution.root.func_id
