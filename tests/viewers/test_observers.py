import unittest

from onegpy.solutions import solution, node
from onegpy.viewers import DefaultObserver
from onegpy.viewers.observer import MLPS_Observer


def get_population():
    s1 = solution.Solution(node.Node())
    s2 = solution.Solution(node.Node())
    s3 = solution.Solution(node.Node())
    solution.set_previous_fitness(s1, 1)
    solution.set_previous_fitness(s2, 2)
    solution.set_previous_fitness(s3, 3)

    pop = []
    for _ in range(2):
        pop.extend([s1, s2, s3])
    pop = pop * 2

    return pop


class TestDefaultObserver(unittest.TestCase):
    def setUp(self):
        self.observer = DefaultObserver()
        self.pop = get_population()

    def begin(self):
        self.observer.begin()

    def update(self):
        self.observer.update(1, self.pop)

    def end(self):
        self.observer.end(self.pop)


class TestMLPS_Observer(unittest.TestCase):
    def setUp(self):
        self.observer = MLPS_Observer()
        self.population_list = [get_population()] * 3

    def begin(self):
        self.observer.begin()

    def update(self):
        self.observer.update(1, 1, self.population_list)

    def end(self):
        self.observer.end(1, 1, self.population_list)
