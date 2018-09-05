# -*- coding: utf-8 -*-
import unittest
from gplib.operators import mutation as mu
from gplib.problem import AbstractProblem
from gplib.solutions import node, solution
from tests.test_problem import EmptyProblem


class ExampleSolution(object):
    def __init__(self):
        self.s1 = self.create_tree()

    @staticmethod
    def create_tree():
        # odd numbers are ids of terminal nodes, the others are non-terminal nodes.
        n1 = node.Node(0)
        n2 = node.Node(2)
        n3 = node.Node(1)
        n4 = node.Node(3)
        n5 = node.Node(5)
        node.set_children(n1, [n2, n3])
        node.set_children(n2, [n4, n5])

        return solution.Solution(n1)


class TestPointMutation(unittest.TestCase, ExampleSolution):
    def setUp(self):
        ExampleSolution.__init__(self)
        self.problem = EmptyProblem()
        self.mutation = mu.PointMutation(1.0, problem=self.problem, mutation_type='onepoint')

    def test_onepoint_mutation(self):
        s2 = self.mutation(self.s1)
        for n in node.get_all_node(s2.root):
            func_list = self.problem.func_bank.get_function_list(n_children=len(n.children))
            self.assertTrue(n.func_id in func_list)


class TestPopulationPointMutation(unittest.TestCase, ExampleSolution):
    def setUp(self):
        ExampleSolution.__init__(self)
        self.problem = EmptyProblem()
        self.pop = [solution.Solution(node.Node()) for _ in range(100)]

    def test_onepoint_mutation(self):
        pop_mutation = mu.PopulationPointMutation(m_rate=1, problem=self.problem)
        new_pop = pop_mutation(self.pop)
        self.assertEqual(len(self.pop), len(new_pop))


if __name__ == '__main__':
    unittest.main()