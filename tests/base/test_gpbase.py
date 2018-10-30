import unittest

from gplib.operator import AbstractOperator
from gplib.operators import PopulationRandomInitializer, TournamentSelection
from gplib.operators.crossover import RandomSelection, PopulationOnePointCrossover, OnePointCrossover
from gplib.problem import AbstractProblem
from gplib.sequential import Sequential
from gplib.solutions.node import Node
from gplib.solutions.solution import Solution
from gplib.base import gpbase
from gplib.loggers import loggers
from gplib.solutions import node
from tests.test_problem import EmptyProblem


class TestSequential(unittest.TestCase):
    def setUp(self):
        self.problem = EmptyProblem()
        self.sequential = Sequential([PopulationOnePointCrossover(c_rate=1),
                                      TournamentSelection(k=10, tournament_size=3, problem=self.problem)])
        self.initializer = PopulationRandomInitializer(k=10, t_prob=0.5, max_depth=3, problem=self.problem)

    def test_gp(self):
        # self.sequential.add(self.sl)
        # self.sequential.add(self.co)

        gp = gpbase.PopulationGP(initializer=self.initializer, sequential=self.sequential,
                                 n_generations=10, logger=loggers.DefaultLogger())
        gp.__call__()


if __name__ == '__main__':
    unittest.main()