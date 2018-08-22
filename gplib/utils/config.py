import json
from collections import OrderedDict
from pathlib import Path

from gplib import operators
from gplib.sequential import Sequential


def sequential_from_json(path):
    path = Path(path)
    with open(path, 'r') as f:
        config = OrderedDict(json.load(f))

    sequential = build_sequential(config)

    return sequential


def build_sequential(config):
    sequential = Sequential()
    for name, args in config.items():
        if isinstance(args, (list, tuple)):
            sequential.add(getattr(operators, name)(*args))
        elif isinstance(args, dict):
            kwargs = args
            sequential.add(getattr(operators, name)(**kwargs))

    return sequential
