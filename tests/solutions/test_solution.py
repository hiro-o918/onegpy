# -*- coding: utf-8 -*-
import unittest

from gplib.solutions import node, solution


class TestSolutionFunctions(unittest.TestCase):
    def setUp(self):
        self.n1 = node.Node()
        self.n2 = node.Node()
        self.n3 = node.Node()
        self.n4 = node.Node()
        self.n5 = node.Node()
        self.n6 = node.Node()

        self.f1 = node.Function(2)
        self.f2 = node.Function(3)
        # ``function_dict'' is not separated based on kinds of nodes
        # such as non-terminal nodes or terminal nodes here.
        self.function_dict = {0: self.f1, 1: self.f2}

        node.set_id(self.n1, 0)
        node.set_id(self.n2, 1)
        node.set_children(self.n1, [self.n2, self.n3])
        node.set_children(self.n2, [self.n4, self.n5, self.n6])

        self.s = solution.Solution(self.n1)

    def test_get_depth(self):
        self.assertEqual(solution.get_depth(self.s), 2)

    def test_solution_equal(self):
        na1 = node.Node()
        na2 = node.Node()
        na3 = node.Node()
        na4 = node.Node()
        na5 = node.Node()
        na6 = node.Node()

        node.set_id(na1, 0)
        node.set_id(na2, 1)
        node.set_children(na1, [na2, na3])
        node.set_children(na2, [na4, na5, na6])
        sa = solution.Solution(na1)
        self.assertTrue(solution.solution_equal(self.s, sa))
        na4 = node.Node(0)
        node.set_children(na2, [na4, na5, na6])
        self.assertFalse(solution.solution_equal(self.s, sa))


if __name__ == '__main__':
    unittest.main()