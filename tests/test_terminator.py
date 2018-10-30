# -*- coding: utf-8 -*-

import unittest

from gplib.terminal_condition import TerminalCondition
from gplib.terminatior import GenerationTerminator
from gplib.problems import arithmetic


class TestGenerationTerminator(unittest.TestCase):
    def setUp(self):
        self.problem = arithmetic.Cos2XProblem(1)
        self.t_gene = 5
        self.t1 = GenerationTerminator(self.problem, self.t_gene)

    def test_t1(self):
        gene = 0
        while not self.t1():
            gene += 1
        self.assertEqual(gene, self.t_gene)


if __name__ == '__main__':
    unittest.main()
