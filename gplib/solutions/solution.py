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


def solution_equal(solution_a, solution_b, as_tree=True):
    # TODO type check if ``solution'' is Solution
    if not as_tree:
        node_equal(solution_a.root, solution_b.root, as_tree=as_tree)
    else:
        return solution_a is solution_b


def is_solution_in_pop(solution, population, as_tree=False):
    """
    check the tree of ``solution'' is in ``population'' or not
    :param solution: Solution object
    :param population: list of Solution object
    :param as_tree: If as_tree is true, solution is compared by all the nodes' structure
                    Otherwise, compared by object id.
    :return: bool
    """
    for s in population:
        if solution_equal(solution, s, as_tree):
            return True
    return False


def select_random_points(solution, k):
    """
    Obtain `k` points in the solution at random.
    :param solution: class `Solution`
    :param k: the number of points to obtain
    :return: a list of class `Node`
    """
    # TODO check k <= len(nodelist) or get min(k, len(nodelist))
    # TODO type check if ``solution'' is Solution
    node_list = get_all_node(solution.root)
    points = random.sample(node_list, k=k)

    return points
