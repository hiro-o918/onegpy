from gplib.solutions import node
from gplib.operator import selection
import random
import copy


# TODO: we must consider the number of parents and crossover points.
# TODO: + checking the number of parents and crossover points in each function
from gplib.solutions.solution import Solution


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

    @staticmethod
    def _crossover_core(parents, points):

        if parents[0].root is points[0]:
            root1 = parents[0].root
            parents[0].root = points[1]
        else:
            index1, subtree1, root1 = node.get_parent_node(parents[0].root, points[0], copied=True)
            subtree1.children[index1] = points[1]

        if parents[1].root is points[1]:
            root2 = parents[1].root
            parents[1].root = points[0]
        else:
            index2, subtree2, root2 = node.get_parent_node(parents[1].root, points[1], copied=True)
            subtree2.children[index2] = points[0]

        return [Solution(root1), Solution(root2)]

    @staticmethod
    def _crossover_loop(parents, points_set):
        if len(points_set[0]) > 1:
            msg = 'n point crossover is not developed'
            raise ValueError(msg)

        for points in zip(points_set[0], points_set[1]):
            parents = AbstractCrossover._crossover_core(parents, points)

        return parents

    def _crossover(self, parents):
        """
        function of applying crossover

        :param parents: list of Node objects. list of root node of parents
        :return: root node of new solution.
        """
        # TODO check len(parents) == 2
        if random.random() > self.c_rate:
            return parents
        else:
            if not self.destructive:
                parents = copy.deepcopy(parents)

            points_set = [self._get_crossover_point(parents[0]), self._get_crossover_point(parents[1])]
            parents = self._crossover_loop(parents, points_set)

        return parents


class OnePointCrossover(AbstractCrossover):

    def __init__(self, c_rate=1.0,destructive=True):
        super().__init__(c_rate, destructive)

    def __call__(self, parents):
        return self._crossover(parents)


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

