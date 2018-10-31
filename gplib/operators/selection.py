import random
from abc import ABC

from gplib.operator import PopulationOperator, ProblemBasedOperator
from gplib.solutions.solution import is_solution_in_pop, copy_solution


class AbstractSelection(PopulationOperator, ABC):
    """
    Abstract class for selection.
    """
    def __init__(self, k, replacement):
        """
        :param k: int. The number of solutions which are selected.
        :param replacement: bool. If replacement is True, duplicated solutions are selected.
        Otherwise, all the solutions are unique in an output population.
        :return: function of selection
        """
        super(AbstractSelection, self).__init__(n_out=k)
        self._k = k
        self.replacement = replacement

    @property
    def k(self):
        return self._k

    @k.setter
    def k(self, _):
        self.not_changeable_warning()

    @k.deleter
    def k(self):
        self.not_changeable_warning()


class AbstractProblemBasedSelection(AbstractSelection, ProblemBasedOperator, ABC):
    """
    Abstract class for problem based selection.
    """
    def __init__(self, k, problem, replacement):
        """
        :param k: int. The number of solutions which are selected.
        :param problem: problem object. target problem.
        :param replacement: bool. If replacement is True, duplicated solutions are selected.
        Otherwise, all the solutions are unique in an output population.
        """
        """

        """
        AbstractSelection.__init__(self, k=k, replacement=replacement)
        ProblemBasedOperator.__init__(self, problem)
        self._k = k
        self.replacement = replacement

    def _cal_fitness(self, population):
        for solution in population:
            self.problem.fitness(solution)


class RandomSelection(AbstractSelection):
    """
    Random selection class.
    """
    def __init__(self, k, replacement):
        """

        :param k: int. The number of solutions which are selected.
        :param replacement: bool. If replacement is True, duplicated solutions are selected.
        Otherwise, all the solutions are unique in an output population.
        """
        super(RandomSelection, self).__init__(k, replacement)

    def __call__(self, population):
        """
        Select k solutions at random.
        :param population: list of solutions. a candidate set of solutions.
        :return: list of solutions.
        """
        if self.replacement:
            chosen = []
            # Contains the bool values indicates whether the id's solution is added to chosen.
            is_picked_idxs = [False] * len(population)

            for i in range(self.k):
                picked_idx = random.randrange(0, len(population))
                candidates = population[picked_idx]
                # If candidate is appended to chosen, copy it.
                if is_picked_idxs[picked_idx]:
                    chosen.append(copy_solution(candidates, deep=True))
                else:
                    chosen.append(candidates)
                    is_picked_idxs[picked_idx] = True

            return chosen
        else:
            return random.sample(population, self.k)


class EliteSelection(AbstractProblemBasedSelection):
    """
    Elite selection class
    """

    def __init__(self, k, problem, replacement=False):
        """
        :param k: int. The number of solutions which are selected.
        :param problem: problem object. target problem.
        :param replacement: bool. If replacement is True, duplicated solutions are selected.
        Otherwise, all the solutions are unique in an output population.
        """
        super(EliteSelection, self).__init__(k, problem, replacement)

    def __call__(self, population):
        """
        Select k best solutions.
        :param population: list of solutions. a candidate set of solutions.
        :return: list of solutions.
        """
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


class TournamentSelection(AbstractProblemBasedSelection):
    """
    Tournament selection class.
    """

    def __init__(self, k, tournament_size, problem, replacement=True):
        """
        :param k: int. The number of solutions which are selected.
        :param tournament_size: int. tournament size of the selection.
        :param problem: problem object. target problem.
        :param replacement: bool. If replacement is True, duplicated solutions are selected.
        Otherwise, all the solutions are unique in an output population.
        """
        if not replacement and k is None:
            msg = 'If replacement is False, selection_size must be set.'
            raise TypeError(msg)

        self.tournament_size = tournament_size
        super(TournamentSelection, self).__init__(k=k, problem=problem, replacement=replacement)
        self.replacement = replacement

    def __call__(self, population):
        """
        Tournament Selection

        :param population: list of solutions. population of solutions.
        :return: list of solutions.
        """

        chosen = []
        self._cal_fitness(population)
        k = self.k or len(population)
        if (not self.replacement) and len(population) < k:
            raise ValueError("A tournament k must be less than population size if replacement false, "
                             "but it got k = {}, population size = {}".format(k, len(population)))

        # Contains the bool values indicates whether the id's solution is added to chosen.
        is_picked_idxs = [False] * len(population)
        solution_idxs = list(range(len(population)))
        while len(chosen) < k:
            candidates_idxs = random.sample(solution_idxs, self.tournament_size)
            best_idx = max(candidates_idxs, key=lambda x: population[x].previous_fitness)

            # If replacement is not true, all the solutions in chosen must have unique trees.
            if not self.replacement \
                    and (is_picked_idxs[best_idx]   # if already picked, continue.
                         # if chosen contains solution which has same structure as candidates, continue.
                         or is_solution_in_pop(population[best_idx], chosen, as_tree=True)):
                continue
            # If candidate is appended to chosen, copy it.
            if is_picked_idxs[best_idx]:
                candidate = copy_solution(population[best_idx], deep=True)
            else:
                candidate = population[best_idx]
                is_picked_idxs[best_idx] = True

            chosen.append(candidate)

        del population

        return chosen


def reduce_population(population):
    """
    Remove the solutions which have same tree structure.
    :param population: list of solutions. population of solutions.
    :return: list of solutions. the dumped population.
    """
    solutions = [population[0]]
    for s in population[1:]:
        if not is_solution_in_pop(s, solutions, as_tree=True):
            solutions.append(s)

    return solutions
