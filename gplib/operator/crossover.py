from gplib.solutions import node
from gplib.operator import selection
import random
import copy


# TODO: we must consider the number of parents and crossover points.
# TODO: + checking the number of parents and crossover points in each function

class AbstractCrossover(object):
    def __init__(self, c_rate, destructive=True):
        """
        Abstract class of crossover.

        :param c_rate: float([0, 1.0]). crossover rate for each iteration
        :param destructive: bool. if it is destructive operator or not(keep parents or not)
        """
        # TODO check c_rate in range (0, 1]
        self.c_rate = c_rate
        self.destructive = destructive

    def __call__(self, parents):
        raise NotImplementedError

    @staticmethod
    def _get_crossover_point(parent, k=1):
        # TODO check k <= len(nodelist) or get min(k, len(nodelist))
        node_list = node.get_all_node(parent.root)
        points = random.sample(node_list, k=k)
        return points

    def _crossover(self, parents, points_set):
        """
        function of applying crossover

        :param parents: list of Node objects. list of root node of parents
        :param points_set: list of Node objects. list of replaced node
        :return: root node of new solution.
        """

        # TODO check len(parents) == 2
        if not self.destructive:
            parents = copy.deepcopy(parents)

        if random.random() < self.c_rate:
            for point1, point2 in zip(points_set[0], points_set[1]):
                if parents[0].root is point1:
                    parents[0].root = point2
                else:
                    index1, subtree1 = node.get_parent_node(parents[0].root, point1)
                    subtree1.children[index1] = point1

                if parents[1].root is point2:
                    parents[1].root = point1
                else:
                    index2, subtree2 = node.get_parent_node(parents[1].root, point2)
                    subtree2.children[index2] = point2

        return parents


class OnePointCrossover(AbstractCrossover):

    def __init__(self, c_rate=1.0,destructive=True):
        super().__init__(c_rate, destructive)

    def __call__(self, parents):
        points_set = []
        for parent in parents:
            points_set.append(self._get_crossover_point(parent))
        return self._crossover(parents, points_set)


def get_default_crossover():

    selection_operator = selection.RandomSelection(k=2, replacement=False)
    crossover_operator = OnePointCrossover(c_rate=0.6)

    def do_crossover(population):
        new_population = []
        while len(population) > len(new_population):
            children = crossover_operator(selection_operator(population))
            new_population.extend(children)
        del population

        return new_population

    return do_crossover

