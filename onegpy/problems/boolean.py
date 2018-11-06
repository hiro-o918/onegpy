import numpy as np
from onegpy.problem import AbstractProblem, FunctionBank
from onegpy.solutions import node


class EvenParity(AbstractProblem):
    """
    Even parity problem class
    """

    def __init__(self, dim, function_bank_builder=None):
        """
        :param dim: int. the number of dimension.
        :param function_bank_builder: function. a builder function for function bank.
        """
        self.dim = dim
        self.x, self.y = self._make_data()
        super(EvenParity, self).__init__(function_bank_builder)

    def _make_data(self):
        """
        make training data.
        :return: tuple of ndarray. (x, y)
        """
        x = []
        y = []
        for i in range(2 ** self.dim):
            xi = []
            for j in range(self.dim):
                xi.append((i >> j) % 2 == 1)
            y.append(sum(xi) % 2 == 1)
            x.append(xi)
        x = np.array(x, dtype=bool)
        y = np.array(y, dtype=bool)
        return x, y

    def _cal_fitness(self, target_solution):
        """
        Calculate fitness
        :param target_solution: solution object. a target solution to calculate fitness.
        :return: float. fitness of the target solution.
        """
        value = self._eval(target_solution.root, self.x)
        cnt = np.sum(np.logical_xor(self.y, value))
        fitness = float(cnt) / float(2**self.dim)
        return fitness

    def _eval(self, current_node, x):
        """
        Evaluate a node with x.
        :param current_node: node object. a target node to evaluate with x
        :param x: ndarray. input of the data.
        :return: float. evaluation result.
        """
        eval_func = self.func_bank.get_func(current_node.func_id)
        if not current_node.children:
            if eval_func.n_children != 0:
                raise ValueError("node must have {} children. but {} have no child.".format(eval_func.n_children, current_node))
            return eval_func(x)
        else:
            results = []
            for c in current_node.children:
                results.append(self._eval(c, x))
            return eval_func(results)

    def _function_bank_builder(self):
        """
        Build function bank
        :return: function bank object.
        """
        return get_default_function_bank(self.dim)


def get_default_function_bank(dim):
    """
    make a function bank with default settings.
    :param dim: the number of dimension
    :return: function bank object.
    """

    func_bank = FunctionBank()

    func_bank.add_function(get_and(2))
    func_bank.add_function(get_or(2))
    func_bank.add_function(get_nand(2))
    func_bank.add_function(get_nor(2))

    for d in range(dim):
        func_bank.add_function(get_x(d))

    return func_bank


def get_and(n_children=2):
    """
    Build and get an "and" function.
    :param n_children: int. the number of children.
    :return: function object.
    """
    def and_func(x):
        result = x[0]
        for i in range(len(x)-1):
            result = np.logical_and(result, x[i+1])
        return result

    return node.Function(n_children, and_func)


def get_or(n_children=2):
    """
    Build and get an "or" function.
    :param n_children: int. the number of children.
    :return: function object.
    """
    def or_func(x):
        result = x[0]
        for i in range(len(x)-1):
            result = np.logical_or(result, x[i+1])
        return result

    return node.Function(n_children, or_func)


def get_nand(n_children=2):
    """
    Build and get a "nand" function.
    :param n_children: int. the number of children.
    :return: function object.
    """
    def nand_func(x):
        result = x[0]
        for i in range(len(x)-1):
            result = np.logical_and(result, x[i+1])
        result = np.logical_not(result)
        return result

    return node.Function(n_children, nand_func)


def get_nor(n_children=2):
    """
    Build and get a "nor" function.
    :param n_children: int. the number of children.
    :return: function object.
    """
    def nor_func(x):
        result = x[0]
        for i in range(len(x)-1):
            result = np.logical_or(result, x[i+1])
        result = np.logical_not(result)
        return result

    return node.Function(n_children, nor_func)


def get_x(dim_i):
    """
    get function of i-th elements in x.
    :param dim_i: int. target dimension.
    :return: function object.
    """

    def x_func(x):
        return x[:, dim_i]
    return node.Function(0, x_func)

