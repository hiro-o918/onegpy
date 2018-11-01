# -*- coding: utf-8 -*-
import random
import types
import warnings
from abc import ABC, abstractmethod

from gplib.utils.util import get_generator_builder


class AbstractOperator(ABC):
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

    @abstractmethod
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


class PopulationOperator(AbstractOperator, ABC):
    """
    This is a base class a population operator.
    Population operator aims at population or a list of solutions.
    """
    pass


class PopulationOperatorAdapter(PopulationOperator):
    """
    This is an adapter to make an operator aim at population.
    """

    def __init__(self, operator, generator_builder=None, n_out=None):
        """
        :param operator: operator object. operator object to apply.
        :param generator_builder: function of generator builder. Default is None (default generator).
        This function makes a generator from input population.
        :param n_out: int. the number of output.
        """
        super(PopulationOperatorAdapter, self).__init__(n_out=n_out)
        operator_checker(operator)
        if operator.n_in is None:
            msg = 'n_in of {} must be set'.format(operator.__name__)
            raise ValueError(msg)

        if operator.n_in != operator.n_out and n_out is None:
            msg = 'The number of population will change by this operator'
            warnings.warn(msg)

        self.operator = operator
        self._register_metaclass()
        self.generator_builder = generator_builder or self._get_default_generator_builder()

    def __call__(self, population, *args, **kwargs):
        """
        Apply an operator of this instance to population.
        A candidate is selected by generator.

        :param population: list of solutions. population.
        :param args:
        :param kwargs:
        :return:
        """
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

    def _get_default_generator_builder(self):

        n_solutions = self.operator.n_in

        def generator_builder(population):
            random.shuffle(population)
            for i in range(0, len(population), n_solutions):
                yield population[i:i + n_solutions]

        return generator_builder

    def _register_metaclass(self):
            self.operator.__class__.register(self.__class__)


class ProblemBasedOperator(ABC):
    """
    This is a base class a operator based on population,
    that is, it requires a problem instance.
    """
    def __init__(self, problem):
        """
        :param problem: problem object. The target problem.
        """
        self.problem = problem


def build_population_operator(operator, selection_class=None, n_out=None, cls_name=None, **kwargs):
    """
    Builder function for population operator.

    :param operator: operator object. The target operator to build.
    :param selection_class: selection class. **NOTE** not instance.
    a generator is built by using a logic of the selection class.
    :param n_out: int. the number of output of the target operator.
    :param cls_name: str. a name of a new class build by this function.
    :param kwargs:
    :return:
    """
    operator_checker(operator)

    if selection_class is not None:
        generator_builder = get_generator_builder(selection_class(k=operator.n_input, **kwargs))
    else:
        generator_builder = None

    po_cls = types.new_class(cls_name or 'Population{}'.format(operator.__class__.__name__),
                             bases=(PopulationOperatorAdapter,))

    return po_cls(operator, generator_builder, n_out)


def operator_checker(operator):
    """
    checker for operator.
    """
    if not isinstance(operator, AbstractOperator):
        typ = TypeError
        msg = 'Expected type: {} not {}.'.format(AbstractOperator, type(operator))
    else:
        return

    raise typ(msg)


def pop_operator_checker(operator):
    """
    checker for population operator.
    """
    if not isinstance(operator, PopulationOperator):
        typ = TypeError
        msg = 'Expected type: {} not {}.'.format(PopulationOperator, type(operator))
    else:
        return

    raise typ(msg)
