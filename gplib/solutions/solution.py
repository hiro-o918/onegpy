import random

from gplib.solutions.node import node_equal, get_all_node


class Solution(object):
    def __init__(self, root):
        # TODO type check if ``root'' is node.Node
        self.root = root
        self.previous_fitness = None


def get_depth(solution):
    # TODO type check if ``solution'' is Solution
    d_list = []

    def cal_depth(c_node, depth):
        if c_node.children is not None:
            for c in c_node.children:
                cal_depth(c, depth+1)
        else:
            d_list.append(depth)

    cal_depth(solution.root, 0)

    return max(d_list)


def solution_equal(solution_a, solution_b):
    # TODO type check if ``solution'' is Solution
    return node_equal(solution_a.root, solution_b.root, as_tree=True)


def is_solution_in_population(solution, population):
    """
    check the tree of ``solution'' is in ``population'' or not
    :param solution: Solution object
    :param population: list of Solution object
    :return: bool
    """
    for s in population:
        if solution_equal(solution, s):
            return True
    return False


def select_random_points(solution, k):
    """
    Obtain `k` points in the solution at random.
    :param solution: class `Solution`
    :param k: the number of points to obtain
    :return: a list of class `Node`
    """
    # TODO type check if ``solution'' is Solution
    node_list = get_all_node(solution.root)
    points = random.sample(node_list, k=k)

    return points
