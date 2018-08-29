import json
from collections import OrderedDict
from pathlib import Path
import importlib

from gplib.operator import ProblemBasedOperator
from gplib.sequential import Sequential


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


def build_viewer(module, name, params, **kwargs):
    return build_instance(module, name, params)


def build_gp(module, name, params, initializer, sequential, viewer, **kwargs):
    return build_instance(module, name, params,
                          initializer=initializer, sequential=sequential, viewer=viewer)


CONFIG_TAGS = ['problem', 'initializer', 'sequential', 'viewer', 'gp']
BUILDER_MAP = {'problem': build_problem,
               'initializer': build_operator,
               'sequential': build_sequential,
               'viewer': build_viewer,
               'gp': build_gp}


def check_config(config):
    for key in config.keys():
        if key not in CONFIG_TAGS:
            msg = 'key must be selected from {}'.format(CONFIG_TAGS)
            raise ValueError(msg)


def gp_from_config(path_or_config):
    if isinstance(path_or_config, dict):
        config = path_or_config
    else:
        path_or_config = Path(path_or_config)
        with open(path_or_config, 'r') as f:
            config = json.load(f)

    instance_dict = {}
    for tag in CONFIG_TAGS:
        if tag == 'sequential':
            instance_dict.update({tag: build_sequential(config[tag], **instance_dict)})
        else:
            module, name, params = unwrap_instance_info(config[tag])
            builder = BUILDER_MAP[tag]
            instance_dict.update({tag: builder(module, name, params, **instance_dict)})

    gp = instance_dict['gp']

    return gp
