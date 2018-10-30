import random

from gplib.operator import AbstractOperator, PopulationOperatorAdapter
from gplib.operators.selection import RandomSelection
# TODO: we must consider the number of parents and crossover points.
# TODO: + checking the number of parents and crossover points in each function
from gplib.solutions.node import nodes_checker
from gplib.solutions.solution import select_random_points, replace_node, solutions_checker
from gplib.utils.util import get_generator_builder


def crossover(parents, points, destructive=False):
    new_p1 = replace_node(parents[0], points[0], points[1], destructive)
    new_p2 = replace_node(parents[1], points[1], points[0], destructive)
    new_parents = (new_p1, new_p2)

    return new_parents


def destructive_crossover(parents, points):
    return crossover(parents, points, destructive=True)


def get_crossover_core(destructive=True):
    if not destructive:
        return crossover
    else:
        return destructive_crossover


def check_parents_and_points(parents, points):
    solutions_checker(parents)
    nodes_checker(points)

    if len(parents) != 2:
        msg = 'The length of parents must be 2, but actual {}'\
            .format(len(parents))
        raise ValueError(msg)

    if len(points) != 2:
        msg = 'The length of points must be 2, but actual {}'\
            .format(len(parents))
        raise ValueError(msg)


class OnePointCrossover(AbstractOperator):
    def __init__(self, c_rate, destructive=True):
        """
        One point crossover.
        :param c_rate: Crossover rate.
        :param destructive: If destructive is true, parents also are changed.
                            Otherwise, parents are copied and keep their structures.
        """
        super(OnePointCrossover, self).__init__(n_in=2, n_out=2)
        self._c_rate = c_rate
        self._destructive = destructive
        self.crossover_core = get_crossover_core(self._destructive)

    def __call__(self, parents):
        if len(parents) != 2:
            msg = 'parents must be a list consisting of two solutions'
            raise ValueError(msg)

        points = [select_random_points(p, 1)[0] for p in parents]

        if random.random() > self._c_rate:
            return parents
        else:
            return self.crossover_core(parents, points)

    @property
    def c_rate(self):
        return self._c_rate

    @c_rate.setter
    def c_rate(self, _):
        self.not_changeable_warning()

    @c_rate.deleter
    def c_rate(self):
        self.not_changeable_warning()

    @property
    def destructive(self):
        return self._destructive

    @destructive.setter
    def destructive(self, _):
        self.not_changeable_warning()

    @destructive.deleter
    def destructive(self):
        self.not_changeable_warning()


class PopulationOnePointCrossover(PopulationOperatorAdapter):

    def __init__(self, c_rate, destructive=False, generator_builder=None):

        operator = OnePointCrossover(c_rate, destructive)
        if generator_builder is None:
            generator_builder = get_generator_builder(RandomSelection(k=operator.n_in, replacement=False))

        super(PopulationOnePointCrossover, self).__init__(operator, generator_builder)

