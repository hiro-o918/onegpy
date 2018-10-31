import unittest

from gplib.viewers.loggers import PrintLogger
from gplib.solutions import solution, node


class TestPrintLogger(unittest.TestCase):
    def setUp(self):
        self.logger = PrintLogger()
        s1 = solution.Solution(node.Node())
        s2 = solution.Solution(node.Node())
        s3 = solution.Solution(node.Node())
        solution.set_previous_fitness(s1, 1)
        solution.set_previous_fitness(s2, 2)
        solution.set_previous_fitness(s3, 3)

        self.pop = []
        for _ in range(2):
            self.pop.extend([s1, s2, s3])
        self.pop = self.pop*2

    def test_begin(self):
        self.logger.begin()

    def test_update(self):
        self.logger.update(1)

    def test_end(self):
        self.logger.end('log')


class TestJSONLogger(unittest.TestCase):
    # TODO: write this
    pass


if __name__ == '__main__':
    unittest.main()
