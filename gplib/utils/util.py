def get_generator_builder(selection):
    """
    Get a generator builder.
    The generator generates list of solutions by means of `selection`.
    :param selection: inheritance of class AbstractSelection.
    :param population: list of solutions.
    :return:
    """
    def generator_builder(population):
        while True:
            yield selection(population)

    return generator_builder


