import datetime
import json
from abc import ABC, abstractmethod
import sys
from pathlib import Path

from gplib.utils import util


class AbstractLogger(ABC):
    def __init__(self, verbose=1, out=sys.stdout, filepath=Path('log')):
        """
            Class of logger.

            :param verbose: int.
            0 -> No log,
            1 -> print a log and save it in the end,
            2 -> print a log and save it every updating.
            :param out: String.output
            :param filepath: Path
        """

        verbose_list = [0, 1, 2]
        if verbose not in verbose_list:
            msg = 'verbose must be selected from {}'.format(verbose_list)
            raise ValueError(msg)

        self._out = out
        self._verbose = verbose
        self._filename = Path(filepath)
        self.log = []

    def get_out(self, info):
        if self._verbose > 0:
            if isinstance(info, dict):
                info = ', '.join(['{}: {}'.format(k, v) for k, v in info.items()])

            print(info, file=self._out)

    def update_log(self, info):
        self.log.append(info)
        if self._verbose > 1:
            with open(self._filename, 'w') as f:
                json.dump(self.log, f, indent=4)

    @abstractmethod
    def begin(self):
        raise NotImplementedError

    @abstractmethod
    def end(self, population):
        raise NotImplementedError

    @abstractmethod
    def update(self, gene, population):
        raise NotImplementedError


class DefaultLogger(AbstractLogger):
    def __init__(self, verbose=1, out=sys.stdout, filepath=Path('log')):
        """
            Default Logger

            :param verbose: int.
            0 -> No log,
            1 -> print a log and save it in the end,
            2 -> print a log and save it every updating.
            :param out: String.output
            :param filepath: Path
        """
        super(DefaultLogger, self).__init__(verbose, out, filepath)

    def begin(self):
        self.get_out(datetime.datetime.today())
        self.get_out("-----------begin-----------")

    def end(self, population):
        self.get_out("------------end------------")
        self.get_out(datetime.datetime.today())
        info = {'max_fit: {}': util.get_fitness_info(population).get('max_fit')}
        self.get_out(info)

    def update(self, gene, population):
        info = {'generation': gene, 'pop_num': len(population)}
        fit_info = util.get_fitness_info(population)
        info.update(fit_info)

        self.get_out(info)
        self.update_log(info)
