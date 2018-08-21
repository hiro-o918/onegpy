from gplib.base import gpbase
from gplib.operators import crossover, selection, initializer
from gplib.problems import boolean
from gplib.utils import util

def build_SGP(problem):
    n_generations = 20

    cross = crossover.PopulationOnePointCrossover(c_rate=1.0)
    select = selection.TournamentSelection(tournament_size=5, problem=problem)

    def run_sgp(population):
        for i in range(n_generations):
            population = select(cross(population))
            eval_cnt = problem.get_eval_count()
            info = util.get_fitness_info(population)
            print(eval_cnt, info)
            if info['max_fit'] >= 1.0:
                break

    return run_sgp


if __name__ == '__main__':
    popsize = 500

    t_prob = 0.1
    max_depth = 10
    dim = 3

    problem = boolean.EvenParity(dim=dim)
    func_dicts = boolean.get_default_node_set(dim=dim)
    problem.func_dicts = func_dicts

    sgp = build_SGP(problem)
    population = []

    for _ in range(popsize):
        population.append(initializer.initialize(t_prob=t_prob, max_depth=max_depth, function_dicts=problem.func_dicts))

    sgp(population)
