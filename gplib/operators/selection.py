import random
from gplib.solutions.solution import is_solution_in_pop, copy_solution


class AbstractSelection(object):

    def __init__(self, problem):
        """
        :return: function of selection
        """
        self.problem = problem

    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    def _cal_fitness(self, population):
        for solution in population:
            self.problem.fitness(solution)


class RandomSelection(AbstractSelection):

    def __init__(self):
        super().__init__(None)

    def __call__(self, population):
        """Random Selection

            # Arguments
                population: list of individual. a candidate set of solutions.

            # Returns
                solution.
        """
        return random.choice(population=population)


class EliteSelection(AbstractSelection):
    def __init__(self, problem):
        super().__init__(problem=problem)

    def __call__(self, population):
        """
        Tournament Selection

        :param population: list of solutions.
        :return: solution.
        """
        self._cal_fitness(population)
        return max(population, key=lambda x: x.previous_fitness)


class SelectionBase(object):
    def __init__(self, selection_size, replacement, selection_type=None):
        """
            Selection Base

            :param selection_size: number of selection solutions.
            :param selection_type: string. type of selection.
            :param replacement: bool. sample with replacement
            :return: list of solutions.
        """
        self.selection_size = selection_size
        self.selection_type = selection_type
        self.replacement = replacement

    def __call__(self, population):
        selection_core = self.get_selection()
        chosen = []
        if self.replacement:
            for i in range(self.selection_size):
                copy_append(selection_core(population), chosen)
        else:
            candidates = population[:]
            for i in range(self.selection_size):
                solution = selection_core(candidates)
                chosen.append(solution)
                candidates.remove(solution)
        return chosen

    def get_selection(self):
        if self.selection_type == 'elite':
            return EliteSelection
        else:
            return RandomSelection


def reduce_population(population):
    solutions = [population[0]]
    for s in population[1:]:
        if not is_solution_in_pop(s, solutions):
            solutions.append(s)

    return solutions


def copy_append(solution, chosen):
    if is_solution_in_pop(solution, chosen, as_tree=False):
        chosen.append(copy_solution(solution, deep=True))
    else:
        chosen.append(solution)