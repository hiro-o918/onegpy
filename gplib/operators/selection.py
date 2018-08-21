import random
from gplib.solutions.solution import is_solution_in_pop, copy_solution


def random_selection(population, problem):
    return random.choice(population=population)


def elite_selection(population, problem):
    _cal_fitness(population, problem)
    return max(population, key=lambda x: x.previous_fitness)


class SelectionBase(object):
    def __init__(self, selection_size, replacement, selection_name, problem=None):
        """
            Selection Base

            :param selection_size: number of selection solutions.
            :param selection_name: string. type of selection.
            :param replacement: bool. sample with replacement
            :return: list of solutions.
        """
        self.selection_size = selection_size
        self.selection_name = selection_name
        self.problem = problem
        self.replacement = replacement

    def __call__(self, population):
        selection_core = get_selection_core(self.selection_name)
        chosen = []
        if self.replacement:
            for i in range(self.selection_size):
                copy_append(selection_core(population, self.problem), chosen)
        else:
            candidates = population[:]
            for i in range(self.selection_size):
                solution = selection_core(candidates, self.problem)
                chosen.append(candidates.pop(solution))
            del candidates
        return chosen


def get_selection_core(selection_name):
    if selection_name == 'elite':
        return elite_selection
    else:
        return random_selection


def _cal_fitness(population, problem):
    for solution in population:
        problem.fitness(solution)


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
