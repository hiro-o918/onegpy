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
        self.k = k
        self.replacement = replacement
        self.problem = problem

    def _cal_fitness(self, population):
        for solution in population:
            self.problem.fitness(solution)


class RandomSelection(AbstractSelection):

    def __init__(self, k, replacement):
        super().__init__(k, replacement, None)

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
        super().__init__(k, replacement, problem)

    def __call__(self, population):
        self._cal_fitness(population)
        k = self.k or len(population)
        chosen = []
        candidates = population[:]
        for i in range(k):
            best = max(candidates, key=lambda x: x.previous_fitness)
            chosen.append(chosen)
            candidates.remove(best)
        del candidates

        return chosen


class TournamentSelection(AbstractSelection):
    def __init__(self, tournament_size, problem, replacement=True, selection_size=None):
        if not replacement and selection_size is None:
            msg = 'If replacement is False, selection_size must be set.'
            raise TypeError(msg)
        self.selection_size = selection_size
        self.tournament_size = tournament_size
        if replacement:
            def append(solution, chosen):
                copy_append(solution, chosen)
        else:
            def append(solution, chosen):
                if not is_solution_in_pop(solution, chosen, False):
                    chosen.append(solution)

        self.append = append
        self.replacement = replacement
        super().__init__(k=tournament_size, replacement=replacement, problem=problem)

    def __call__(self, population):
        """
        Tournament Selection

        :param population: list of solutions.
        :return: list of solutions.
        """

        chosen = []
        self._cal_fitness(population)
        #TODO: we must check the original population size > k (it is also super redundant if k is almost equal to population size), if replacement=False.
        selection_size = self.selection_size or len(population)
        while len(chosen) < selection_size:
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
