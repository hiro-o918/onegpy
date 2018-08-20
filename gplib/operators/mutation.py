from gplib.solutions import node
import random

class AbstractMutation(object):
    def __init__(self, m_rate):
        """
        Abstract class of mutation.

        :param m_rate: float([0, 1.0]). mutaion rate for each iteration
        """
        self.m_rate = m_rate

    def __call__(self, solution):
        raise NotImplementedError

class BitStringMutation(AbstractMutation):
    def __init__(self, m_rate):
        super.__init__(m_rate)

    def __call__(self, solution, function_dict):
        """
            Mutation points in the solution at random.
            :param solution: class `Solution`
            :param function_dict: dictionary of functions
            :return: solution.
        """
        points = node.get_all_node(solution.root)
        for point in points:
            if random.random() <= self.m_rate:
                func_id = random.choice(list(function_dict.keys()))
                node.set_id(point, func_id)
        return solution
