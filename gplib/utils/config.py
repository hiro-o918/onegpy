import json
from pathlib import Path
import importlib

from gplib.operator import ProblemBasedOperator
from gplib.terminator import ProblemBasedTerminator
from gplib.sequential import Sequential
from gplib.terminal_condition import TerminalCondition


def build_instance(module, name, params, *args, **kwargs):
    if params is None:
        return getattr(module, name)(*args, **kwargs)
    elif isinstance(params, (list, tuple)):
        return getattr(module, name)(*params, *args, **kwargs)
    elif isinstance(params, dict):
        kwargs.update(params)
        return getattr(module, name)(*args, **kwargs)
    else:
        msg = 'Invalid arguments'
        Exception(msg)
    print('Imported from {}'.format(module))
    print('Build {} using params {}'.format(name, params))


def unwrap_instance_info(instance_info):
    if len(instance_info) == 2:
        module_name, name = instance_info
        params = None
    elif len(instance_info) == 3:
        module_name, name, params = instance_info
    else:
        msg = 'Unsupported `instance_info` format. Reformat the items of the config to follow the below format:\n' \
              '[module_path, name] or [module_path, name, params]'
        raise ValueError(msg)
    module = importlib.import_module(module_name)

    return module, name, params


def build_problem(module, name, params, **kwargs):
    return build_instance(module, name, params)


def build_operator(module, name, params, **kwargs):
    if issubclass(getattr(module, name), ProblemBasedOperator):
        return build_instance(module, name, params, problem=kwargs['problem'])
    else:
        return build_instance(module, name, params)


def build_sequential(operator_configs, **kwargs):
    sequential = Sequential()
    for operator_config in operator_configs:
        module, name, params = unwrap_instance_info(operator_config)
        sequential.add(build_operator(module, name, params, **kwargs))

    return sequential


def build_observer(module, name, params, **kwargs):
    return build_instance(module, name, params)


def build_terminator(module, name, params, **kwargs):
    if issubclass(getattr(module, name), ProblemBasedTerminator):
        return build_instance(module, name, params, problem=kwargs['problem'])
    else:
        return build_instance(module, name, params)


def build_terminal_condition(terminator_configs, **kwargs):
    t_condition = TerminalCondition()
    for terminator_config in terminator_configs:
        module, name, params = unwrap_instance_info(terminator_config)
        t_condition.add(build_terminator(module, name, params, **kwargs))

    return t_condition


def check_config(config, config_tags):
    for key in config.keys():
        if key not in config_tags:
            msg = 'key must be selected from {}'.format(config_tags)
            raise ValueError(msg)


def check_builder_map(config_tags, builder_map):
    for tag in config_tags:
        if tag not in builder_map:
            raise ValueError('There is no {} in builder_map'.format(tag))


def gp_from_config(path_or_config, config_tags=None, builder_map=None):
    """
    Create a gp instance based on config.
    Keys of config indicate instances' name and values follows below format.
    `[module, class or function, list or dict of arguments]`
    where list or dict of arguments only contains hyper parameters not dependent instances

    :param path_or_config: filepath or dict
    :param config_tags: list of instance names. All the instances are built in this order.
    Tags which are not in `config` will be skipped.
    :param builder_map: dict. the mapper of instances' names to their builder
    :return gp: a gp instance

    - Example of config
        config = {
            "gp": ["gplib.base", "PopulationGP", [20]],
            "initializer": [
                "gplib.operators", "PopulationRandomInitializer", [500, 0.1, 10]
            ],
            "problem": [
                "gplib.problems", "EvenParity", {"dim": 3}
            ],
            "sequential": [
                ["gplib.operators", "PopulationOnePointCrossover", {"c_rate": 0.5, "destructive": False}],
                ["gplib.operators", "PopulationPointMutation", {"m_rate": 0.2}],
                ["gplib.operators", "TournamentSelection", {"k": 500, "tournament_size": 5}]
            ],
            "logger": [
                "gplib.viewers", "DefaultObserver"
            ]
        }
    """

    if isinstance(path_or_config, dict):
        config = path_or_config
    else:
        path_or_config = Path(path_or_config)
        with open(path_or_config, 'r') as f:
            config = json.load(f)

    # set default config_tags and builder_map.
    if config_tags is None:
        config_tags = ['problem',
                       'initializer',
                       'sequential',
                       'localsearch',
                       'observer',
                       'terminal_condition',
                       'gp']
    if builder_map is None:
        builder_map = {'problem': build_problem,
                       'initializer': build_operator,
                       'sequential': build_sequential,
                       'localsearch': build_operator,
                       'observer': build_observer,
                       'terminal_condition': build_terminal_condition,
                       'gp': build_instance}

    check_config(config, config_tags)
    check_builder_map(config_tags, builder_map)

    instance_dict = {}
    for tag in config_tags:
        if tag not in config:
            continue

        if tag == 'sequential':
            instance_dict.update({tag: build_sequential(config[tag], **instance_dict)})
        elif tag == 'terminal_condition':
            instance_dict.update({tag: build_terminal_condition(config[tag], **instance_dict)})
        else:
            module, name, params = unwrap_instance_info(config[tag])
            builder = builder_map[tag]
            instance_dict.update({tag: builder(module, name, params, **instance_dict)})

    gp = instance_dict['gp']

    return gp
