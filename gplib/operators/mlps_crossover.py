import random
from gplib.solutions import solution
from gplib.operator import AbstractOperator


class MLPS_Crossover(AbstractOperator):
    """
    Crossover class for the MLPS-GP
    """
    def __init__(self, problem, stop_after_one=False, donor_order='random'):
        """
        :param problem: problem object. target problem.
        :param stop_after_one: bool. stop a crossover after the first donation.
        :param donor_order:
        """
        super(MLPS_Crossover, self).__init__()
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
        ##cross_points: list of tuple, (parent of crosspoint, children index)
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

        #TODO: check if the pre_node and the donor is same sub-tree, if so, we don't have to check the fitness of the new solution.
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
        options =[]
        for i, donor in enumerate(donors):
            if not solution.solution_equal(recipient, donor, as_tree=True):
                options.append(i)
        return options



