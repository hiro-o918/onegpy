import unittest
from pathlib import Path

from gplib.utils.config import gp_from_config


# TODO: Develop test cases
class TestConfig(unittest.TestCase):
    def test_gp_from_config(self):
        path = Path('tests/utils/gp_config.json')
        gp = gp_from_config(path)
        gp()

