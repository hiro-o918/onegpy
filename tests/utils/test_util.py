import unittest

from onegpy.operators import RandomSelection
from onegpy.solutions.node import Node
from onegpy.solutions.solution import Solution
from onegpy.utils.util import get_generator_builder


class TestUtil(unittest.TestCase):
    def test_get_generator_builder(self):
        n_pop = 100
        population = [Solution(Node())] * n_pop
        k = 10
        selection = RandomSelection(k=k, replacement=True)

        generator_builder = get_generator_builder(selection)
        generator = generator_builder(population)

        n_selected = 10
        selected_pop_list = []
        for pop in generator:
            selected_pop_list.append(pop)
            if len(selected_pop_list) == n_selected:
                break

        self.assertEqual(len(selected_pop_list), n_selected)

        for pop in selected_pop_list:
            self.assertEqual(len(pop), k)
