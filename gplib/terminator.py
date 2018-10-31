from abc import ABC


class AbstractTerminator(ABC):
    def __call__(self):
        return True


class GenerationTerminator(AbstractTerminator):
    def __init__(self, t_gene):
        self.t_gene = t_gene
        self.gene = 0

    def __call__(self):
        self.gene += 1
        return self.gene > self.t_gene


class ProblemBasedTerminator(AbstractTerminator):
    def __init__(self, problem):
        self.problem = problem


class EvalCountTerminator(ProblemBasedTerminator):
    def __init__(self, problem, t_eval_cnt):
        ProblemBasedTerminator.__init__(self, problem)
        self.t_eval_cnt = t_eval_cnt

    def __call__(self):
        return self.t_eval_cnt <= self.problem.get_eval_count()


class FitnessTerminator(ProblemBasedTerminator):
    def __init__(self, problem, t_fitness):
        ProblemBasedTerminator.__init__(self, problem)
        self.t_fitness = t_fitness

    def __call__(self):
        return self.t_fitness <= self.problem.get_elite_fitness


def terminator_checker(terminator):
    if not isinstance(terminator, AbstractTerminator):
        typ = TypeError
        msg = 'Expected type: {} not {}.'.format(AbstractTerminator, type(terminator))
    else:
        return

    raise typ(msg)
