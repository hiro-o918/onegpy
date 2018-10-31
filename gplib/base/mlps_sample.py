from gplib.utils.config import gp_from_config

if __name__ == '__main__':
    config = {
        "gp": [
            "gplib.base", "MLPS_GP", {'max_evals': 100000, 'depth_limit': 20}
        ],
        "initializer": [
            "gplib.operators", "RandomInitializer", [0.1, 10]
        ],
        "problem": [
            "gplib.problems", "EvenParity", {"dim": 5}
        ],
        "localsearch": [
            "gplib.operators", "FIHC", {"target_node": 'nonterminal', "func_search_type": 'all_check'}
        ]
    }

    mlps = gp_from_config(config)
    mlps()
