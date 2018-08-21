# -*- coding: utf-8 -*-
import unittest
from gplib.solutions import node
from gplib.solutions.solution import Solution, solution_equal
from gplib.operators import selection as se


class EmptyProblem(object):
    def fitness(self, solution):
        pass


class ExampleSolutions(object):
    def __init__(self):
        self.population = []
        self.n_set = 2
        for i in range(self.n_set):
            s1 = self.create_tree_type1()
            s2 = self.create_tree_type2()
            s3 = self.create_tree_type3()
            s1.previous_fitness = 1
            s2.previous_fitness = 2
            s3.previous_fitness = 3
            self.population.append(s1)
            self.population.append(s2)
            self.population.append(s3)
        self.population = self.population * 2
    @staticmethod
    def create_tree_type1():
        n1 = node.Node(0)
        n2 = node.Node(1)
        n3 = node.Node(0)
        n4 = node.Node(1)
        n5 = node.Node(0)
        node.set_children(n1, [n2, n3])
        node.set_children(n2, [n4, n5])

        return Solution(n1)

    @staticmethod
    def create_tree_type2():
        n1 = node.Node(0)
        n2 = node.Node(1)
        n3 = node.Node(0)
        n4 = node.Node(1)
        n5 = node.Node(0)
        node.set_children(n1, [n2])
        node.set_children(n2, [n3, n4, n5])

        return Solution(n1)

    @staticmethod
    def create_tree_type3():
        n1 = node.Node(0)
        n2 = node.Node(1)
        n3 = node.Node(0)
        n4 = node.Node(1)
        n5 = node.Node(0)
        node.set_children(n1, [n2, n3, n4])
        node.set_children(n2, [n5])

        return Solution(n1)


class TestEliteSelection(unittest.TestCase, ExampleSolutions):
    def setUp(self):
        ExampleSolutions.__init__(self)
        self.problem = EmptyProblem()

    def test_random_selection(self):
        solution = se.elite_selection(self.population, self.problem)
        self.assertEqual(solution.previous_fitness, 3)


class TestSelectionBase(unittest.TestCase, ExampleSolutions):
    def setUp(self):
        ExampleSolutions.__init__(self)
        self.elite_size = 1
        self.selection_size = 3
        self.problem = EmptyProblem()

    def test_random_selection_base_with_replacement(self):
        selection = se.SelectionBase(self.selection_size, True, 'random')
        chosen = selection(self.population)
        self.assertEqual(self.selection_size, len(chosen))

    def test_random_selection_base_without_replacement(self):
        selection = se.SelectionBase(self.selection_size, False, 'random')
        chosen = selection(self.population)
        self.assertEqual(self.selection_size, len(chosen))

    def test_elite_selection_base_with_replacement(self):
        selection = se.SelectionBase(self.elite_size, True, 'elite', self.problem)
        chosen = selection(self.population)
        self.assertEqual(self.elite_size, len(chosen))

    def test_elite_selection_base_without_replacement(self):
        selection = se.SelectionBase(self.elite_size, False, 'elite', self.problem)
        chosen = selection(self.population)
        self.assertEqual(self.elite_size, len(chosen))


# class TestTournamentSelection(unittest.TestCase, ExampleSolutions):
#     def setUp(self):
#         ExampleSolutions.__init__(self)
#         self.tournament_size = 2
#         self.selection_size = 3
#         self.problem = EmptyProblem()
#
#     def test__call__with_replacement(self):
#         selection = TournamentSelection(self.tournament_size, self.problem, replacement=True)
#         chosen = selection.__call__(self.population)
#         self.assertEqual(len(self.population), len(chosen))
#
#         selection = TournamentSelection(self.tournament_size, self.problem,
#                                         replacement=True, selection_size=self.selection_size)
#         chosen = selection.__call__(self.population)
#         self.assertEqual(self.selection_size, len(chosen))
#
#     def test__call__without_replacement(self):
#         selection = TournamentSelection(self.tournament_size, self.problem, replacement=False,
#                                         selection_size=self.selection_size)
#         chosen = selection.__call__(self.population)
#         self.assertEqual(self.selection_size, len(chosen))
#
#         msg = 'If replacement is False, selection_size must be set.'
#         with self.assertRaises(TypeError, msg=msg):
#             TournamentSelection(self.tournament_size, self.problem, replacement=False)


class TestSelectionFunctions(unittest.TestCase, ExampleSolutions):
    def setUp(self):
        ExampleSolutions.__init__(self)

    def test_reduce_population(self):
        self.assertEqual(len(se.reduce_population(self.population)), 3)

    def test_copy_append(self):
        s1 = self.create_tree_type1()
        s2 = s1
        chosen = [s1]
        se.copy_append(s2, chosen)
        self.assertFalse(solution_equal(chosen[0], chosen[1], False))


if __name__ == '__main__':
    unittest.main()
