from gplib.solutions import node
from gplib.operators import selection
from gplib.operator import AbstractOperator
import random


# TODO: we must consider the number of parents and crossover points.
# TODO: + checking the number of parents and crossover points in each function
from gplib.solutions.solution import Solution, select_random_points


def crossover(parents, points):
    if parents[0].root is points[0]:
        root1 = points[1]
    else:
        graph1 = node.get_graph_to_target(parents[0].root, points[0])
        index1, subtree1, root1 = node.copy_nodes_along_graph(graph1)
        subtree1.children[index1] = points[1]

    if parents[1].root is points[1]:
        root2 = points[0]
    else:
        graph2 = node.get_graph_to_target(parents[1].root, points[1])
        index2, subtree2, root2 = node.copy_nodes_along_graph(graph2)
        subtree2.children[index2] = points[0]

    parents = [Solution(root1), Solution(root2)]

    return parents


def destructive_crossover(parents, points):
    if parents[0].root is points[0]:
        parents[0].root = points[1]
    else:
        index1, subtree1 = node.get_parent_node(parents[0].root, points[0])
        subtree1.children[index1] = points[1]

    if parents[1].root is points[1]:
        parents[1].root = points[0]
    else:
        index2, subtree2 = node.get_parent_node(parents[1].root, points[1])
        subtree2.children[index2] = points[0]

    return parents


def get_crossover_core(destructive=True):
    if not destructive:
        return crossover
    else:
        return destructive_crossover


class OnePointCrossover(AbstractOperator):
    def __init__(self, c_rate, destructive=True):
        """
        One point crossover.
        :param c_rate: Crossover rate.
        :param destructive: If destructive is true, parents also are changed.
                            Otherwise, parents are copied and keep their structures.
        """
        super(OnePointCrossover, self).__init__()
        self.c_rate = c_rate
        self.destructive = destructive

    def __call__(self, parents):
        if len(parents) != 2:
            msg = 'parents must be a list consisting of two solutions'
            raise ValueError(msg)

        points = [select_random_points(p, 1)[0] for p in parents]

        if random.random() > self.c_rate:
            return parents
        else:
            crossover_core = get_crossover_core(self.destructive)
            return crossover_core(parents, points)


def get_default_crossover():
    selection_operator = selection.RandomSelection(k=2, replacement=False)
    crossover_operator = OnePointCrossover(c_rate=0.5)

    def do_crossover(population):
        new_population = []
        while len(population) > len(new_population):
            children = crossover_operator(selection_operator(population))
            new_population.extend(children)
        del population

        return new_population

    return do_crossover
