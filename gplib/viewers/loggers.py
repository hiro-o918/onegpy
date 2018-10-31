import datetime
import json
from abc import ABC, abstractmethod
import sys
from pathlib import Path


class AbstractLogger(ABC):

    @abstractmethod
    def begin(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def end(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def update(self, *args, **kwargs):
        raise NotImplementedError


class PrintLogger(AbstractLogger):
    def __init__(self, out=sys.stdout):
        """
            Print Logger

            :param out: String.output output to print.
        """

        self._out = out

    def begin(self, **kwargs):
        self._get_out(datetime.datetime.today())
        self._get_out("-----------begin-----------")

    def end(self, log, **kwargs):
        """
        :param log: dict.
        """
        self._get_out("------------end------------")
        self._get_out(datetime.datetime.today())

        self._get_out(log)

    def update(self, log, **kwargs):
        self._get_out(log)

    def _get_out(self, log):
        if isinstance(log, dict):
            log = ', '.join(['{}: {}'.format(k, v) for k, v in log.items()])
        if isinstance(log, list):
            log = ', '.join(log)

        print(log, file=self._out)


class JSONLogger(AbstractLogger):
    def __init__(self, filedir=Path('.'), filename='log', save_every_updating=False):
        """
        JSON Logger

        :param filedir: str or Path. Directory to dump json.
        :param filename: str or Path. Name of json
        :param save_every_updating: bool. if true, save history every updating.
         otherwise save only in the end.
        """
        self._filedir = Path(filedir)
        if not self._filedir.exists():
            self._filedir.mkdir(parents=True)

        self._filepath = self._filedir.joinpath(filename)
        self._save_every_updating = save_every_updating

    def begin(self, **kwargs):
        pass

    def end(self, history, **kwargs):
        self._dump(history)

    def update(self, history, **kwargs):
        if self._save_every_updating:
            self._dump(history)

    def _dump(self, history):
        with open(self._filepath, 'w') as f:
            json.dump(history, f, indent=4)
