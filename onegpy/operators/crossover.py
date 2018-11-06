import random

from onegpy.operator import AbstractOperator, PopulationOperatorAdapter
from onegpy.operators.selection import RandomSelection
from onegpy.solutions import solution
from onegpy.solutions.node import nodes_checker
from onegpy.solutions.solution import select_random_points, replace_node, solutions_checker
from onegpy.utils.util import get_generator_builder


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


class MLPSCrossover(AbstractOperator):
    """
    Crossover class for the MLPS-GP
    """

    def __init__(self, problem, stop_after_one=False, donor_order='random'):
        """
        :param problem: problem object. target problem.
        :param stop_after_one: bool. stop a crossover after the first donation.
        :param donor_order:
        """
        super(MLPSCrossover, self).__init__()
        self.stop_after_one = stop_after_one
        self.donor_order = donor_order
        self.problem = problem

    def __call__(self, recipient, cross_points, donors):
        """
        Crossover class for MLPS-GP
        :param recipient: solution object. recipient of the MLPS-GP crossover.
        :param cross_points: list of node objects. crossover points list for the MLPS-GP.
                              Basically, this is terminal node positions of the candidate solution after local search.
        :param donors: list of solutions. a candidate donor subtree list.
                        Basically, this is a layer(sub-population) in pyramid.
        """
        # cross_points: list of tuple, (parent of crosspoint, children index)
        random.shuffle(cross_points)
        for cross_point in cross_points:
            self.improve(recipient, cross_point, donors)

    def improve(self, recipient, cross_point, donors):
        """
        Replace a sub-tree of the recipient at a crossover point with donors
        :param recipient: solution object. recipient of the MLPS-GP crossover.
        :param cross_point: node object. a crossover point.
        :param donors: list of solutions. a candidate donor subtree list.
        :return:
        """
        # check if the recipient and each donor have a same tree structure or not.
        # options is list of donors which are used for replacement
        options = self.get_options(recipient, donors)
        if self.donor_order == 'random':
            random.shuffle(options)
        for index in options:
            donor = donors[index]
            stop = self.donate(recipient, cross_point, donor)
            # if stop after one is True, stop the donation soon.
            if stop or self.stop_after_one:
                break
        del options

    def donate(self, recipient, cross_point, donor):
        """
        Replace a sub-tree of the recipient with a donor
        :param recipient: solution object. recipient of the MLPS-GP crossover.
        :param cross_point: node object. a crossover point.
        :param donor: node object. root node of subtree(donor's root).
        :return: bool. if fitness is improved or not.
        """
        stop = False
        previous_fitness = recipient.previous_fitness
        parent_node, index = cross_point
        pre_node = parent_node.children[index]
        # TODO: check if the pre_node and the donor is same sub-tree, if so, we don't have to check the fitness of the new solution.
        parent_node.children[index] = donor.root
        fitness = self.problem.fitness(recipient)
        if previous_fitness >= fitness:
            parent_node.children[index] = pre_node
            solution.set_previous_fitness(recipient, previous_fitness)
        else:
            stop = True
        return stop

    def get_options(self, recipient, donors):
        """
        Check if the recipient and each donor have a same tree structure or not.
        :param recipient: solution object. recipient of the MLPS-GP crossover.
        :param donors: list of solutions. a candidate donor subtree list.
        :return: list of solutions. solutions list which are used as donor in crossover
        """
        options = []
        for i, donor in enumerate(donors):
            if not solution.solution_equal(recipient, donor, as_tree=True):
                options.append(i)
        return options
