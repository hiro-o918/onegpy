# -*- coding: utf-8 -*-
import unittest
from gplib.solutions import node
from gplib.solutions.solution import is_solution_in_population, Solution
from gplib.operator import RandomSelection, TournamentSelection, reduce_population


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


class TestRandomSelection(unittest.TestCase, ExampleSolutions):
    def setUp(self):
        ExampleSolutions.__init__(self)
        self.k = 3
        self.problem = EmptyProblem()

    def test__call__with_replacement(self):
        selection = RandomSelection(self.k,  replacement=True)
        chosen = selection.__call__(self.population)
        self.assertEqual(len(chosen), self.k)

    def test__call__without_replacement(self):
        selection = RandomSelection(self.k, replacement=False)
        chosen = selection.__call__(self.population)
        self.assertEqual(self.k, len(chosen))


class TestTournamentSelection(unittest.TestCase, ExampleSolutions):
    def setUp(self):
        ExampleSolutions.__init__(self)
        self.tournament_size = 2
        self.problem = EmptyProblem()

    def test__call__with_replacement(self):
        selection = TournamentSelection(self.tournament_size, self.problem, replacement=True)
        n_population = len(self.population)
        chosen = selection.__call__(self.population)
        self.assertEqual(len(chosen), n_population)

    # def test__call__without_replacement(self):
    #     selection = TournamentSelection(self.tournament_size, self.problem, replacement=False)
    #     n_population = len(self.population)
    #     chosen = selection.__call__(self.population)
    #     self.assertEqual(min(n_population, len(reduce_population(chosen))), len(chosen))
    #
    #     for i in range(len(chosen)):
    #         self.assertFalse(is_solution_in_population(chosen[i], (chosen[:i] + chosen[i + 1:])))


class TestSelectionFunctions(unittest.TestCase, ExampleSolutions):
    def setUp(self):
        ExampleSolutions.__init__(self)

    def test_reduce_population(self):
        self.assertEqual(len(reduce_population(self.population)), 3)


if __name__ == '__main__':
    unittest.main()