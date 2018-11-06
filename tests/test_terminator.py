# -*- coding: utf-8 -*-

import unittest

from onegpy.terminator import GenerationTerminator
from onegpy.terminator import TerminalCondition
from onegpy.terminator import AbstractTerminator
from onegpy.problems import arithmetic


class TestGenerationTerminator(unittest.TestCase):
    def setUp(self):
        self.t_gene = 5
        self.t1 = GenerationTerminator(self.t_gene)

    def test_t1(self):
        gene = 0
        while not self.t1():
            gene += 1
        self.assertEqual(gene, self.t_gene)


class TestTrue(AbstractTerminator):
    def __call__(self):
        return True


class TestFalse(AbstractTerminator):
    def __call__(self):
        return False


class TestTerminalCondition(unittest.TestCase):
    def setUp(self):
        self.problem = arithmetic.Cos2XProblem(1)
        self.t1 = TestFalse()
        self.t2 = TestTrue()
        self.T1 = TerminalCondition([self.t1, self.t1])
        self.T2 = TerminalCondition([self.t2, self.t2])

    def testT1(self):
        self.assertFalse(self.T1())

    def testT2(self):
        self.assertTrue(self.T2())


if __name__ == '__main__':
    unittest.main()
