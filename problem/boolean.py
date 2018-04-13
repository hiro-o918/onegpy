from solutions import node
import numpy as np

class EvenParity(object):

    def __init__(self, dim):
        self.func_dict = {}
        self.dim = dim
        self.x, self.y = self._make_data(dim)


    def _make_data(self, dim):
        x = []
        y = []
        for i in range(2 ** dim):
            xi = []
            for j in range(dim):
                xi.append((i >> j) % 2 == 1)
            y.append(sum(xi) % 2 == 1)
            x.append(xi)
        x = np.array(x, dtype=bool)
        y = np.array(y, dtype=bool)
        return x, y


    def fitness(self, solution):
        cnt = 0
        for x, y in zip(self.x, self.y):
            value = self._eval(solution.root, x)
            if not np.logical_xor(y, value):
                cnt += 1
        return float(cnt) / float(2**self.dim)


    def _eval(self, node, x):
        eval_func = self.func_dict[node.id]

        if eval_func.n_children == 0:
            return eval_func(x)
        else:
            results = []
            for c in node.children:
                results.append(self.eval(c, x))
                return eval_func(results)


def get_default_node_set(dim):
    node_dict = {}

    node_dict[0] = get_and(2)
    node_dict[1] = get_or(2)
    node_dict[2] = get_nand(2)
    node_dict[3] = get_nor(2)

    for d in dim:
        node_dict[4+d] = get_x(d)

    return node_dict

def get_and(n_children=2):
    def and_func(x):
        result = x[0]
        for i in range(len(x)-1):
            result = np.logical_and(result, x[i+1])
        return result

    return node.get_func(and_func, n_children)


def get_or(n_children=2):
    def or_func(x):
        result = x[0]
        for i in range(len(x)-1):
            result = np.logical_or(result, x[i+1])
        return result

    return node.get_func(or_func, n_children)


def get_nand(n_children=2):
    def nand_func(x):
        result = x[0]
        for i in range(len(x)-1):
            result = np.logical_and(result, x[i+1])
        result = np.logical_not(result)
        return result

    return node.get_func(nand_func, n_children)


def get_nor(n_children=2):
    def nor_func(x):
        result = x[0]
        for i in range(len(x)-1):
            result = np.logical_or(result, x[i+1])
        result = np.logical_not(result)
        return result

    return node.get_func(nor_func, n_children)


def get_x(dim_i):
    def x_func(x):
        return x[dim_i]
    return node.get_func(x_func, 0)

