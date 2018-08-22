import unittest
from collections import OrderedDict
from pathlib import Path

from gplib.utils.config import sequential_from_json, build_sequential


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config = \
            OrderedDict({
                    "PopulationOnePointCrossover": {
                    "c_rate": 1,
                    "destructive": False
                    },
                    "RandomSelection": [2, True],
                    "OnePointCrossover": [1]
                    })

    def test_sequential_from_json(self):
        path = Path('tests/utils/config.json')
        sequential = sequential_from_json(path)

    def test_build_sequential(self):
        sequential = build_sequential(self.config)
        for name, operator in zip(self.config.keys(), sequential.operators):
            self.assertEqual(name, operator.__class__.__name__)

