from gplib.solutions.solution import Solution


class AbstractProblem(object):

    def __init__(self):
        self.func_dicts = None
        self._eval_cnt = 0

    def fitness(self, target_solution_or_solutions):
        if isinstance(target_solution_or_solutions, Solution):
            fitness = self._cal_fitness(target_solution=target_solution_or_solutions)
            self._eval_cnt += 1
            target_solution_or_solutions.previous_fitness = fitness
            return fitness
        elif isinstance(target_solution_or_solutions, list):
            fitness_list = []
            for s in target_solution_or_solutions:
                fitness = self._cal_fitness(target_solution=s)
                s.previous_fitness = fitness
                fitness_list.append(fitness_list)
            self._eval_cnt += len(target_solution_or_solutions)
            return fitness_list
        else:
            raise TypeError("target_solution_or_solutions should be Solution object or list of Solution objects.")


    def _cal_fitness(self, target_solution):
        raise NotImplementedError("_cal_fitness should be implemented in {}".format(self.__class__))

    def get_eval_count(self):
        return self._eval_cnt

