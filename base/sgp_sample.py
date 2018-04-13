from operator import crossover, selection, initializer
from problem import boolean
from base import gpbase

def build_SGP():
    dim = 3

    cross = crossover.OnePointCrossover()
    selec = selection.TournamentSelection(tournament_size=2)

    operators = [cross, selec]

    prob = boolean.EvenParity(dim = dim)

    func_dict = boolean.get_default_node_set(dim=dim)

    gp = gpbase.GP(operators, prob, func_dict=func_dict)

    return gp


if __name__ == '__main__':
    popsize = 20

    t_prob = 0.9
    max_depth= 5
    n_terminal = 0
    n_nonterminal = 0
    function_dict = None

    for _ in range(popsize):
        initializer.initialize()