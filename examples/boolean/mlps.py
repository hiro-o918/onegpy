from gplib.utils.config import gp_from_config


if __name__ == '__main__':
    config = {
        "gp": [
            "gplib.base", "MLPS_GP", {'depth_limit': 20}
        ],
        "initializer": [
            "gplib.operators", "RandomInitializer", [0.1, 10]
        ],
        "problem": [
            "gplib.problems", "EvenParity", {"dim": 5}
        ],
        "localsearch": [
            "gplib.operators", "FIHC", {"target_node": 'nonterminal', "func_search_type": 'all_check'}
        ],
        "terminal_condition": [
            ["gplib.terminator", "GenerationTerminator", {"t_gene": 10}],
            ["gplib.terminator", "EvalCountTerminator", {"t_eval_cnt": 100000}]
        ],
        'observer': [
            'gplib.viewers', 'MLPS_Observer', {'verbose': 3}
        ],
    }

    mlps = gp_from_config(config)
    mlps()
