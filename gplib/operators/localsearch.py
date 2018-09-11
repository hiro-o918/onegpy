from abc import ABC
from functools import partial
import random

from gplib.solutions import node, solution
from gplib.operator import AbstractOperator, ProblemBasedOperator


class AbstractLocalSearch(AbstractOperator, ProblemBasedOperator, ABC):
    def __init__(self, problem, target_node, func_search_type):
        """
        Abstract class of localsearch.

        :param problem: problem
        :param target_node: String. type of target nodes
        :param func_search_type: String, function name
        """
        AbstractOperator.__init__(self, n_in=1, n_out=1)
        ProblemBasedOperator.__init__(self, problem)
        self._target_node = target_node
        self._func_search_type = func_search_type

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
    def func_search_type(self):
        return self._func_search_type

    @func_search_type.setter
    def func_search_type(self, _):
        self.not_changeable_warning()

    @func_search_type.deleter
    def func_search_type(self):
        self.not_changeable_warning()


def improve(target_solution, target_node, candidate_id, problem):
    """
    core function for local search.
    replace the old function with a new function and then revert it if fitness is not improved.
    :param target_solution: solution object. target solution of local search.
    :param target_node: node object. target node of the target solution.
    :param candidate_id: int. ID of candidate function for local search.
    :param problem: problem object. problem for calculation of fitness.
    :return: bool. if improvement is success, return True.
    """
    pre_id = target_node.func_id
    node.set_id(target_node, candidate_id)
    if target_solution.previous_fitness is None:  # if the solution does not have previous fitness, calculate it.
        pre_fit = problem.fitness(target_solution)
    else:
        pre_fit = target_solution.previous_fitness
    new_fit = problem.fitness(target_solution)  # check the fitness.
    if pre_fit >= new_fit:  # if it is not success, revert the function.
        node.set_id(target_node, pre_id)
        solution.set_previous_fitness(target_solution, pre_fit)
        return False
    else:
        return True


def all_check(target_solution, target_node, problem):
    """
    search function for a target node.
    try to replace a current function with all candidate function and replace best improving function.
    :param target_solution: solution object. target solution of local search.
    :param target_node: node object. target node of the target solution.
    :param problem: problem object. problem for calculation of fitness.
    :return: bool. if improvement is success, return True.
    """
    func_bank = problem.func_bank
    n_children = len(target_node.children)
    function_list = func_bank.get_function_list(n_children)

    improved = False
    for candidate_id in function_list:
        if target_node.func_id != candidate_id:  # if the current function equals to the candidate one, skip checking
            improved |= improve(target_solution, target_node, candidate_id, problem)

    return improved


def stop_improvement(target_solution, target_node, problem, is_shuffle=True):
    """
    search function for a target node.
    try to replace a current function with candidate functions and replace first improving function.
    :param target_solution: solution object. target solution of local search.
    :param target_node: node object. target node of the target solution.
    :param problem: problem object. problem for calculation of fitness.
    :param is_shuffle: bool. if candidate functions are shuffled or not. default is True
    :return: bool. if improvement is success, return True.
    """
    func_bank = problem.func_bank
    n_children = len(target_node.children)
    function_list = func_bank.get_function_list(n_children)

    if is_shuffle:
        random.shuffle(function_list)

    for candidate_id in function_list:
        if target_node.func_id != candidate_id:  # if the current function equals to the candidate one, skip checking
            improved = improve(target_solution, target_node, candidate_id, problem)
            if improved:
                return improved
    return False


def fihc(target_solution, node_list, fs_core):
    """
    First improvement hill climber (FIHC) function.
    :param target_solution: solution object. target solution of local search.
    :param node_list: list of node object. candidate node list.
    :param fs_core: function. search function for a target node.
    :return: solution object.
    """
    searched = []
    random.shuffle(node_list)
    while node_list:
        target_node = node_list.pop()
        improved = fs_core(target_solution, target_node)
        if improved:  # if the solution is improved, nodes in searched list are added candidate list again.
            node_list.extend(searched)
            searched.clear()
            random.shuffle(node_list)
        searched.append(target_node)

    return target_solution


def bihc(target_solution, node_list, fs_core):
    """
    Best improvement hill climber (BIHC) function.
    :param node_list: list of node object. candidate node list.
    :param fs_core: function. search function for a target node.
    :return: solution object.
    """
    pre_node = None
    while node_list:
        ori_fit = target_solution.previous_fitness
        best_fit = target_solution.previous_fitness
        best_node = None
        best_id = None
        for target_node in node_list:  # Try to find the best-improving target node and the function id.
            ori_id = target_node.func_id
            fs_core(target_solution, target_node)
            if best_fit < target_solution.previous_fitness:
                best_node = target_node
                best_id = target_node.func_id
            # the target solution is reverted to the original for the next iteration.
            node.set_id(target_node, ori_id)
            solution.set_previous_fitness(target_solution, ori_fit)
        # If there is no improvement, end this local search.
        if best_node is None:
            break

        # Otherwise, adopt the improvement to the solution.
        node.set_id(best_node, best_id)
        solution.set_previous_fitness(target_solution, best_fit)

        if pre_node is not None:
            node_list.append(pre_node)
        node_list.remove(best_node)  # remove the replaced node from candidate node list
        pre_node = best_node

    return target_solution


def get_func_search_core(func_search_type, **kwargs):
    """
    getter of function search function.
    :param func_search_type: String. name of function of func search.
    :param kwargs:
    :return: function. funcsearch_core
    """
    if func_search_type == 'all_check':
        # Obtain `one_point` function fixed `func_bank`
        func_search_core = partial(all_check, **kwargs)
    elif func_search_type == 'stop_improvement':
        func_search_core = partial(stop_improvement, **kwargs)
    else:
        msg = '{} is not found'.format(func_search_type)
        raise ValueError(msg)

    return func_search_core


class FIHC(AbstractLocalSearch):

    def __init__(self, problem, target_node='nonterminal', func_search_type='all_check'):
        """
        FIHC class.
        :param problem: problem object. problem for calculation of fitness.
        :param target_node: String. target node type (eg. nonterminal, terminal)
        :param func_search_type: String. String. name of function of function search.
        """
        super(FIHC, self).__init__(problem, target_node, func_search_type)
        self.func_search_core = get_func_search_core(self.func_search_type, problem=problem)

    def __call__(self, target_solution):
        """
        First Improvement Hill Climber
        :param target_solution: solution object. target solution of FIHC
        :return: solution object.
        """

        target_nodes = self.get_target_node(target_solution.root)
        return fihc(target_solution, target_nodes, self.func_search_core)


class BIHC(AbstractLocalSearch):

    def __init__(self, problem, target_node='nonterminal'):
        """
        BIHC class.
        :param problem: problem object. problem for calculation of fitness.
        :param target_node: String. target node type (eg. nonterminal, terminal)
        :param func_search_type: String. String. name of function of function search.
        """
        super(BIHC, self).__init__(problem, target_node, func_search_type='all_check')
        self.func_search_core = get_func_search_core(self.func_search_type, problem=problem)

    def __call__(self, target_solution):
        """
        Best Improvement Hill Climber
        :param target_solution: solution object. target solution of BIHC
        :return: solution object.
        """

        target_nodes = self.get_target_node(target_solution.root)
        return bihc(target_solution, target_nodes, self.func_search_core)
