# -*- coding: utf-8 -*-

import unittest

from gplib.terminal_condition import TerminalCondition
from gplib.terminatior import AbstractTerminator
from gplib.problems import arithmetic


class TestTrue(AbstractTerminator):
    def __call__(self):
        return True


class TestFalse(AbstractTerminator):
    def __call__(self):
        return False


class TestTerminalCondition(unittest.TestCase):
    def setUp(self):
        self.problem = arithmetic.Cos2XProblem(1)
        self.t1 = TestTrue(self.problem)
        self.t2 = TestFalse(self.problem)
        self.T1 = TerminalCondition([self.t1, self.t2])
        self.T2 = TerminalCondition([self.t1, self.t1])

    def testT1(self):
        self.assertFalse(self.T1())

    def testT2(self):
        self.assertTrue(self.T2())


if __name__ == '__main__':
    unittest.main()
