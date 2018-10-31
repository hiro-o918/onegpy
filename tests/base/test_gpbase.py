import unittest

from gplib.operators import PopulationRandomInitializer, TournamentSelection
from gplib.operators.crossover import PopulationOnePointCrossover
from gplib.sequential import Sequential
from gplib.base import gpbase
from gplib.terminal_condition import TerminalCondition
from gplib.terminator import GenerationTerminator
from gplib.viewers import observer
from tests.test_problem import EmptyProblem


class TestSequential(unittest.TestCase):
    def setUp(self):
        self.problem = EmptyProblem()
        self.sequential = Sequential([PopulationOnePointCrossover(c_rate=1),
                                      TournamentSelection(k=10, tournament_size=3, problem=self.problem)])
        self.initializer = PopulationRandomInitializer(k=10, t_prob=0.5, max_depth=3, problem=self.problem)

        self.terminal_condition = TerminalCondition([GenerationTerminator(10)])

    def test_gp(self):
        gp = gpbase.PopulationGP(initializer=self.initializer, sequential=self.sequential,
                                 n_generations=10, terminal_condition=self.terminal_condition,
                                 observer=observer.DefaultObserver(verbose=3))
        gp.__call__()


if __name__ == '__main__':
    unittest.main()