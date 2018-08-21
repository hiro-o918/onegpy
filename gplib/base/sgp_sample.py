from gplib.operator import crossover, selection, initializer
from gplib.problems import boolean
from gplib.base import gpbase

def build_SGP():
    dim = 3
    n_generations = 20

    problem = boolean.EvenParity(dim=dim)

    cross = crossover.get_default_crossover()
    selec = selection.TournamentSelection(tournament_size=5, problem=problem)

    operators = [cross, selec]

    func_dicts = boolean.get_default_node_set(dim=dim)

    problem.func_dicts = func_dicts

    gp = gpbase.GP(operators, problem, func_dicts=func_dicts, n_generations=n_generations)

    return gp


if __name__ == '__main__':
    popsize = 500

    t_prob = 0.1
    max_depth = 10
    function_dict = None

    gp = build_SGP()
    population = []

    for _ in range(popsize):
        population.append(initializer.initialize(t_prob=t_prob, max_depth=max_depth, function_dicts=gp.func_dicts))

    gp(population)