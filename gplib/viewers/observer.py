from abc import ABC, abstractmethod

from gplib.utils import util
from gplib.viewers.loggers import JSONLogger, PrintLogger


def generate_sgp_log(gene, population):
    general_log = {'generation': gene, 'pop_num': len(population)}
    fit_log = util.get_fitness_info(population)
    log = {**general_log, **fit_log}

    return log


def generate_mlpsgp_log(iter_cnt, eval_cnt, population_list):
    detailed_log = []
    for i, sub_pop in enumerate(population_list):
        general_log = {'iter_cnt': iter_cnt, 'eval_cnt': eval_cnt, 'level': i + 1}
        fitness_log = util.get_fitness_info(sub_pop)
        detailed_log.append({**general_log, **fitness_log})

    fitness_list_mapper = {'min': 0, 'ave': 1, 'max': 2}
    fitness_list = np.array(list(map(lambda x:
                                     [x['min_fit'], x['ave_fit'], x['max_fit']],
                                     detailed_log)))

    summary_log = {'iter_count': iter_cnt,
                   'eval_cnt': eval_cnt,
                   'min': min(fitness_list[:, fitness_list_mapper['min']]),
                   'ave': np.average(fitness_list[:, fitness_list_mapper['ave']]),
                   'max': max(fitness_list[:, fitness_list_mapper['max']]),
                   'n_level': len(population_list)}

    return {'detail': detailed_log, 'summary': summary_log}


class AbstractObserver(ABC):
    def __init__(self):
        self._loggers = []

    @abstractmethod
    def set_loggers(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def begin(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def end(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def update(self, *args, **kwargs):
        raise NotImplementedError


class DefaultObserver(AbstractObserver):
    def __init__(self, verbose=3, **kwargs):
        """
        Observer for SGP.

            :param verbose: int.
            0 -> No log,
            1 -> print a log.
            2 -> save a log.
            3 -> print and sve a log
            :param out: String.output output to print.
            :param filepath: filepath: str or Path. Path to dump json.
            :param save_every_updating: bool. if true, save history every updating.
             otherwise save only in the end.
        """
        super(DefaultObserver, self).__init__()
        self.set_loggers(verbose, **kwargs)
        self.history = []

    def set_loggers(self, verbose, **kwargs):
        if verbose & 0b01:
            self._loggers.append(PrintLogger(**kwargs))
        if verbose & 0b10:
            self._loggers.append(JSONLogger(**kwargs))

    def begin(self):
        [l.begin() for l in self._loggers]

    def end(self, population):
        log = {'max_fit': util.get_fitness_info(population).get('max_fit')}
        [l.end(log=log, history=self.history) for l in self._loggers]

    def update(self, gene, population):
        general_log = {'generation': gene, 'pop_num': len(population)}
        fit_log = util.get_fitness_info(population)
        log = {**general_log, **fit_log}
        self.history.append(log)

        [l.update(log=log, history=self.history) for l in self._loggers]

