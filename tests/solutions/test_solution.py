# -*- coding: utf-8 -*-
import copy
import unittest

from gplib.solutions import node, solution


class TestSolutionFunctions(unittest.TestCase):
    def setUp(self):
        self.n1 = node.Node(0)
        self.n2 = node.Node(1)
        self.n3 = node.Node(0)
        self.n4 = node.Node(1)
        self.n5 = node.Node(0)
        self.n6 = node.Node(1)

        self.f1 = node.Function(2)
        self.f2 = node.Function(3)
        # ``function_dict'' is not separated based on kinds of nodes
        # such as non-terminal nodes or terminal nodes here.
        self.function_dict = {0: self.f1, 1: self.f2}

        node.set_children(self.n1, [self.n2, self.n3])
        node.set_children(self.n2, [self.n4, self.n5, self.n6])

        self.s1 = solution.Solution(self.n1)
        self.depth = 2
        self.n_nodes = 6

    def test_calc_solution_depth(self):
        self.assertEqual(solution.calc_solution_depth(self.s1), self.depth)

    def test_calc_solution_n_nodes(self):
        self.assertEqual(solution.calc_solution_n_nodes(self.s1), self.n_nodes)

    def test_set_solution_depth(self):
        solution.set_solution_depth(self.s1, 0)
        self.assertEqual(self.s1.depth, 0)
        solution.set_solution_depth(self.s1)
        self.assertEqual(self.s1.depth, self.depth)

    def test_set_solution_n_nodes(self):
        solution.set_solution_n_nodes(self.s1, 0)
        self.assertEqual(self.s1.n_nodes, 0)
        solution.set_solution_n_nodes(self.s1)
        self.assertEqual(self.s1.n_nodes, self.n_nodes)

    def test_solution_equal(self):
        na1 = node.Node(0)
        na2 = node.Node(1)
        na3 = node.Node(0)
        na4 = node.Node(1)
        na5 = node.Node(0)
        na6 = node.Node(1)

        node.set_id(na1, 0)
        node.set_id(na2, 1)
        node.set_children(na1, [na2, na3])
        node.set_children(na2, [na4, na5, na6])
        sa = solution.Solution(na1)
        self.assertTrue(solution.solution_equal(self.s1, sa, True))
        self.assertFalse(solution.solution_equal(self.s1, sa, False))
        na4 = node.Node(0)
        node.set_children(na2, [na4, na5, na6])
        self.assertFalse(solution.solution_equal(self.s1, sa, True))

    def test_select_random_points(self):
        k = 2
        points = solution.select_random_points(self.s1, k)
        for point in points:
            self.assertTrue(isinstance(point, node.Node))
        self.assertEqual(len(points), k)

    def test_non_destructive_replace_node(self):
        na1 = node.Node(1)
        na2 = node.Node(0)

        node.set_id(na1, 0)
        node.set_id(na2, 1)
        node.set_children(na1, [na2])
        original_s1 = copy.deepcopy(self.s1)
        new_s1 = solution.replace_node(self.s1, self.n2, na1, destructive=False)

        expected_nodes = [node.Node(0), node.Node(0), node.Node(1), node.Node(0)]
        node.set_children(expected_nodes[0], [expected_nodes[1], expected_nodes[3]])
        node.set_children(expected_nodes[1], [expected_nodes[2]])

        self.assertTrue(node.node_equal(new_s1.root, expected_nodes[0], as_tree=True))
        self.assertEqual(new_s1.n_nodes, len(expected_nodes))
        self.assertEqual(new_s1.depth, 2)
        # Check whether the original solution is protected.
        self.assertTrue(solution.solution_equal(original_s1, self.s1))
        self.assertFalse(self.s1 is new_s1)

    def test_destructive_replace_node(self):
        na1 = node.Node(1)
        na2 = node.Node(0)

        node.set_id(na1, 0)
        node.set_id(na2, 1)
        node.set_children(na1, [na2])
        original_s1 = copy.deepcopy(self.s1)
        new_s1 = solution.replace_node(self.s1, self.n2, na1, destructive=True)

        expected_nodes = [node.Node(0), node.Node(0), node.Node(1), node.Node(0)]
        node.set_children(expected_nodes[0], [expected_nodes[1], expected_nodes[3]])
        node.set_children(expected_nodes[1], [expected_nodes[2]])

        self.assertTrue(node.node_equal(new_s1.root, expected_nodes[0], as_tree=True))
        self.assertEqual(new_s1.n_nodes, len(expected_nodes))
        self.assertEqual(new_s1.depth, 2)
        # Check whether the original solution is NOT protected.
        self.assertFalse(solution.solution_equal(original_s1, new_s1))
        self.assertTrue(self.s1 is new_s1)


if __name__ == '__main__':
    unittest.main()