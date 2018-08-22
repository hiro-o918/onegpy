import unittest

from gplib.operator import build_population_operator, PopulationOperator, operator_checker
from gplib.operators.crossover import PopulationOnePointCrossover, OnePointCrossover
from gplib.solutions.node import Node
from gplib.solutions.solution import Solution


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

    def test_build_population_operator(self):
        pop_operator = build_population_operator(self.operator)
        self.assertIsInstance(pop_operator, PopulationOperator)

    def test_operator_checker(self):
        self.assertIsNone(operator_checker(self.operator))

        msg = 'Expected type: {} not {}.'.format(self.operator, bool)
        with self.assertRaises(TypeError, msg=msg):
            operator_checker(False)


if __name__ == '__main__':
    unittest.main()
