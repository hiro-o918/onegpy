from gplib.solutions import node
import random


class AbstractMutation(object):
    def __init__(self, m_rate):
        """
        Abstract class of mutation.

        :param m_rate: float([0, 1.0]). mutation rate for each iteration
        """
        self.m_rate = m_rate

    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class BitStringMutation(AbstractMutation):
    def __init__(self, m_rate):
        super(BitStringMutation, self).__init__(m_rate)

    def __call__(self, solution, function_dicts):
        """
            Mutation points in the solution at random.
            :param solution: class `Solution`
            :param function_dicts: list of dictionary of functions
                                    dicts[0] nonterminal. dicts[1] terminal.
            :return: solution.
        """
        points = node.get_all_node(solution.root)
        for point in points:
            if random.random() <= self.m_rate:
                if point.children is None:
                    node.set_id(point, random.choice(list(function_dicts[1].keys())))
                else:
                    node.set_id(point, random.choice(list(function_dicts[0].keys())))
        return solution
