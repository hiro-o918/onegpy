# -*- coding: utf-8 -*-
import unittest
import warnings
from gplib.operators import crossover as co
from gplib.solutions import node, solution


class ExampleParents(object):
    def __init__(self):
        self.s1 = self.create_tree()
        self.s2 = self.create_tree()
        self.parents = [self.s1, self.s2]

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


class TestCrossover(unittest.TestCase, ExampleParents):
    def setUp(self):
        ExampleParents.__init__(self)

    def test_crossover(self):
        s1_nodes = node.get_all_node(self.parents[0].root)
        s2_nodes = node.get_all_node(self.parents[1].root)
        points = [s1_nodes[0], s2_nodes[2]]

        expected_nodes1 = [node.Node(1)]
        expected_nodes2 = [node.Node(0), node.Node(1), node.Node(0), node.Node(1), node.Node(1),
                           node.Node(0), node.Node(0), node.Node(0), node.Node(0)]

        node.set_children(expected_nodes2[0], [expected_nodes2[1], expected_nodes2[8]])
        node.set_children(expected_nodes2[1], [expected_nodes2[2], expected_nodes2[7]])
        node.set_children(expected_nodes2[2], [expected_nodes2[3], expected_nodes2[6]])
        node.set_children(expected_nodes2[3], [expected_nodes2[4], expected_nodes2[5]])

        new_s1, new_s2 = co.crossover(self.parents, points)
        self.assertTrue(node.node_equal(expected_nodes1[0], new_s1.root, as_tree=True))
        self.assertTrue(node.node_equal(expected_nodes2[0], new_s2.root, as_tree=True))
        self.assertFalse(self.parents[0] is new_s1)
        self.assertFalse(self.parents[1] is new_s2)

    def test_destructive_crossover_core(self):
        s1_nodes = node.get_all_node(self.parents[0].root)
        s2_nodes = node.get_all_node(self.parents[1].root)
        points = [s1_nodes[0], s2_nodes[2]]

        expected_nodes1 = [node.Node(1)]
        expected_nodes2 = [node.Node(0), node.Node(1), node.Node(0), node.Node(1), node.Node(1),
                           node.Node(0), node.Node(0), node.Node(0), node.Node(0)]

        node.set_children(expected_nodes2[0], [expected_nodes2[1], expected_nodes2[8]])
        node.set_children(expected_nodes2[1], [expected_nodes2[2], expected_nodes2[7]])
        node.set_children(expected_nodes2[2], [expected_nodes2[3], expected_nodes2[6]])
        node.set_children(expected_nodes2[3], [expected_nodes2[4], expected_nodes2[5]])

        new_s1, new_s2 = co.destructive_crossover(self.parents, points)
        self.assertTrue(node.node_equal(expected_nodes1[0], new_s1.root, as_tree=True))
        self.assertTrue(node.node_equal(expected_nodes2[0], new_s2.root, as_tree=True))
        self.assertTrue(self.parents[0] is new_s1)
        self.assertTrue(self.parents[1] is new_s2)


class TestOnePointCrossover(unittest.TestCase, ExampleParents):
    def setUp(self):
        ExampleParents.__init__(self)
        self.destructive_co = co.OnePointCrossover(c_rate=1, destructive=True)
        self.non_destructive_co = co.OnePointCrossover(c_rate=1, destructive=False)

    def test_crossover(self):
        with warnings.catch_warnings(record=True) as w:
            self.destructive_co.destructive = False
            self.assertTrue(len(w) == 1)
            msg = 'This variable is not changeable.' \
                  ' Thus, the operation has no effect.'
            self.assertSequenceEqual(msg, str(w[-1].message))

        self.destructive_co(self.parents)

    def test_destructive_crossover(self):
        self.destructive_co.destructive = True
        self.destructive_co(self.parents)


if __name__ == '__main__':
    unittest.main()