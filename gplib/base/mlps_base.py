from gplib.operators.mlps_crossover import MLPS_Crossover
from gplib.utils import util
from gplib.solutions import node, solution
import numpy as np
from gplib.problems import boolean
from gplib.operators import initializer


class MLPS_GP(object):

    def __init__(self, initializer, localsearch, problem, max_evals, t_prob, max_depth, simplify=None,
                 is_add_terminal=True, only_add_best=False, only_add_improvements=False, depth_limit=1000000):
        """

        :param initializer: function. Initialize operator of MLPS-GP.
        :param localsearch: local search object. Local search operator of MLPS_GP.
        :param problem: Problem object. problem to solve.
        :param max_evals: int. the number of maximum evaluations for the terminal condition.
        :param t_prob: float. terminal probability for initialization.
        :param max_depth: int. a limit depth of a tree for initialization.
        :param simplify: simplify object. Simplify operator of MLPS-GP. Default is None.
        :param is_add_terminal: bool. a control parameter of MLPS-GP. Default is True.
        :param only_add_best: bool. a control parameter of MLPS-GP. Default is False.
        :param only_add_improvements: bool. a control parameter of MLPS-GP. Default is False.
        :param depth_limit: int. a limit depth of a tree during search. Default is 1000000.
        """
        self.initializer = initializer
        self.localsearch = localsearch
        self.crossover = MLPS_Crossover(problem)
        self.problem = problem
        self.max_evals = max_evals
        self.simplify = simplify
        self.is_add_terminal = is_add_terminal
        self.only_add_best = only_add_best
        self.only_add_improvements = only_add_improvements
        self.depth_limit = depth_limit
        self.population_list = []
        self.t_prob = t_prob
        self.max_depth = max_depth
        self.func_bank = problem.func_bank

    def __call__(self):
        cnt = 0
        if self.is_add_terminal:
            ##TODO: implement terminal initializer
            pass

        while self.problem.get_eval_count() < self.max_evals:
            self.mlps_iterate()
            cnt += 1
            max_fit = []
            ave = []
            for i, sub_pop in enumerate(self.population_list):
                if len(sub_pop) == 0:
                    continue
                fitness_info = util.get_fitness_info(sub_pop)
                ave.append(fitness_info['ave_fit'])
                max_fit.append(fitness_info['max_fit'])
            print('{}, max:{}, ave:{}'.format(cnt, max(max_fit), np.average(ave)))
            if max(max_fit) == 1.0:
                break

    def mlps_iterate(self):
        ## initialization
        candidate_solution = self.initialize_solution()

        ## get terminal node positions
        terminal_points = node.get_all_terminal_points(candidate_solution.root)

        ##crossover
        self.do_crossover(candidate_solution, terminal_points)

    def get_skip_pop(self, level):
        size = len(self.population_list)
        for i in range(size, level+1):
            self.population_list.append([])

        return self.population_list[level]

    def initialize_solution(self):
        candidate_solution = self.initializer(self.t_prob, self.max_depth, self.func_bank)
        problem.fitness(candidate_solution)

        if self.localsearch is not None:
            self.localsearch(candidate_solution)

        solution.set_solution_depth(candidate_solution)
        self.add_indiv(candidate_solution, True, candidate_solution.depth)

        return candidate_solution

    def do_crossover(self, candidate_solution, terminal_points):
        solution.set_solution_depth(candidate_solution)
        ## TODO: if you use a subtree node, you should calculate depth again here.
        for i, donors in enumerate(self.population_list):
            if candidate_solution.depth < i:
                break

            ## TODO: check the total number of fitness evaluations. if it is over the limitation, close this loop

            if len(donors) > 0:
                previous_fitness = candidate_solution.previous_fitness
                self.crossover(recipient=candidate_solution, cross_points=terminal_points, donors=donors)
                solution.set_solution_depth(candidate_solution)
                ## TODO: if you use a subtree node, you should calculate depth again here.

                if (not self.only_add_improvements) or (previous_fitness < candidate_solution.previous_fitness):
                    self.add_indiv(candidate_solution, False, candidate_solution.depth)

            #TODO: if you want to use only continue improvements or use not continue only one, implement here!

    def add_indiv(self, candidate, is_init, depth):
        is_containts = False
        is_best = True

        if self.depth_limit < depth:
            return False

        candidate_copy = solution.copy_solution(candidate, deep=True)

        if self.simplify is not None and is_init:
            self.simplify.simple(candidate_copy)

        ##TODO: if dummy node is introduced, we must check the number of nodes here.

        if (len(self.population_list) > depth):
            sub_population = self.population_list[depth]
            for indiv in sub_population:
                ##TODO: if you want to donate this rapidly, you can use comparison based on the number of node
                if solution.solution_equal(indiv, candidate_copy):
                    is_containts = True
                    break

        ## check if the candidate has the best solution in subset of solutions which is not deeper than the candidate.
        if self.only_add_best and (not is_init):
            under_depth = min(len(self.population_list), depth)
            for i in range(under_depth):
                max_fit = util.get_fitness_info(self.population_list[i])['max_fit']
                if max_fit >= candidate.previous_fitness:
                    is_best = False

        if (not is_containts) and is_best:
            level = depth
            sub_population = self.get_skip_pop(level)

            ##TODO: if you want to use only_add_original_fit or remove_equals, implement it here

            ##TODO: if you use subtree node, create a new root using subtree node here(also, update elite).
            sub_population.append(candidate_copy)

            sub_population.sort(key=lambda x: x.previous_fitness, reverse=True)
            return True

        return False


if __name__ == '__main__':

    t_prob = 0.1
    max_depth = 3
    dim = 6
    max_evals = 100000

    init_op = initializer.initialize
    ls_op = None

    problem = boolean.EvenParity(dim=dim)

    population = []
    mlps = MLPS_GP(initializer= init_op, localsearch=ls_op, problem=problem, max_evals=max_evals, t_prob=t_prob,
                   max_depth=max_depth, is_add_terminal=False)

    mlps()
