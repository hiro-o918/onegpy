import random


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

    def __init__(self, tournament_size, problem, replacement=True):
        self.tournament_size = tournament_size
        if replacement:
            def append(solution, chosen):
                chosen.append(solution)
        else:
            def append(solution, chosen):
                if solution not in chosen:
                    chosen.append(solution)

        self.append = append
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

        k = len(population)

        #TODO: we must check the original population size > k (it is also super redundant if k is almost equal to population size), if replacement=False.
        while(len(chosen) < k):
            candidates = self.rand_f(population=population, k=self.tournament_size)
            best = max(candidates, key=lambda x: x.previous_fitness)
            self.append(best, chosen)

        del population

        return chosen

