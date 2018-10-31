import unittest

from gplib.viewers.loggers import PrintLogger, JSONLogger
from gplib.solutions import solution, node


class TestPrintLogger(unittest.TestCase):
    def setUp(self):
        self.logger = PrintLogger()


    def test_begin(self):
        self.logger.begin()

    def test_update(self):
        self.logger.update(1)

    def test_end(self):
        self.logger.end('log')


class TestJSONLogger(unittest.TestCase):
    def setUp(self):
        self.logger = JSONLogger()

    def test_begin(self):
        self.logger.begin()

    def test_update(self):
        self.logger.update(1)

    def test_end(self):
        self.logger.end('log')


if __name__ == '__main__':
    unittest.main()
