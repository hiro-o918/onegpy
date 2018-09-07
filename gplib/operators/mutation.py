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
    def func_bank(self):
        return self.problem.func_bank

    @func_bank.setter
    def func_bank(self, _):
        self.not_changeable_warning()

    @func_bank.deleter
    def func_bank(self):
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


def one_point(solution, func_bank):
    point = random.choice(node.get_all_node(solution.root))
    n_children = len(point.children)
    function_list = func_bank.get_function_list(n_children)
    if function_list is None:
        raise ValueError("function bank must have {}'s function list, but it has no list.".format(n_children))

    candidate_id = random.sample(function_list, 2)
    if point.func_id != candidate_id[0]:
        node.set_id(point, candidate_id[0])
    else:
        node.set_id(point, candidate_id[1])

    return solution


def get_mutation_core(mutation_type, **kwargs):
    if mutation_type == 'onepoint':
        # Obtain `one_point` function fixed `func_bank`
        mutation_core = partial(one_point, **kwargs)
    else:
        msg = '{} is not found'.format(mutation_type)
        raise ValueError(msg)

    return mutation_core


class PointMutation(AbstractMutation):
    def __init__(self, m_rate, problem, mutation_type='onepoint'):
        super(PointMutation, self).__init__(m_rate, mutation_type, problem)
        self.mutation_core = get_mutation_core(self._mutation_type, func_bank=problem.func_bank)

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
            return self.mutation_core(solution)


class PopulationPointMutation(PopulationOperatorAdapter, ProblemBasedOperator):
    def __init__(self, m_rate, problem, mutation_type='onepoint', generator_builder=None):
        operator = PointMutation(m_rate, problem, mutation_type)

        super(PopulationPointMutation, self).__init__(operator, generator_builder)
