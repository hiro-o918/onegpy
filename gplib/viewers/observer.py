from abc import ABC, abstractmethod

from gplib.utils import util
from gplib.viewers.loggers import JSONLogger, PrintLogger


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
    def __init__(self, verbose, **kwargs):
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

