from abc import ABC


class AbstractTerminator(ABC):
    """
    Base of Terminator class
    """
    def __call__(self):
        return True


class GenerationTerminator(AbstractTerminator):
    def __init__(self, t_gene):
        """
        A terminator based on the number of generation.

        :param t_gene: int. a target generation count.
        """
        self.t_gene = t_gene
        self.gene = 0

    def __call__(self):
        """
        Returns `True`, if the number of generation is greater than `self.t_gene`

        :return : bool.
        """
        self.gene += 1
        return self.gene > self.t_gene


class ProblemBasedTerminator(AbstractTerminator):
    def __init__(self, problem):
        """
        Base of Terminator class based on problem.

        :param problem: Problem.
        """
        self.problem = problem


class EvalCountTerminator(ProblemBasedTerminator):
    def __init__(self, problem, t_eval_cnt):
        """
        A terminator based on the number of evaluation.

        :param problem: Problem.
        :param t_eval_cnt: int. a target evaluation count.
        """
        ProblemBasedTerminator.__init__(self, problem)
        self.t_eval_cnt = t_eval_cnt

    def __call__(self):
        """
        Returns `True` if the number of evaluation is greater than or equals to `self.t_eval_count`.

        :return : bool.
        """
        return self.t_eval_cnt <= self.problem.get_eval_count()


class FitnessTerminator(ProblemBasedTerminator):
    def __init__(self, problem, t_fitness):
        """
        A terminator based on the value of fitness.

        :param problem: Problem.
        :param t_fitness: float. a target value of fitness.
        """
        ProblemBasedTerminator.__init__(self, problem)
        self.t_fitness = t_fitness

    def __call__(self):
        """
        Returns `True` if the value of fitness is greater than or equals to `self.t_fitness`

        :return : bool.
        """
        return self.t_fitness <= self.problem.get_elite_fitness


def terminator_checker(terminator):
    if not isinstance(terminator, AbstractTerminator):
        typ = TypeError
        msg = 'Expected type: {} not {}.'.format(AbstractTerminator, type(terminator))
    else:
        return

    raise typ(msg)
