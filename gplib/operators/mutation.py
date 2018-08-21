from functools import partial

from gplib.solutions import node
import random


class AbstractMutation(object):
    def __init__(self, m_rate, function_dicts, function_name):
        """
        Abstract class of mutation.

        :param m_rate: float([0, 1.0]). mutation rate for each iteration
        :param function_dicts: list of dictionary of functions
                                dicts[0] nonterminal. dicts[1] terminal.
        :param function_name: function name
        """
        self.m_rate = m_rate
        self.function_dicts = function_dicts
        self.function_name = function_name

    def __call__(self, *args, **kwargs):
        raise NotImplementedError


def one_point(solution, function_dicts):
    point = random.choice(node.get_all_node(solution.root))
    if point.children is None:
        node.set_id(point, random.choice(list(function_dicts[1].keys())))
    else:
        node.set_id(point, random.choice(list(function_dicts[0].keys())))
    return solution


def rate_selection(solution, function_dicts, selection_rate):
    points = node.get_all_node(solution.root)
    for point in points:
        if random.random() <= selection_rate:
            if point.children is None:
                node.set_id(point, random.choice(list(function_dicts[1].keys())))
            else:
                node.set_id(point, random.choice(list(function_dicts[0].keys())))
    return solution


def get_mutation_core(function_name, **kwargs):
    if function_name == 'rate':
        mutation_core = partial(rate_selection, **kwargs)
    elif function_name == 'onepoint':
        mutation_core = partial(one_point, **kwargs)
    else:
        msg = '{} is not found'.format(function_name)
        raise ValueError(msg)

    return mutation_core


class OnePointMutation(AbstractMutation):
    def __init__(self, m_rate, function_dicts, function_name='onepoint', **kwargs):
        super(OnePointMutation, self).__init__(m_rate, function_dicts, function_name)
        self.mutation_core = get_mutation_core(function_name, **kwargs)

    def __call__(self, solution):
        """
            Mutation points in the solution at random.
            :param solution: class `Solution`

            :return: solution.
        """
        if random.random() > self.m_rate:
            return solution
        else:
            # mutation_core = get_mutation_core(self.function_name)
            return self.mutation_core(solution, self.function_dicts)


class RateSelectionMutation(AbstractMutation):
    def __init__(self, m_rate, function_dicts, function_name='rate', **kwargs):
        super(RateSelectionMutation, self).__init__(m_rate, function_dicts, function_name)
        self.mutation_core = get_mutation_core(function_name, **kwargs)

    def __call__(self, solution):
        """
            Mutation points in the solution at random.
            :param solution: class `Solution`

            :return: solution.
        """
        return self.mutation_core(solution, self.function_dicts, self.m_rate)
