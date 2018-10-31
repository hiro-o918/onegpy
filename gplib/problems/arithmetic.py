from gplib.problem import AbstractProblem, FunctionBank
from gplib.solutions import node
import math
import random
import numpy as np


class Cos2XProblem(AbstractProblem):
    """
    Cos2X problem class
    """
    def __init__(self, n_data, function_bank_builder=None):
        """
        :param n_data: the number of training data
        :param function_bank_builder: function. a builder function for function bank.
        """
        self.x, self.y = self._make_data(n_data)
        super(Cos2XProblem, self).__init__(function_bank_builder)

    def _make_data(self, n_data):
        """
        make training data.
        :param n_data:  the number of training data.
        :return: tuple of ndarray. (x, y)
        """
        x = []
        for i in range(n_data):
            x.append(random.uniform(-math.pi, math.pi))
        x = np.array(x, dtype=float)
        y = np.cos(2*x)
        return x, y

    def _cal_fitness(self, target_solution):
        """
        Calculate fitness
        :param target_solution: solution object. a target solution to calculate fitness.
        :return: float. fitness of the target solution.
        """
        fitness = np.sum(np.abs(self._eval(target_solution.root, self.x) - self.y))

        return 1.0 / (1 + fitness)

    # TODO: use for terminal condition
    def get_hitcounter(self, target_solution, t):
        hitcounter = 0
        for x, y in zip(self.x, self.y):
            error = abs(self._eval(target_solution.root, x) - y)

            if error <= t:
                hitcounter += 1
        return hitcounter

    def _eval(self, current_node, x):
        eval_func = self.func_bank.get_func(current_node.func_id)

        if current_node.is_terminal:
            if eval_func.n_children != 0:
                raise ValueError("node must have {} children. but {} have no child.".format(eval_func.n_children, current_node))
            return eval_func(x)
        else:
            return eval_func([self._eval(c, x) for c in current_node.children])

    def _function_bank_builder(self):
        return get_default_function_bank()


def get_default_function_bank():
    """
    make a function bank with default settings.
    :return: function bank object.
    """

    func_bank = FunctionBank()

    func_bank.add_function(get_add())
    func_bank.add_function(get_sub())
    func_bank.add_function(get_mul())
    func_bank.add_function(get_div())
    func_bank.add_function(get_val(1.0))
    func_bank.add_function(get_sin())
    func_bank.add_function(get_x())

    return func_bank


def get_sin():
    """
    Build and get an "sin" function.
    :return: function object.
    """
    def sin_func(x):
        return np.sin(x[0])

    return node.Function(1, sin_func)


def get_add():
    """
    Build and get an "add" function.
    :return: function object.
    """
    def add_func(x):
        return x[0] + x[1]

    return node.Function(2, add_func)


def get_sub():
    """
    Build and get an "sub" function.
    :return: function object.
    """
    def sub_func(x):
        return x[0] - x[1]

    return node.Function(2, sub_func)


def get_mul():
    """
    Build and get an "mul" function.
    :return: function object.
    """
    def mul_func(x):
        return np.nan_to_num(x[0] * x[1])

    return node.Function(2, mul_func)


def get_div():
    """
    Build and get an "div" function.
    :return: function object.
    """
    def div_func(x):
        return np.nan_to_num(x[0] / x[1])

    return node.Function(2, div_func)


def get_x():
    """
    get function of x.
    :return: function object.
    """
    def x_func(x):
        return x

    return node.Function(0, x_func)


def get_val(val=1.0):
    """
    get function of constant.
    :param val: float. value of constant.
    :return: function object.
    """
    def val_func(x):
        return np.array([val for _ in range(len(x))], float)

    return node.Function(0, val_func)
