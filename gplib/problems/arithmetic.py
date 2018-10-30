import numpy as np
from gplib.problem import AbstractProblem, FunctionBank
from gplib.solutions import node
import math
import random


class Cos2XProblem(AbstractProblem):
    def __init__(self, data, function_bank_builder=None):
        self.x, self.y = self._make_data(data)
        super(Cos2XProblem, self).__init__(function_bank_builder)

    def _make_data(self, data):
        x = []
        y = []
        for i in range(data):
            x.append(random.uniform(-math.pi, math.pi))
            y.append(math.cos(2*x[i]))
        return x, y

    def _cal_fitness(self, target_solution):
        fitness = 0.0
        for x, y in zip(self.x, self.y):
            error = abs(self._eval(target_solution.root, x) - y)
            fitness += error
        return 1.0 / (1 + fitness)

    def get_hitcount(self, target_solution):
        hitcounter = 0
        for x, y in zip(self.x, self.y):
            error = abs(self._eval(target_solution.root, x) - y)

            if error <= 0.001:
                hitcounter += 1
        return hitcounter

    def _eval(self, current_node, x):
        eval_func = self.func_bank.get_func(current_node.func_id)
        if current_node.is:
            if eval_func.n_children != 0:
                raise ValueError("node must have {} children. but {} have no child.".format(eval_func.n_children, current_node))
            return eval_func(x)
        else:
            results = []
            for c in current_node.children:
                results.append(self._eval(c, x))
            return eval_func(results)

    def _function_bank_builder(self):
        return get_default_function_bank()


def get_default_function_bank():

    func_bank = FunctionBank()

    func_bank.add_function(get_add(2))
    func_bank.add_function(get_sub(2))
    func_bank.add_function(get_mul(2))
    func_bank.add_function(get_div(2))
    func_bank.add_function(get_val(0, 1.0))
    func_bank.add_function(get_sin(1))
    func_bank.add_function(get_x(0))

    return func_bank


def get_sin(n_children=1):
    def sin_func(x):
        return math.sin(x[0])

    return node.Function(sin_func, n_children)


def get_add(n_children=2):
    def add_func(x):
        return x[0] + x[1]

    return node.Function(add_func, n_children)


def get_sub(n_children=2):
    def sub_func(x):
        return x[0] - x[1]

    return node.Function(sub_func, n_children)


def get_mul(n_children=2):
    def mul_func(x):
        return x[0] * x[1]

    return node.Function(mul_func, n_children)


def get_div(n_children=2):
    def div_func(x):
        right = x[1]
        if abs(x[1]) <= 0.0:
            right = 1.0
        return x[0] / right

    return node.Function(div_func, n_children)


def get_x(n_children=0):
    def x_func(x):
        return x

    return node.Function(x_func, n_children)


def get_val(n_children=0, val=1.0):
    def val_func(x):
        return val

    return node.Function(val_func, n_children)
