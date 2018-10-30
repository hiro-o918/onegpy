import random

from gplib.operator import AbstractOperator, PopulationOperatorAdapter
from gplib.operators.selection import RandomSelection
from gplib.solutions.node import nodes_checker
from gplib.solutions.solution import select_random_points, replace_node, solutions_checker
from gplib.utils.util import get_generator_builder


def crossover(parents, points, destructive=False):
    """
    Core function for crossover
    :param parents: list of solution objects. solutions to do crossover.
    :param points: list of node. crossover points. these nodes are replaced each other.
    :param destructive: bool. If true, solution is replaced, keeping its object.
    Otherwise, new solution instance is created, protecting original solution.
    :return: list of solution objects. new_solutions
    """
    check_parents_and_points(parents, points)
    new_p1 = replace_node(parents[0], points[0], points[1], destructive)
    new_p2 = replace_node(parents[1], points[1], points[0], destructive)
    new_parents = (new_p1, new_p2)

    return new_parents


def destructive_crossover(parents, points):
    """
    A function for destructive crossover
    :param parents: list of solution objects. solutions to do crossover.
    :param points: list of node. crossover points. these nodes are replaced each other.
    :return: list of solution objects. new_solutions
    """
    check_parents_and_points(parents, points)
    return crossover(parents, points, destructive=True)


def get_crossover_core(destructive=True):
    """
    Getter of core function for crossover
    :param destructive: bool. If true, solution is replaced, keeping its object.
    Otherwise, new solution instance is created, protecting original solution.
    :return: function. crossover function
    """
    if not destructive:
        return crossover
    else:
        return destructive_crossover


def check_parents_and_points(parents, points):
    """
    Checker for parents and points
    """
    solutions_checker(parents)
    nodes_checker(points)


class OnePointCrossover(AbstractOperator):
    """
    One point crossover class.
    This crossover is not for population but for a single set of parents.
    """
    def __init__(self, c_rate, destructive=True):
        """
        :param c_rate: float. crossover rate.
        :param destructive: bool. If destructive is true, parents also are changed.
                            Otherwise, parents are copied and keep their structures.
        """
        super(OnePointCrossover, self).__init__(n_in=2, n_out=2)
        self._c_rate = c_rate
        self._destructive = destructive
        self.crossover_core = get_crossover_core(self._destructive)

    def __call__(self, parents):
        """
        Do crossover with crossover probability c_rate.
        :param parents: list of solution objects. solutions to do crossover.
        :return: list of solution objects. new_solutions
        """
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
    """
    One point crossover class for population.
    """
    def __init__(self, c_rate, destructive=False, generator_builder=None):
        """

        :param c_rate: float. Crossover rate
        :param destructive: bool. If destructive is true, parents also are changed.
                            Otherwise, parents are copied and keep their structures.
        :param generator_builder: generator builder. Builder of generator for parents.
                                  Default is None (generator builder using Random Selection).
                                  e.g. If you want to use tournament selection as parents selection,
                                        you can write 'get_generator_builder(TournamentSelection(...))'
        """
        operator = OnePointCrossover(c_rate, destructive)
        if generator_builder is None:
            generator_builder = get_generator_builder(RandomSelection(k=operator.n_in, replacement=False))

        super(PopulationOnePointCrossover, self).__init__(operator, generator_builder)

