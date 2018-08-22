import random

from gplib.operator import PopulationOperator
from gplib.solutions.solution import is_solution_in_pop, copy_solution


class AbstractSelection(PopulationOperator):

    def __init__(self, k, replacement, problem):
        """
        :param k: int. The number of solutions which are selected.
        :param replacement: bool. sample with replacement
        :return: function of selection
        """
        super(AbstractSelection, self).__init__()
        self.k = k
        self.replacement = replacement
        self.problem = problem

    def _cal_fitness(self, population):
        for solution in population:
            self.problem.fitness(solution)

    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class RandomSelection(AbstractSelection):

    def __init__(self, k, replacement):
        super(RandomSelection, self).__init__(k, replacement, None)

    def __call__(self, population):
        """Random Selection

            # Arguments
                population: list of individual. a candidate set of solutions.

            # Returns
                list of solutions.
        """
        if self.replacement:
            chosen = []
            for i in range(self.k):
                copy_append(random.choice(population), chosen)
            return chosen
        else:
            return random.sample(population, self.k)


class EliteSelection(AbstractSelection):
    """Elite Selection

        # Returns
           list of solutions.
    """
    def __init__(self, k, problem, replacement=False):
        super(EliteSelection, self).__init__(k, replacement, problem)

    def __call__(self, population):
        self._cal_fitness(population)
        k = self.k or len(population)
        chosen = []
        candidates = population[:]
        for i in range(k):
            best = max(candidates, key=lambda x: x.previous_fitness)
            chosen.append(best)
            candidates.remove(best)
        del candidates

        return chosen


class TournamentSelection(AbstractSelection):
    def __init__(self, k, tournament_size, problem, replacement=True):
        if not replacement and k is None:
            msg = 'If replacement is False, selection_size must be set.'
            raise TypeError(msg)

        self.tournament_size = tournament_size
        super(TournamentSelection, self).__init__(k=k, replacement=replacement, problem=problem)

        if replacement:
            def append(solution, chosen):
                copy_append(solution, chosen)
        else:
            def append(solution, chosen):
                if not is_solution_in_pop(solution, chosen, False):
                    chosen.append(solution)

        self.append = append
        self.replacement = replacement
        super(TournamentSelection, self).__init__(k=tournament_size, replacement=replacement, problem=problem)

    def __call__(self, population):
        """
        Tournament Selection

        :param population: list of solutions.
        :return: list of solutions.
        """

        chosen = []
        self._cal_fitness(population)
        #TODO: we must check the original population size > k (it is also super redundant if k is almost equal to population size), if replacement=False.
        k = self.k or len(population)
        while len(chosen) < k:
            candidates = random.sample(population, self.tournament_size)
            best = max(candidates, key=lambda x: x.previous_fitness)
            self.append(best, chosen)

        del population

        return chosen


def reduce_population(population):
    solutions = [population[0]]
    for s in population[1:]:
        if not is_solution_in_pop(s, solutions, as_tree=True):
            solutions.append(s)

    return solutions


def copy_append(solution, chosen):
    if is_solution_in_pop(solution, chosen, as_tree=False):
        chosen.append(copy_solution(solution, deep=True))
    else:
        chosen.append(solution)
