# -*- coding: utf-8 -*-
import unittest
from tests.test_problem import EmptyProblem
from onegpy.solutions import node, solution
from onegpy.operators import localsearch


class ExampleSolution(object):
    def __init__(self, root_id=2):
        self.s1 = self.create_tree(root_id=root_id)

    @staticmethod
    def create_tree(root_id):
        # odd numbers are ids of terminal nodes, the others are non-terminal nodes.
        n1 = node.Node(root_id)
        n2 = node.Node(2)

        n3 = node.Node(1)
        n4 = node.Node(3)
        n5 = node.Node(5)

        node.set_children(n1, [n2, n3])
        node.set_children(n2, [n4, n5])

        s = solution.Solution(n1)
        solution.set_previous_fitness(s, root_id)

        return s


class TestImprove(unittest.TestCase, ExampleSolution):

    def setUp(self):
        self.root_id = 2
        ExampleSolution.__init__(self, root_id=self.root_id)
        self.problem = EmptyProblem()

    def test_improve(self):
        root = self.s1.root
        candidate_id = 0
        improved = localsearch.improve(self.s1,  root, candidate_id, self.problem)
        self.assertEqual(improved, False)
        self.assertEqual(self.s1.root.func_id, self.root_id)

        candidate_id = 4
        improved = localsearch.improve(self.s1, root, candidate_id, self.problem)
        self.assertEqual(improved, True)
        self.assertEqual(self.s1.root.func_id, candidate_id)


class TestAllCheck(unittest.TestCase, ExampleSolution):

    def setUp(self):
        self.root_id = 2
        ExampleSolution.__init__(self, root_id=self.root_id)
        self.problem = EmptyProblem()

    def test_all_check(self):
        root = self.s1.root
        c1 = root.children[0]
        c2 = root.children[1]

        improved = localsearch.all_check(self.s1, root, self.problem)
        self.assertEqual(improved, True)
        self.assertEqual(root.func_id, 4)

        improved = localsearch.all_check(self.s1, c1, self.problem)
        self.assertEqual(improved, False)

        improved = localsearch.all_check(self.s1, c2, self.problem)
        self.assertEqual(improved, False)


class TestStopImprovement(unittest.TestCase, ExampleSolution):

    def setUp(self):
        self.root_id = 0
        ExampleSolution.__init__(self, root_id=self.root_id)
        self.problem = EmptyProblem()

    def test_stop_improvement_with_shuffle(self):
        root = self.s1.root
        c1 = root.children[0]
        c2 = root.children[1]
        is_shuffle = True

        flg2 = False
        flg4 = False
        for i in range(100):
            improved = localsearch.stop_improvement(self.s1, root, self.problem, is_shuffle=is_shuffle)
            if i == 0:
                self.assertEqual(improved, True)
            if root.func_id == 2:
                flg2 = True
                node.set_id(root, self.root_id)
                solution.set_previous_fitness(self.s1, self.root_id)
            elif root.func_id == 4:
                flg4 = True
                node.set_id(root, self.root_id)
                solution.set_previous_fitness(self.s1, self.root_id)

            if flg2 and flg4:
                break

        self.assertEqual(flg2 and flg4, True)

        improved = localsearch.stop_improvement(self.s1, c1, self.problem, is_shuffle=is_shuffle)
        self.assertEqual(improved, False)

        improved = localsearch.stop_improvement(self.s1, c2, self.problem, is_shuffle=is_shuffle)
        self.assertEqual(improved, False)

    def test_stop_improvement_without_shuffle(self):
        root = self.s1.root
        c1 = root.children[0]
        c2 = root.children[1]
        is_shuffle = False

        improved = localsearch.stop_improvement(self.s1, root, self.problem, is_shuffle=is_shuffle)
        self.assertEqual(improved, True)
        self.assertEqual(root.func_id, 2)

        improved = localsearch.stop_improvement(self.s1, c1, self.problem, is_shuffle=is_shuffle)
        self.assertEqual(improved, False)

        improved = localsearch.stop_improvement(self.s1, c2, self.problem, is_shuffle=is_shuffle)
        self.assertEqual(improved, False)


