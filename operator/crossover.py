from solutions import node
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
        self.c_rate = c_rate
        self.destructive = destructive

    def __call__(self, parents):
        points = []
        for parent in parents:
            points.append(self.__get_crossover_point__(parent))
        return self.__crossover__(parents, points)

    def __get_crossover_point__(self, parent):
        """
        Abstract function

        :param parent:
        :return:
        """
        raise NotImplementedError

    def __crossover__(self, parents, points):
        """
        function of applying crossover

        :param parents: list of Node objects. list of root node of parents
        :param points: list of Node objects. list of replaced node
        :return: root node of new solution.
        """

        if not self.destructive:
            parents = copy.deepcopy(parents)
        index1, subtree1 = node.get_parent_node(parents[0], points[0])
        index2, subtree2 = node.get_parent_node(parents[1], points[1])

        if random.random() < self.c_rate:
            subtree1.children[index1] = points[1]
            subtree2.children[index2] = points[0]

        return parents


class OnePointCrossover(AbstractCrossover):

    def __init__(self, c_rate=1.0,destructive=True):
        super().__init__(c_rate, destructive)

    def __get_crossover_point__(self, parent, k =1):
        node_list = node.get_all_node(parent)
        point = random.sample(node_list, k=k)
        return point