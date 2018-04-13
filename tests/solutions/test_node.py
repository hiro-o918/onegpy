# -*- coding: utf-8 -*-
"""
Created on 11 4 2018/04/11 18:36 2018

@author: Hironori Yamamoto
"""
import unittest

from solutions import node as nd


class TestNode(unittest.TestCase):
    def test_Node(self):
        n1 = nd.Node()
        self.assertEqual(n1.func_id, -1)
        self.assertEqual(n1.children, None)

        n2 = nd.Node(1)
        self.assertEqual(n2.func_id, 1)


class TestFunction(unittest.TestCase):
    def test_Function(self):
        f1 = nd.Function(1)
        self.assertEqual(f1.n_children, 1)
        self.assertEqual(f1.eval, None)
        # TODO create test for argument ``eval'' after defined what is eval


class TestNodeFunction(unittest.TestCase):

    def setUp(self):
        self.n1 = nd.Node()
        self.n2 = nd.Node()
        self.n3 = nd.Node()
        self.n4 = nd.Node()
        self.n5 = nd.Node()
        self.n6 = nd.Node()

        self.f1 = nd.Function(2)
        self.f2 = nd.Function(3)
        self.function_dict = {0: self.f1, 1: self.f2}

    def test_set_id(self):
        func_id = 0
        nd.set_id(self.n1, func_id)

        self.assertEqual(self.n1.func_id, func_id)

    def test_get_n_children(self):
        func_id = 0
        func = self.function_dict[func_id]

        self.assertEqual(nd.get_n_children(func_id, self.function_dict), func.n_children)

    def test_set_children(self):
        children = [self.n2, self.n3]
        nd.set_children(self.n1, children)

        self.assertEqual(self.n1.children, children)

    def test_get_parent_node(self):
        nd.set_id(self.n1, 0)
        nd.set_id(self.n2, 1)
        nd.set_children(self.n1, [self.n2, self.n3])
        nd.set_children(self.n2, [self.n4, self.n5, self.n6])

        self.assertEqual(nd.get_parent_node(self.n1, self.n4), (0, self.n2))

    def test_get_all_node(self):
        nd.set_id(self.n1, 0)
        nd.set_id(self.n2, 1)
        nd.set_children(self.n1, [self.n2, self.n3])
        nd.set_children(self.n2, [self.n4, self.n5, self.n6])

        all_nodes = [self.n1, self.n2, self.n4, self.n5, self.n6, self.n3]

        self.assertEqual(nd.get_all_node(self.n1), all_nodes)

    def test__func_id_checker(self):
        with self.assertRaises(ValueError):
            nd._func_id_checker(-1)
        with self.assertRaises(TypeError):
            nd._func_id_checker('1')
        self.assertEqual(nd._func_id_checker(1), None)

    def test__node_checker(self):
        with self.assertRaises(TypeError):
            nd._node_checker(1)
        self.assertEqual(nd._node_checker(self.n1), None)

    def test__nodes_checker(self):
        with self.assertRaises(TypeError):
            nd._nodes_checker(1, 1)
        self.assertEqual(nd._nodes_checker(self.n1, self.n2), None)

    def test__children_checker(self):
        le_msg = 'Expected type: {} not {}.'.format(nd.Node, list)
        with self.assertRaises(TypeError, msg=le_msg):
            nd._children_checker(self.n1)
        # self.assertEqual(le.msg, 'Expected type: {}'.format(list))

        ne_msg = 'Expected type: {} not {}.'.format(nd.Node, int)
        with self.assertRaises(TypeError, msg=ne_msg):
            nd._children_checker([1, 2])

        self.assertEqual(nd._children_checker([self.n1, self.n2]), None)


if __name__ == '__main__':
    unittest.main()
