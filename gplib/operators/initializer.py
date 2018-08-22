from gplib.solutions import solution, node
import random


def initialize(t_prob, max_depth, function_dicts):
    """Generating a new solution.

        # Arguments
            t_prob: float((0, 1]). probability of terminal node.
            max_depth: int. The limit of depth of the solution.
            func_dicts: tuple of dictionary

        # Return
            solution
    """
    # TODO check t_prob range and all the arguments are correct.
    n_nonterminal = len(function_dicts[0])
    n_terminal = len(function_dicts[1])

    def new_node(parent, depth):
        current_node = node.Node()
        if t_prob > random.random() or depth == max_depth:
            func_id = random.randrange(0, n_terminal)
        else:
            current_node.children = []
            func_id = random.randrange(0, n_nonterminal)
            n_child = node.get_n_children(func_id, function_dicts[0])
            for _ in range(n_child):
                new_node(current_node, depth + 1)

        node.set_id(current_node, func_id)

        if parent is not None:
            parent.children.append(current_node)
        else:
            return current_node

    root = new_node(None, 0)

    return solution.Solution(root)


def population_initialize(t_prob, max_depth, pop_size, function_dicts):
    pop = []
    for i in range(pop_size):
        pop.append(initialize(t_prob, max_depth, function_dicts))
    return pop
