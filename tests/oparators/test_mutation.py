# -*- coding: utf-8 -*-
import unittest
from gplib.operators import mutation as mu
from gplib.solutions import node, solution


class ExampleParents(object):
    def __init__(self):
        self.s1 = self.create_tree()

    @staticmethod
    def create_tree():
        n1 = node.Node(0)
        n2 = node.Node(1)
        n3 = node.Node(0)
        n4 = node.Node(1)
        n5 = node.Node(0)
        node.set_children(n1, [n2, n3])
        node.set_children(n2, [n4, n5])

        return solution.Solution(n1)


class TestPointMutation(unittest.TestCase, ExampleParents):
    def setUp(self):
        ExampleParents.__init__(self)
        self.mutation = mu.PointMutation(1.0, function_dicts=[({0: 'a', 1: 'b'}), ({0: 'c', 1: 'd'})], mutation_type='onepoint')

    def test_onepoint_mutation(self):
        self.mutation(self.s1)


if __name__ == '__main__':
    unittest.main()