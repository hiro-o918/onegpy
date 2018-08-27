from abc import ABC
from functools import partial
import random

from gplib.solutions import node
from gplib.operator import AbstractOperator, PopulationOperatorAdapter, ProblemBasedOperator


class AbstractMutation(AbstractOperator, ProblemBasedOperator, ABC):
    def __init__(self, m_rate, mutation_type, problem):
        """
        Abstract class of mutation.

        :param m_rate: float([0, 1.0]). mutation rate for each iteration
        :param mutation_type: function name
        :param problem: problem
        """
        AbstractOperator.__init__(self, n_in=1, n_out=1)
        ProblemBasedOperator.__init__(self, problem)
        self._m_rate = m_rate
        self._mutation_type = mutation_type

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
    def func_dicts(self):
        return self.problem.func_dicts

    @func_dicts.setter
    def func_dicts(self, _):
        self.not_changeable_warning()

    @func_dicts.deleter
    def func_dicts(self):
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


def one_point(solution, func_dicts):
    point = random.choice(node.get_all_node(solution.root))
    if point.children is None:
        node.set_id(point, random.choice(list(func_dicts[1].keys())))
    else:
        node.set_id(point, random.choice(list(func_dicts[0].keys())))
    return solution


def get_mutation_core(mutation_type, **kwargs):
    if mutation_type == 'onepoint':
        mutation_core = partial(one_point, **kwargs)
    else:
        msg = '{} is not found'.format(mutation_type)
        raise ValueError(msg)

    return mutation_core


class PointMutation(AbstractMutation):
    def __init__(self, m_rate, problem, mutation_type='onepoint', **kwargs):
        super(PointMutation, self).__init__(m_rate, mutation_type, problem)
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
            return self.mutation_core(solution, self.func_dicts)


class PopulationPointMutation(PopulationOperatorAdapter, ProblemBasedOperator):
    def __init__(self, m_rate, problem, mutation_type='onepoint', generator_builder=None):
        operator = PointMutation(m_rate, problem, mutation_type)

        super(PopulationPointMutation, self).__init__(operator, generator_builder)
