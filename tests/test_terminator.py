# -*- coding: utf-8 -*-

import unittest

from gplib.terminator import GenerationTerminator


class TestGenerationTerminator(unittest.TestCase):
    def setUp(self):
        self.t_gene = 5
        self.t1 = GenerationTerminator(self.t_gene)

    def test_t1(self):
        gene = 0
        while not self.t1():
            gene += 1
        self.assertEqual(gene, self.t_gene)


if __name__ == '__main__':
    unittest.main()
