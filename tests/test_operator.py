import unittest

from onegpy.operator import build_population_operator, PopulationOperator, operator_checker
from onegpy.operators.crossover import PopulationOnePointCrossover, OnePointCrossover
from onegpy.solutions.node import Node
from onegpy.solutions.solution import Solution


class TestPopulationOperatorAdapter(unittest.TestCase):
    def setUp(self):
        self.co = PopulationOnePointCrossover(c_rate=1)

    def test__get_default_generator_builder(self):
        n_pop = 100
        population = [Solution(Node())] * n_pop

        generator = self.co._get_default_generator_builder()(population)
        for pop in generator:
            self.assertEqual(len(pop), self.co.operator.n_in)


class TestOperatorFunctions(unittest.TestCase):
    def setUp(self):
        self.operator = OnePointCrossover(c_rate=1)
        self.cls_name = 'PopCOO'
        self.pop_operator = build_population_operator(self.operator, cls_name=self.cls_name)

    def test_build_population_operator(self):
        self.assertIsInstance(self.pop_operator, PopulationOperator)
        self.assertIsInstance(self.pop_operator, self.operator.__class__)
        self.assertEqual(self.pop_operator.__class__.__name__, self.cls_name)
        # check a default class name
        pop_operator = build_population_operator(self.operator)
        self.assertEqual(pop_operator.__class__.__name__, 'PopulationOnePointCrossover')

    def test_operator_checker(self):
        self.assertIsNone(operator_checker(self.operator))

        msg = 'Expected type: {} not {}.'.format(self.operator, bool)
        with self.assertRaises(TypeError, msg=msg):
            operator_checker(False)

    def test_pop_operator_checker(self):
        self.assertIsNone(operator_checker(self.pop_operator))

        msg = 'Expected type: {} not {}.'.format(self.pop_operator, bool)
        with self.assertRaises(TypeError, msg=msg):
            operator_checker(False)


if __name__ == '__main__':
    unittest.main()
