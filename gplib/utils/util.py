def build_generator(selection, population):
    """
    Build a generator selecting from fixed population by means of `selection`.
    :param selection: inheritance of class AbstractSelection.
    :param population: list of solutions.
    :return:
    """
    def generator():
        while True:
            yield selection(population)

    return generator()


