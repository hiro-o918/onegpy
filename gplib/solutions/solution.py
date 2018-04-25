from gplib.solutions.node import node_equal


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

