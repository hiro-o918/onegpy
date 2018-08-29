import copy
import random

from gplib.solutions.node import node_equal, get_all_node, get_graph_to_target, calc_node_depth, copy_nodes_along_graph


class Solution(object):
    def __init__(self, root):
        # TODO type check if ``root'' is node.Node
        self.root = root
        self.previous_fitness = None
        self._depth = None
        self._n_nodes = None

    @property
    def depth(self):
        if self._depth is None:
            set_solution_depth(self)

        return self._depth

    @depth.setter
    def depth(self, _):
        msg = 'To set depth to solution, use the function {}'\
            .format(set_solution_depth.__name__)
        raise Exception(msg)

    @property
    def n_nodes(self):
        if self._n_nodes is None:
            set_solution_n_nodes(self)

        return self._n_nodes

    @n_nodes.setter
    def n_nodes(self, _):
        msg = 'To set depth to solution, use the function {}'\
            .format(set_solution_depth.__name__)
        raise Exception(msg)


def calc_solution_depth(solution):
    # TODO type check if ``solution'' is Solution
    depth = calc_node_depth(solution.root)
    set_solution_depth(solution, depth)

    return depth


def calc_solution_n_nodes(solution):
    # TODO type check if ``solution'' is Solution
    nodes = get_all_node(solution.root)
    n_nodes = len(nodes)
    set_solution_n_nodes(solution, n_nodes)

    return n_nodes


def set_solution_depth(solution, depth=None):
    # TODO type check if ``solution'' is Solution
    if depth is None:
        solution._depth = calc_solution_depth(solution)
    else:
        solution._depth = depth


def set_solution_n_nodes(solution, n_nodes=None):
    # TODO type check if ``solution'' is Solution
    if n_nodes is None:
        solution._n_nodes = len(get_all_node(solution.root))
    else:
        solution._n_nodes = n_nodes


def solution_equal(solution_a, solution_b, as_tree=True):
    # TODO type check if ``solution'' is Solution
    if as_tree:
        if solution_a.n_nodes != solution_b.n_nodes:
            return False
        if solution_a.depth != solution_b.depth:
            return False

        return node_equal(solution_a.root, solution_b.root, as_tree=as_tree)
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


def copy_solution(solution, deep=False):
    if not deep:
        new_solution = solution.__class__(solution.root)
        if solution.previous_fitness is not None:
            new_solution.previous_fitness = copy.copy(solution.previous_fitness)
        return new_solution
    else:
        return copy.deepcopy(solution)


def replace_node(solution, replaced_node, new_node, destructive=True):
    """
    Replace a node in a solution by another node.
    :param solution: class Solution.
    :param replaced_node: class Node. A node to be replaced in the solution.
    :param new_node: class Node. A node set to replaced point in the solution.
    :param destructive: bool. If true, solution is replaced, keeping its object.
    Otherwise, new solution instance is created, protecting original solution.
    :return solution: class Solution.
    """

    # TODO: Type check if ``solution'' is Solution and ``nodes'' are Node
    # If replaced_node is root node
    if solution.root is replaced_node:
        if destructive:
            solution.root = new_node
        else:
            solution = Solution(new_node)

        set_solution_n_nodes(solution)
        set_solution_depth(solution)

        return solution

    # Otherwise
    try:
        graph = get_graph_to_target(solution.root, replaced_node)
    except ValueError:
        msg = 'replaced_node must be in a tree of a solution.'
        raise ValueError(msg)

    # Obtain terms to calculate the number of the nodes and the depth.
    point_depth = len(graph)
    n_rpl_nodes = len(get_all_node(replaced_node))
    n_new_nodes = len(get_all_node(new_node))
    rpl_node_depth = calc_node_depth(replaced_node)
    new_node_depth = calc_node_depth(new_node)

    # Core calculation and setting of depth and the number of nodes.
    depth = max(point_depth + new_node_depth - rpl_node_depth, solution.depth)
    n_nodes = solution.n_nodes + n_new_nodes - n_rpl_nodes

    # Obtain the replaced point
    if destructive:
        idx, parent = graph[-1]
    else:
        idx, parent, root = copy_nodes_along_graph(graph)
        solution = Solution(root)

    # Replace the replaced_node by new_node
    parent.children[idx] = new_node

    # Set the depth and n_nodes based on the results.
    set_solution_depth(solution, depth)
    set_solution_n_nodes(solution, n_nodes)

    return solution
