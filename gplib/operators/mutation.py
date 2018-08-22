from functools import partial
import random

from gplib.solutions import node
from gplib.operator import AbstractOperator, PopulationOperatorAdapter
from gplib.operators import RandomSelection
from gplib.utils.util import get_generator_builder


class AbstractMutation(AbstractOperator):
    def __init__(self, m_rate, function_dicts, mutation_type):
        """
        Abstract class of mutation.

        :param m_rate: float([0, 1.0]). mutation rate for each iteration
        :param function_dicts: list of dictionary of functions
                                dicts[0] nonterminal. dicts[1] terminal.
        :param mutation_type: function name
        """
        super(AbstractMutation, self).__init__(n_in=1, n_out=1)
        self._m_rate = m_rate
        self._function_dicts = function_dicts
        self._mutation_type = mutation_type

    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    @property
    def m_rate(self):
        return self._m_rate

    @m_rate.setter
    def m_rate(self, _):
        self.not_changeable_warning()

    @m_rate.deleter
    def m_rate(self):
        self.not_changeable_warning()

    @property
    def function_dicts(self):
        return self._function_dicts

    @function_dicts.setter
    def function_dicts(self, _):
        self.not_changeable_warning()

    @function_dicts.deleter
    def function_dicts(self):
        self.not_changeable_warning()

    @property
    def mutation_type(self):
        return self._mutation_type

    @mutation_type.setter
    def mutation_type(self, _):
        self.not_changeable_warning()

    @mutation_type.deleter
    def mutation_type(self):
        self.not_changeable_warning()


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
        self.mutation_core = get_mutation_core(self._mutation_type, **kwargs)

    def __call__(self, solution):
        """
        Point Mutation.
            :param solution: class `Solution`

            :return: solution.
        """
        if isinstance(solution, list):
            if len(solution) is 1:
                solution = solution[0]
            else:
                raise TypeError

        if random.random() > self._m_rate:
            return solution
        else:
            return self.mutation_core(solution, self._function_dicts)


class PopulationPointMutation(PopulationOperatorAdapter):
    def __init__(self, m_rate, function_dicts, mutation_type='onepoint', generator_builder=None):
        operator = PointMutation(m_rate, function_dicts, mutation_type)

        super(PopulationPointMutation, self).__init__(operator, generator_builder)
