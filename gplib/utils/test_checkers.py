import unittest

from gplib.utils import checkers


class TestCheckers(unittest.TestCase):
    def test_prob_checkers(self):
        with self.assertRaises(ValueError):
            checkers.prob_checker(2)
            checkers.prob_checker(-1)

        checkers.prob_checker(0.1)
        checkers.prob_checker(1)
        checkers.prob_checker(0)