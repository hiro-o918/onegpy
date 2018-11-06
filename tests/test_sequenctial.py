import unittest

from onegpy.operator import AbstractOperator
from onegpy.operators.crossover import RandomSelection, PopulationOnePointCrossover, OnePointCrossover
from onegpy.sequential import Sequential
from onegpy.solutions.node import Node
from onegpy.solutions.solution import Solution


class TestSequential(unittest.TestCase):
    def setUp(self):
        self.sequential = Sequential([PopulationOnePointCrossover(c_rate=1)])
        self.pop = [Solution(Node()) for _ in range(100)]
        self.co = OnePointCrossover(c_rate=1)
        self.sl = RandomSelection(k=2, replacement=False)

    def test_add(self):
        msg = 'Expected type: {} not {}.'.format(AbstractOperator, bool)
        with self.assertRaises(TypeError, msg=msg):
            self.sequential(False)

        msg = 'Invalid operator:\n' \
              'Expected operator.n_in: None not {}'.format(self.co.n_in)
        with self.assertRaises(TypeError, msg=msg):
            self.sequential(self.co)

        self.assertIsNone(self.sequential.add(self.sl))
        self.assertIsNone(self.sequential.add(self.co))

    def test__call__(self):
        self.sequential.add(self.sl)
        self.sequential.add(self.co)

        self.assertEqual(2, len(self.sequential(self.pop)))

