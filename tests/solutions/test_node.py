# -*- coding: utf-8 -*-
"""
Created on 11 4 2018/04/11 18:36 2018

@author: Hironori Yamamoto
"""
import unittest

from solutions import node as nd


class TestNode(unittest.TestCase):

    def setUp(self):
        self.n1 = nd.Node()
        self.n2 = nd.Node()
        self.n3 = nd.Node()
        self.n4 = nd.Node()
        self.n5 = nd.Node()
        self.n6 = nd.Node()

        self.f1 = nd.Function(2)
        self.f2 = nd.Function(3)
        self.function_dict = {'0': self.f1, '1': self.f2}

    def test_set_id(self):
        func_id = 0
        nd.set_id(self.n1, func_id)

        self.assertEqual(self.n1.func_id, func_id)

    def test_get_n_children(self):
        func_id = 0
        func = self.function_dict[str(func_id)]

        self.assertEqual(nd.get_n_children(func_id, self.function_dict), func.n_children)

    def test_set_children(self):
        children = [self.n2, self.n3]
        nd.set_children(self.n1, children)

        self.assertEqual(self.n1.children, children)

    def test_get_parent_node(self):
        # TODO After checking this development in detail, fix
        nd.set_id(self.n1, 0)
        nd.set_id(self.n2, 1)
        nd.set_children(self.n1, [self.n2, self.n3])
        nd.set_children(self.n2, [self.n4, self.n5, self.n6])

        self.assertEqual(nd.get_parent_node(self.n1, self.n4), (0, self.n2))

    def test_get_all_node(self):
        # TODO After checking this development in detail, fix
        nd.set_id(self.n1, 0)
        nd.set_id(self.n2, 1)
        nd.set_children(self.n1, [self.n2, self.n3])
        nd.set_children(self.n2, [self.n4, self.n5, self.n6])

        all_nodes = [self.n1, self.n2, self.n4, self.n5, self.n6, self.n3]

        self.assertEqual(nd.get_all_node(self.n1), all_nodes)


if __name__ == '__main__':
    unittest.main()
