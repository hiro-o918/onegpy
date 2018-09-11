import unittest

from gplib.viewer.viewer import DefaultViewer
from gplib.solutions import solution, node
from gplib.utils import util


class TestDefaultViewer(unittest.TestCase):
    def setUp(self):
        self.viewer = DefaultViewer()
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
        self.viewer.begin()

    def test_update(self):
        self.viewer.update(1, self.pop)

    def test_end(self):
        self.viewer.end(self.pop)





if __name__ == '__main__':
    unittest.main()