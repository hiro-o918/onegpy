# -*- coding: utf-8 -*-
import unittest
from gplib.operators import mutation as mu
from gplib.solutions import node, solution


class ExampleSolution(object):
    def __init__(self):
        self.s1 = self.create_tree()

    @staticmethod
    def create_tree():
        n1 = node.Node(0)
        n2 = node.Node(1)
        n3 = node.Node(2)
        n4 = node.Node(3)
        n5 = node.Node(2)
        node.set_children(n1, [n2, n3])
        node.set_children(n2, [n4, n5])

        return solution.Solution(n1)


class TestPointMutation(unittest.TestCase, ExampleSolution):
    def setUp(self):
        ExampleSolution.__init__(self)
        self.mutation = mu.PointMutation(1.0, function_dicts=[({0: 'a', 1: 'b'}), ({2: 'c', 3: 'd'})], mutation_type='onepoint')

    def test_onepoint_mutation(self):
        s2 = self.mutation(self.s1)
        for n in node.get_all_node(s2.root):
            if n.children is None:
                self.assertTrue(n.func_id in [2, 3])

            else:
                self.assertTrue(n.func_id in [0, 1])


class TestPopulationPointMutation(unittest.TestCase, ExampleSolution):
    def setUp(self):
        ExampleSolution.__init__(self)
        self.pop = [solution.Solution(node.Node()) for _ in range(100)]

    def test_onepoint_mutation(self):
        pop_mutation = mu.PopulationPointMutation(m_rate=1, function_dicts=[({0: 'a', 1: 'b'}), ({2: 'c', 3: 'd'})])
        new_pop = pop_mutation(self.pop)
        self.assertEqual(len(self.pop), len(new_pop))


if __name__ == '__main__':
    unittest.main()