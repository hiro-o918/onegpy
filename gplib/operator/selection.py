import random
from gplib.solutions.solution import is_solution_in_population


class AbstractSelection(object):

    def __init__(self, k, replacement, problem):
        """
        :param k: int. The number of solutions which are selected.
        :param replacement: bool. sample with replacement
        :return: function of selection
        """
        self.k = k

        if replacement:
            self.rand_f = random.choices
        else:
            self.rand_f = random.sample

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
        return self.rand_f(population=population, k=self.k)


class TournamentSelection(AbstractSelection):
    def __init__(self, tournament_size, problem, replacement=True, selection_size=None):
        if not replacement and selection_size is None:
            msg = 'If replacement is False, selection_size must be set.'
            raise TypeError(msg)
        self.selection_size = selection_size
        self.tournament_size = tournament_size
        if replacement:
            def append(solution, chosen):
                return chosen.append(solution)
        else:
            def append(solution, chosen):
                if not is_solution_in_population(solution, chosen):
                    chosen.append(solution)

        self.append = append
        self.replacement = replacement
        super().__init__(k=tournament_size, replacement=False, problem=problem)

    def __call__(self, population):
        """
        Tournament Selection

        :param population: list of solutions.
        :param k: int. the number of solutions which are selected
        :return: list of solutions.
        """

        chosen = []
        self._cal_fitness(population)
        #TODO: we must check the original population size > k (it is also super redundant if k is almost equal to population size), if replacement=False.
        selection_size = self.selection_size or len(population)
        while len(chosen) < selection_size:
            candidates = self.rand_f(population=population, k=self.tournament_size)
            best = max(candidates, key=lambda x: x.previous_fitness)
            self.append(best, chosen)

        del population

        return chosen


def reduce_population(population):
    solutions = [population[0]]
    for s in population[1:]:
        if not is_solution_in_population(s, solutions):
            solutions.append(s)

    return solutions

