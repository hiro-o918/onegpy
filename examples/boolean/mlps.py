from onegpy.utils.config import gp_from_config


if __name__ == '__main__':
    config = {
        "gp": [
            "onegpy.base", "MLPSGP", {'depth_limit': 20}
        ],
        "initializer": [
            "onegpy.operators", "RandomInitializer", [0.1, 10]
        ],
        "problem": [
            "onegpy.problems", "EvenParity", {"dim": 3}
        ],
        "localsearch": [
            "onegpy.operators", "FIHC", {"target_node": 'nonterminal', "func_search_type": 'all_check'}
        ],
        "terminal_condition": [
            ["onegpy.terminator", "GenerationTerminator", {"t_gene": 10}],
            ["onegpy.terminator", "EvalCountTerminator", {"t_eval_cnt": 100000}]
        ],
        'observer': [
            'onegpy.viewers', 'MLPSObserver', {'verbose': 3}
        ],
    }

    mlps = gp_from_config(config)
    mlps()
