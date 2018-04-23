# -*- coding: utf-8 -*-
import unittest
import copy
from operator import itemgetter
import pandas
from gplib.operator import crossover
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


class TestAbstractCrossover(unittest.TestCase, ExampleParents):
    def setUp(self):
        ExampleParents.__init__(self)
        self.c_rate = 1
        self.crossover = crossover.AbstractCrossover(self.c_rate)

    def test__get_crossover_point(self):
        k = 1
        points = self.crossover._get_crossover_point(self.s1, k)
        for point in points:
            self.assertTrue(isinstance(point, node.Node))
        # self.assertEqual(len(points), k)

    def test_crossover_core(self):
        s1_nodes = node.get_all_node(self.s1.root)
        s2_nodes = node.get_all_node(self.s2.root)
        points_set = [[s1_nodes[0]], [s2_nodes[2]]]

        expected_nodes1 = [node.Node(1)]
        expected_nodes2 = [node.Node(0), node.Node(1), node.Node(0), node.Node(1), node.Node(1),
                           node.Node(0), node.Node(0), node.Node(0), node.Node(0)]
        node.set_children(expected_nodes2[0], [expected_nodes2[1], expected_nodes2[8]])
        node.set_children(expected_nodes2[1], [expected_nodes2[2], expected_nodes2[7]])
        node.set_children(expected_nodes2[2], [expected_nodes2[3], expected_nodes2[6]])
        node.set_children(expected_nodes2[3], [expected_nodes2[4], expected_nodes2[5]])

        new_s1, new_s2 = self.crossover._crossover_loop(self.parents, points_set)
        self.assertTrue(node.node_equal(expected_nodes1[0], new_s1.root, as_tree=True))
        self.assertTrue(node.node_equal(expected_nodes2[0], new_s2.root, as_tree=True))

    def test__crossover(self):
        self.crossover.destructive = False
        new_s1, new_s2 = self.crossover._crossover([self.s1.root, self.s2.root])
        self.assertNotEqual(self.s1, new_s1)
        self.assertNotEqual(self.s2, new_s2)
        self.crossover.destructive = True
        new_s1, new_s2 = self.crossover._crossover([self.s1.root, self.s2.root])
        self.assertEqual(self.s1, new_s1)
        self.assertEqual(self.s2, new_s2)



