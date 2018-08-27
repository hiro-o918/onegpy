from abc import ABC

from gplib.operator import AbstractOperator, PopulationOperator, ProblemBasedOperator
from gplib.solutions import solution, node
import random


class AbstractInitializer(AbstractOperator, ProblemBasedOperator, ABC):
    def __init__(self, n_in, n_out, problem):
        AbstractOperator.__init__(self, n_in, n_out)
        ProblemBasedOperator.__init__(self, problem)

    @property
    def func_dicts(self):
        return self.problem.func_dicts

    @func_dicts.setter
    def func_dicts(self, _):
        self.not_changeable_warning()

    @func_dicts.deleter
    def func_dicts(self):
        self.not_changeable_warning()


class RandomInitializer(AbstractInitializer):
    def __init__(self, t_prob, max_depth, problem):
        super(RandomInitializer, self).__init__(n_in=0, n_out=1, problem=problem)
        self.t_prob = t_prob
        self.max_depth = max_depth

    def __call__(self):
        """Generating a new solution.

                # Arguments
                    t_prob: float((0, 1]). probability of terminal node.
                    max_depth: int. The limit of depth of the solution.
                    func_dicts: tuple of dictionary

                # Return
                    solution
                    :param **kwargs:
            """
        # TODO check t_prob range and all the arguments are correct.
        # TODO check problem is class Problem
        n_nonterminal = len(self.func_dicts[0])
        n_terminal = len(self.func_dicts[1])

        def new_node(parent, depth):
            current_node = node.Node()
            if self.t_prob > random.random() or depth == self.max_depth:
                func_id = random.randrange(0, n_terminal)
            else:
                current_node.children = []
                func_id = random.randrange(0, n_nonterminal)
                n_child = node.get_n_children(func_id, self.func_dicts[0])
                for _ in range(n_child):
                    new_node(current_node, depth + 1)

            node.set_id(current_node, func_id)

            if parent is not None:
                parent.children.append(current_node)
            else:
                return current_node

        root = new_node(None, 0)

        return solution.Solution(root)


class PopulationRandomInitializer(RandomInitializer, PopulationOperator):
    def __init__(self, k, t_prob, max_depth, problem):
        self.k = k
        RandomInitializer.__init__(self, t_prob=t_prob, max_depth=max_depth, problem=problem)
        PopulationOperator.__init__(self, 0, k)

    def __call__(self):
        population = [RandomInitializer.__call__(self) for _ in range(self.k)]

        return population

