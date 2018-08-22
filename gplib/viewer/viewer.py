import sys
import datetime
from gplib.utils import util


class AbstractViewer(object):
    def __init__(self, filename='STDOUT'):
        """
                    Class of viewer.

                    :param filename: String.output filename.null: stdout, "STDERR": stderr
        """
        if filename is 'STDOUT':
            self.out = sys.__stdout__
        elif filename is 'STDERR':
            self.out = sys.__stderr__
        else:
            try:
                self.out = open(filename, 'w+')
            except IOError:
                self.out = sys.__stdout__
                print('Cannot open {}.'.format(filename))

    def get_out(self, str_out):
        print(str_out, file=self.out)

    def begin(self):
        raise NotImplementedError

    def end(self, population):
        raise NotImplementedError

    def update(self, gene, population):
        raise NotImplementedError


class DefaultViewer(AbstractViewer):
    def __init__(self, filename='STDOUT'):
        """
            Class of viewer.
        """
        super(DefaultViewer, self).__init__(filename)

    def begin(self):
        self.get_out(datetime.datetime.today())
        self.get_out("-----------begin-----------")

    def end(self, population):
        self.get_out("------------end------------")
        self.get_out(datetime.datetime.today())
        self.get_out("eliteFitness:{}".format(util.get_fitness_info(population).get('max_fit')))
        self.out.close()

    def update(self, gene, population):
        fit_info = util.get_fitness_info(population)
        self.get_out("generation:{} maxFitness:{} averageFitness:{} popNum:{}".format(
            gene, fit_info.get('max_fit'), fit_info.get('ave_fit'), len(population)))
