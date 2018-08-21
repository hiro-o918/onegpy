# -*- coding: utf-8 -*-
import random
import warnings


class AbstractOperator(object):
    """
        This is the base class for operators.
    """
    def __init__(self, n_in=None, n_out=None):
        """
        The number of input solution to the operator and outputs one of the operator
        `None` means that the operator handles variable length solutions.
        :param n_in: int or None
        :param n_out: int or None
        """
        self._n_in = n_in
        self._n_out = n_out

    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def not_changeable_warning():
        msg = 'This variable is not changeable.' \
              ' Thus, the operation has no effect.'
        warnings.warn(msg)

    @property
    def n_in(self):
        return self._n_in

    @n_in.setter
    def n_in(self, _):
        self.not_changeable_warning()

    @n_in.deleter
    def n_in(self):
        self.not_changeable_warning()

    @property
    def n_out(self):
        return self._n_out

    @n_out.setter
    def n_out(self, _):
        self.not_changeable_warning()

    @n_out.deleter
    def n_out(self):
        self.not_changeable_warning()


class AbstractPopulationOperator(AbstractOperator):
    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class PopulationOperator(AbstractPopulationOperator):
    def __init__(self, operator, generator_builder=None, n_out=None):
        super(PopulationOperator, self).__init__()
        check_operator(operator)
        self.operator = operator
        self.generator_builder = generator_builder or self._build_default_generator
        self.n_out = n_out

    def __call__(self, population, *args, **kwargs):
        new_pop = []
        generator = self.generator_builder(population)

        for solutions in generator:
            new_solutions = self.operator(solutions)
            if isinstance(new_solutions, (list, tuple)):
                new_pop.extend(new_solutions)
            else:
                new_pop.append(new_solutions)

            if len(new_pop) >= (self.n_out or len(population)):
                break

        return new_pop

    def _build_default_generator(self, population):
        random.shuffle(population)
        n_solutions = self.operator.n_in

        def generator():
            for i in range(0, len(population), n_solutions):
                yield population[i:i + n_solutions]

        return generator()


def build_population_operator(operator, selection_class=None, n_out=None, **kwargs):
    check_operator(operator)

    if selection_class is not None:
        build_generator = selection_class(k=operator.n_input, **kwargs).build_generator
    else:
        build_generator = None

    return PopulationOperator(operator, build_generator, n_out)


def check_operator(operator):
    if not isinstance(operator, AbstractOperator):
        typ = TypeError
        msg = 'Expected type: {} not {}.'.format(AbstractOperator, type(operator))
    else:
        return

    raise typ(msg)
