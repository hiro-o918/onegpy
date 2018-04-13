from solutions import solution
from solutions import node
import random

def initialize(t_prob, max_depth, n_terminal, n_nonterminal, function_dict):
    """Generating a new solution.

        # Arguments
            t_prob: float((0, 1]). probability of terminal node.
            max_depth: int. The limit of depth of the solution.
            n_terminal: int.
            n_nonterminal: int.
            func_map: dictionary

        # Return
            solution
    """
    def new_node(parent, depth):
        if depth < max_depth:
            n_child = node.get_n_children(parent.id, function_dict)
            children = []
            for _ in n_child:
                child = node.Node()
                if t_prob > random.random():
                    func_id = random.randint(n_terminal)
                else:
                    func_id = random.randint(n_nonterminal)
                    new_node(child, depth + 1)
                node.set_id(child, func_id)
                children.append(child)

            # adding the child to parent, if it has parent
            if parent is not None:
                node.set_children(node, children)
            else:
                return child

    root = new_node(None, 0)

    return solution.Solution(root)