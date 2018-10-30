from abc import ABC

from gplib.operator import AbstractOperator, PopulationOperator, ProblemBasedOperator
from gplib.problem import problem_checker
from gplib.solutions import solution, node
import random

from gplib.utils.checkers import prob_checker


class AbstractInitializer(AbstractOperator, ProblemBasedOperator, ABC):
    def __init__(self, n_in, n_out, problem):
        problem_checker(problem)
        AbstractOperator.__init__(self, n_in, n_out)
        ProblemBasedOperator.__init__(self, problem)

    @property
    def func_bank(self):
        return self.problem.func_bank

    @func_bank.setter
    def func_bank(self, _):
        self.not_changeable_warning()

    @func_bank.deleter
    def func_bank(self):
        self.not_changeable_warning()

    def _get_nonterminal_list(self):
        nonterminal_list = []
        child_dict = self.func_bank.children_dict
        for key, id_list in child_dict.items():
            if key != 0:
                nonterminal_list.extend(id_list)
        if len(nonterminal_list) == 0:
            raise ValueError("the number of non-terminal must be more than 0. but it has no non-terminal node")
        return nonterminal_list

    def _get_terminal_list(self):
        terminal_list = self.func_bank.get_function_list(0)

        if terminal_list is None:
            raise ValueError("function bank must have terminal list, but it has no terminal list.")
        elif len(terminal_list) == 0:
            raise ValueError("the number of terminal must be more than 0, but it has no terminal node.")
        return terminal_list


class RandomInitializer(AbstractInitializer):
    """
    Generating a new solution.
    """

    def __init__(self, t_prob, max_depth, problem):
        """
        :param t_prob: float((0, 1]). probability of terminal node.
        :param max_depth: int. The limit of depth of the solution.
        :param problem: problem object. problem to solve
        """
        prob_checker(t_prob)
        super(RandomInitializer, self).__init__(n_in=0, n_out=1, problem=problem)
        self.t_prob = t_prob
        self.max_depth = max_depth
        self.nonterminal_list = self._get_nonterminal_list()
        self.terminal_list = self._get_terminal_list()

    def __call__(self):
        """
        Generating a new solution.
        :return: solution object. solution
        """


        def new_node(parent, depth):
            current_node = node.Node()
            if self.t_prob > random.random() or depth == self.max_depth:
                func_id = random.choice(self.terminal_list)
            else:
                current_node.children = []
                func_id = random.choice(self.nonterminal_list)
                n_child = node.get_n_children(func_id, self.func_bank.get_function_list())
                for _ in range(n_child):
                    new_node(current_node, depth + 1)

            node.set_id(current_node, func_id)

            if parent is not None:
                parent.children.append(current_node)
            else:
                return current_node

        root = new_node(None, 0)

        return solution.Solution(root)


class PopulationTerminalInitializer(AbstractInitializer, PopulationOperator):
    """
    Generating all solutions which have an only terminal node.
    """
    def __init__(self, problem):
        """
        :param k: int. the number of solutions to generate
        :param problem: problem object. problem to solve
        """
        AbstractInitializer.__init__(self, n_in=0, n_out=None, problem=problem)
        self.terminal_list = self._get_terminal_list()
        PopulationOperator.__init__(self, 0, len(self.terminal_list))

    def __call__(self):
        """
        Generating all solutions which have an only terminal node.
        :return: list of solution object. list of all terminal solutions
        """
        def make_node(func_id):
            new_node = node.Node()
            node.set_id(new_node, func_id)
            return new_node

        population = [solution.Solution(make_node(func_id)) for func_id in self.terminal_list]
        return population


class PopulationRandomInitializer(RandomInitializer, PopulationOperator):
    """
    Generating solutions using random initializer.
    """
    def __init__(self, k, t_prob, max_depth, problem):
        """
        :param k: int. the number of solutions to generate.
        :param t_prob: float((0, 1]). probability of terminal node.
        :param max_depth: int. The limit of depth of the solution.
        :param problem: problem object. problem to solve
        """
        self.k = k
        RandomInitializer.__init__(self, t_prob=t_prob, max_depth=max_depth, problem=problem)
        PopulationOperator.__init__(self, 0, k)

    def __call__(self):
        population = [RandomInitializer.__call__(self) for _ in range(self.k)]

        return population

