# -*- coding: utf-8 -*-

import unittest

from gplib.solutions import node


class TestNodeFunctions(unittest.TestCase):

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

    def test_set_id(self):
        func_id = 0
        node.set_id(self.n1, func_id)

        self.assertEqual(self.n1.func_id, func_id)

    def test_get_n_children(self):
        func_id = 0
        func = self.function_dict[func_id]

        self.assertEqual(node.get_n_children(func_id, self.function_dict), func.n_children)

    def test_set_children(self):
        children = [self.n2, self.n3]
        node.set_children(self.n1, children)

        self.assertEqual(self.n1.children, children)

    def test__copy_nodes_along_graph(self):
        node.set_id(self.n1, 0)
        node.set_id(self.n2, 1)
        node.set_children(self.n1, [self.n2, self.n3])
        node.set_children(self.n2, [self.n4, self.n5])
        node.set_children(self.n3, [self.n6])

        graph = [(0, self.n1), (1, self.n2)]
        pos, parent, root = node.copy_nodes_along_graph(graph)
        self.assertEqual(pos, 1)
        self.assertTrue(node.node_equal(parent, self.n2))
        self.assertTrue(node.node_equal(root, self.n1, as_tree=True))
        self.assertFalse(parent is self.n2)
        self.assertFalse(root is self.n1)

    def test_get_parent_node(self):
        node.set_id(self.n1, 0)
        node.set_id(self.n2, 1)
        node.set_children(self.n1, [self.n2, self.n3])
        node.set_children(self.n2, [self.n4, self.n5, self.n6])
        self.assertEqual(node.get_parent_node(self.n1, self.n4), (0, self.n2))

        msg = 'There is no parent of root.'
        with self.assertRaises(ValueError, msg=msg):
            node.get_parent_node(self.n1, self.n1)

        msg = 'Invalid arguments: cannot find parent.'
        with self.assertRaises(ValueError, msg=msg):
            node.get_parent_node(node.Node(), node.Node())

    def test_get_graph_to_target(self):
        node.set_id(self.n1, 0)
        node.set_id(self.n2, 1)
        node.set_children(self.n1, [self.n2, self.n3])
        node.set_children(self.n2, [self.n4, self.n5, self.n6])
        graph = [(0, self.n1), (0, self.n2)]
        self.assertEqual(node.get_graph_to_target(self.n1, self.n4), graph)

        msg = 'There is no parent of root.'
        with self.assertRaises(ValueError, msg=msg):
            node.get_graph_to_target(self.n1, self.n1)

        msg = 'Invalid arguments: cannot find parent.'
        with self.assertRaises(ValueError, msg=msg):
            node.get_graph_to_target(node.Node(), node.Node())

    def test_get_all_node(self):
        node.set_id(self.n1, 0)
        node.set_id(self.n2, 1)
        node.set_children(self.n1, [self.n2, self.n3])
        node.set_children(self.n2, [self.n4, self.n5, self.n6])
        all_nodes = [self.n1, self.n2, self.n4, self.n5, self.n6, self.n3]

        self.assertEqual(node.get_all_node(self.n1), all_nodes)

    def test_calc_node_depth(self):
        node.set_id(self.n1, 0)
        node.set_id(self.n2, 1)
        node.set_children(self.n1, [self.n2, self.n3])
        node.set_children(self.n2, [self.n4, self.n5, self.n6])

        self.assertEqual(node.calc_node_depth(self.n1), 2)

    def test_node_equal(self):
        node.set_id(self.n1, 0)
        node.set_id(self.n2, 0)
        node.set_id(self.n3, 0)
        node.set_id(self.n4, 0)
        node.set_id(self.n5, 0)
        node.set_id(self.n6, 0)
        node.set_children(self.n1, [self.n2, self.n3])
        node.set_children(self.n4, [self.n5, self.n6])

        self.assertTrue(node.node_equal(self.n1, self.n4))
        self.assertTrue(node.node_equal(self.n1, self.n4, as_tree=True))
        node.set_id(self.n2, 1)
        self.assertFalse(node.node_equal(self.n1, self.n3))
        self.assertFalse(node.node_equal(self.n2, self.n3))
        self.assertFalse(node.node_equal(self.n1, self.n4, as_tree=True))

    def test_node_array_equal(self):
        self.assertTrue(node.node_array_equal([self.n1, self.n2], [self.n3, self.n4]))
        node.set_id(self.n4, 0)
        self.assertFalse(node.node_array_equal([self.n1, self.n2], [self.n3, self.n4]))

    def test_func_id_checker(self):
        with self.assertRaises(ValueError):
            node.func_id_checker(-1)
        with self.assertRaises(TypeError):
            node.func_id_checker('1')
        self.assertEqual(node.func_id_checker(1), None)

    def test_node_checker(self):
        with self.assertRaises(TypeError):
            node.node_checker(1)
        self.assertEqual(node.node_checker(self.n1), None)

    def test_nodes_checker(self):
        with self.assertRaises(TypeError):
            node.nodes_checker([1, 1])
        self.assertEqual(node.nodes_checker([self.n1, self.n2]), None)

    def test_children_checker(self):
        le_msg = 'Expected type: {} not {}.'.format(node.Node, list)
        with self.assertRaises(TypeError, msg=le_msg):
            node.children_checker(self.n1)

        ne_msg = 'Expected type: {} not {}.'.format(node.Node, int)
        with self.assertRaises(TypeError, msg=ne_msg):
            node.children_checker([1, 2])

        self.assertEqual(node.children_checker([self.n1, self.n2]), None)

    def test_get_all_terminal_nodes(self):
        node.set_id(self.n1, 0)
        node.set_id(self.n2, 1)
        node.set_children(self.n1, [self.n2, self.n3])
        node.set_children(self.n2, [self.n4, self.n5])
        node.set_children(self.n3, [self.n6])

        terminal_nodes = node.get_all_terminal_nodes(self.n1)
        expected_terminal_nodes = [self.n4, self.n5, self.n6]

        for n in terminal_nodes:
            self.assertTrue(n in expected_terminal_nodes)

    def test_get_nonterminal_nodes(self):
        node.set_id(self.n1, 0)
        node.set_id(self.n2, 1)
        node.set_children(self.n1, [self.n2, self.n3])
        node.set_children(self.n2, [self.n4, self.n5])
        node.set_children(self.n3, [self.n6])

        nonterminal_nodes = node.get_all_nonterminal_nodes(self.n1)
        expected_nonterminal_nodes = [self.n1, self.n2, self.n3]

        for n in nonterminal_nodes:
            self.assertTrue(n in expected_nonterminal_nodes)


if __name__ == '__main__':
    unittest.main()
