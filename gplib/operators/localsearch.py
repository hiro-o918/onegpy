from abc import ABC
from functools import partial
import random

from gplib.solutions import node, solution
from gplib.operator import AbstractOperator, ProblemBasedOperator


class AbstractLocalSearch(AbstractOperator, ProblemBasedOperator, ABC):
    def __init__(self, problem, target_node, localsearch_type):
        """
        Abstract class of localsearch.

        :param problem: problem
        :param target_node: String. type of target nodes
        :param localsearch_type: String, function name
        """
        AbstractOperator.__init__(self, n_in=1, n_out=1)
        ProblemBasedOperator.__init__(self, problem)
        self._target_node = target_node
        self._localsearch_type = localsearch_type

    def get_target_node(self, root):
        if self.target_node == 'nonterminal':
            return node.get_all_nonterminal_node(root)
        elif self.target_node == 'terminal':
            return node.get_all_nonterminal_node(root)
        elif self.target_node == 'all':
            return node.get_all_node(root)
        else:
            msg = '{} is not found'.format(self.target_node)
            raise ValueError(msg)

    @property
    def func_bank(self):
        return self.problem.func_bank

    @func_bank.setter
    def func_bank(self, _):
        self.not_changeable_warning()

    @func_bank.deleter
    def func_bank(self):
        self.not_changeable_warning()

    @property
    def target_node(self):
        return self._target_node

    @target_node.setter
    def target_node(self, _):
        self.not_changeable_warning()

    @target_node.deleter
    def target_node(self):
        self.not_changeable_warning()

    @property
    def localsearch_type(self):
        return self._localsearch_type

    @localsearch_type.setter
    def localsearch_type(self, _):
        self.not_changeable_warning()

    @localsearch_type.deleter
    def localsearch_type(self):
        self.not_changeable_warning()


def improve(target_solution, target_node, candidate_id, problem):
    pre_id = target_node.func_id
    node.set_id(target_node, candidate_id)
    if target_solution.previous_fitness is None:
        pre_fit = problem.fitness(target_solution)
    else:
        pre_fit = target_solution.previous_fitness
    new_fit = problem.fitness(target_solution)
    if pre_fit >= new_fit:
        node.set_id(target_node, pre_id)
        solution.set_previous_fitness(target_solution, pre_fit)
        return False
    else:
        return True


def all_check(target_solution, target_node, problem):
    func_bank = problem.func_bank
    n_children = len(target_node.children)
    function_list = func_bank.get_function_list(n_children)

    improved = False
    for candidate_id in function_list:
        if target_node.func_id != candidate_id:
            improved |= improve(target_solution, target_node, candidate_id, problem)

    return improved


def stop_improvement(target_solution, target_node, problem, is_shuffle=True):
    func_bank = problem.func_bank
    n_children = len(target_node.children)
    function_list = func_bank.get_function_list(n_children)

    if is_shuffle:
        random.shuffle(function_list)

    for candidate_id in function_list:
        if target_node.func_id != candidate_id:
            improved = improve(target_solution, target_node, candidate_id, problem)
            if improved:
                return improved
    return False


def fihc(target_solution, node_list, ls_core):
    searched = []
    random.shuffle(node_list)
    while len(node_list) > 0:
        target_node = node_list.pop()
        improved = ls_core(target_solution, target_node)
        if improved:
            node_list.extend(searched)
            searched.clear()
            random.shuffle(node_list)
        searched.append(target_node)

    return target_solution


def bihc(target_solution, node_list, ls_core):
    pre_node = None
    while len(node_list) > 0:
        ori_fit = target_solution.previous_fitness
        best_fit = target_solution.previous_fitness
        best_node = None
        best_id = None
        for target_node in node_list:
            ori_id = target_node.func_id
            ls_core(target_solution, target_node)
            if best_fit < target_solution.previous_fitness:
                best_node = target_node
                best_id = target_node.func_id
            node.set_id(target_node, ori_id)
            solution.set_previous_fitness(target_solution, ori_fit)
        if best_node is not None:
            node.set_id(best_node, best_id)
            solution.set_previous_fitness(target_solution, best_fit)

            if pre_node is not None:
                node_list.append(pre_node)
            node_list.remove(best_node)
            pre_node = best_node
        else:
            return target_solution
    return target_solution


def get_localsearch_core(localsearch_type, **kwargs):
    if localsearch_type == 'all_check':
        # Obtain `one_point` function fixed `func_bank`
        localsearch_core = partial(all_check, **kwargs)
    elif localsearch_type == 'stop_improvement':
        localsearch_core = partial(stop_improvement, **kwargs)
    else:
        msg = '{} is not found'.format(localsearch_type)
        raise ValueError(msg)

    return localsearch_core


class FIHC(AbstractLocalSearch):
    def __init__(self, problem, target_node='nonterminal', localsearch_type='all_check'):
        super(FIHC, self).__init__(problem, target_node, localsearch_type)
        self.localsearch_core = get_localsearch_core(self._localsearch_type, problem=problem)

    def __call__(self, target_solution):
        """
        First Improvement Hill Climber
        :param target_solution: solution object. target solution of FIHC
        :return: solution object.
        """

        target_nodes = self.get_target_node(target_solution.root)
        return fihc(target_solution, target_nodes, self.localsearch_core)
