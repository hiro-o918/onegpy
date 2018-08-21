from functools import partial

from gplib.solutions import node
from gplib.operator import AbstractOperator
import random


class AbstractMutation(AbstractOperator):
    def __init__(self, m_rate, function_dicts, mutation_type):
        """
        Abstract class of mutation.

        :param m_rate: float([0, 1.0]). mutation rate for each iteration
        :param function_dicts: list of dictionary of functions
                                dicts[0] nonterminal. dicts[1] terminal.
        :param mutation_type: function name
        """
        self.m_rate = m_rate
        self.function_dicts = function_dicts
        self.mutation_type = mutation_type

    def __call__(self, *args, **kwargs):
        raise NotImplementedError


def one_point(solution, function_dicts):
    point = random.choice(node.get_all_node(solution.root))
    if point.children is None:
        node.set_id(point, random.choice(list(function_dicts[1].keys())))
    else:
        node.set_id(point, random.choice(list(function_dicts[0].keys())))
    return solution


def get_mutation_core(mutation_type, **kwargs):
    if mutation_type == 'onepoint':
        mutation_core = partial(one_point, **kwargs)
    else:
        msg = '{} is not found'.format(mutation_type)
        raise ValueError(msg)

    return mutation_core


class PointMutation(AbstractMutation):
    def __init__(self, m_rate, function_dicts, mutation_type='onepoint', **kwargs):
        super(PointMutation, self).__init__(m_rate, function_dicts, mutation_type)
        self.mutation_core = get_mutation_core(mutation_type, **kwargs)

    def __call__(self, solution):
        """
        Point Mutation.
            :param solution: class `Solution`

            :return: solution.
        """
        if random.random() > self.m_rate:
            return solution
        else:
            return self.mutation_core(solution, self.function_dicts)
