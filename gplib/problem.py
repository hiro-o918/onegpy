from abc import ABC, abstractmethod

from gplib.solutions.solution import Solution


class AbstractProblem(ABC):

    def __init__(self, function_bank_builder=None):
        if function_bank_builder is not None:
            self._function_bank_builder = function_bank_builder

        self.func_bank = self._function_bank_builder()
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

    @abstractmethod
    def _cal_fitness(self, target_solution):
        raise NotImplementedError("_cal_fitness should be implemented in {}".format(self.__class__))

    def get_eval_count(self):
        return self._eval_cnt

    @abstractmethod
    def _function_bank_builder(self):
        raise NotImplementedError('default_function_bank_builder should be implemented in {}'.format(self.__class__))


class FunctionBank(object):

    def __init__(self):
        self.function_list = []
        self.children_dict = {}

    def add_function(self, func):
        n_children = func.n_children
        func_id = len(self.function_list)
        self.function_list.append(func)

        if not n_children in self.children_dict:
            self.children_dict[n_children] = []
        self.children_dict[n_children].append(func_id)

    def get_function_list(self, n_children=None):
        if n_children is None:
            return self.function_list
        if not n_children in self.children_dict:
            return None
        else:
            return self.children_dict[n_children]