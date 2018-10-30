import random
from gplib.solutions import solution
from gplib.operator import AbstractOperator


class MLPS_Crossover(AbstractOperator):

    def __init__(self, problem, stop_after_one=False, donor_order='random'):
        super(MLPS_Crossover, self).__init__()
        self.stop_after_one = stop_after_one
        self.donor_order = donor_order
        self.problem = problem

    def __call__(self, recipient, cross_points, donors):
        ##cross_points: list of tuple, (parent of crosspoint, children index)
        random.shuffle(cross_points)
        for cross_point in cross_points:
            self.improve(recipient, cross_point, donors)

    def improve(self, recipient, cross_point, donors):

        options = self.get_options(recipient, donors)

        if self.donor_order == 'random':
            random.shuffle(options)

        for index in options:
            donor = donors[index]
            stop = self.donate(recipient, cross_point, donor)

            if stop or self.stop_after_one:
                break

        del options

    def donate(self, recipient, cross_point, donor):
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
        options =[]
        for i, donor in enumerate(donors):
            if not solution.solution_equal(recipient, donor, as_tree=True):
                options.append(i)
        return options



