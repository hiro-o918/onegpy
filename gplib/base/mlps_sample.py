from gplib.base.mlps_base import MLPS_GP
from gplib.operators.initializer import RandomInitializer
from gplib.operators.localsearch import FIHC
from gplib.problems import boolean


if __name__ == '__main__':

    t_prob = 0.2
    max_depth = 3
    dim = 4
    max_evals = 100000

    problem = boolean.EvenParity(dim=dim)

    init_op = RandomInitializer(t_prob, max_depth, problem)
    ls_op = FIHC(problem, target_node='nonterminal', func_search_type='all_check')
    #ls_op = None

    population = []
    mlps = MLPS_GP(initializer= init_op, localsearch=ls_op, problem=problem, max_evals=max_evals, t_prob=t_prob,
                   max_depth=max_depth, is_add_terminal=False)

    mlps()