import numpy as np

from gplib.problem import AbstractProblem
from gplib.solutions import node


class EvenParity(AbstractProblem):

    def __init__(self, dim):
        super().__init__()
        self.dim = dim
        self.x, self.y = self._make_data()

    def _make_data(self):
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
        value = self._eval(target_solution.root, self.x)
        cnt = np.sum(np.logical_xor(self.y, value))
        fitness = float(cnt) / float(2**self.dim)
        target_solution.previous_fitness = fitness
        return fitness

    def _eval(self, current_node, x):
        if current_node.children is None:
            eval_func = self.func_dicts[1][current_node.func_id]
            return eval_func(x)
        else:
            eval_func = self.func_dicts[0][current_node.func_id]
            results = []
            for c in current_node.children:
                results.append(self._eval(c, x))
            return eval_func(results)


def get_default_node_set(dim):
    nonterminal_node_dict = {}
    terminal_node_dict = {}

    nonterminal_node_dict[0] = get_and(2)
    nonterminal_node_dict[1] = get_or(2)
    nonterminal_node_dict[2] = get_nand(2)
    nonterminal_node_dict[3] = get_nor(2)

    for d in range(dim):
        terminal_node_dict[d] = get_x(d)

    return nonterminal_node_dict, terminal_node_dict


def get_and(n_children=2):
    def and_func(x):
        result = x[0]
        for i in range(len(x)-1):
            result = np.logical_and(result, x[i+1])
        return result

    return node.build_func(and_func, n_children)


def get_or(n_children=2):
    def or_func(x):
        result = x[0]
        for i in range(len(x)-1):
            result = np.logical_or(result, x[i+1])
        return result

    return node.build_func(or_func, n_children)


def get_nand(n_children=2):
    def nand_func(x):
        result = x[0]
        for i in range(len(x)-1):
            result = np.logical_and(result, x[i+1])
        result = np.logical_not(result)
        return result

    return node.build_func(nand_func, n_children)


def get_nor(n_children=2):
    def nor_func(x):
        result = x[0]
        for i in range(len(x)-1):
            result = np.logical_or(result, x[i+1])
        result = np.logical_not(result)
        return result

    return node.build_func(nor_func, n_children)


def get_x(dim_i):
    def x_func(x):
        return x[:, dim_i]
    return node.build_func(x_func, 0)

