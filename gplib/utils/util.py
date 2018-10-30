def get_generator_builder(selection):
    """
    Get a generator builder.
    The generator generates list of solutions by means of `selection`.
    :param selection: inheritance of class AbstractSelection.
    :return: generator_builder
    """
    def generator_builder(population):
        while True:
            yield selection(population)

    return generator_builder


def get_fitness_info(population):
    sorted_pop = sorted(population, key=lambda x: x.previous_fitness, reverse=True)
    max_fit = sorted_pop[0].previous_fitness
    min_fit = sorted_pop[-1].previous_fitness

    sum = 0.0
    for solution in sorted_pop:
        sum += solution.previous_fitness

    ave_fit = sum / float(len(population))

    info = {'max_fit': max_fit, 'ave_fit': ave_fit, 'min_fit': min_fit}

    return info




