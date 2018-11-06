from onegpy.utils.config import gp_from_config


if __name__ == '__main__':
    config = {
        "gp": ["onegpy.base", "PopulationGP"],
        "initializer": [
            "onegpy.operators", "PopulationRandomInitializer", [500, 0.1, 10]
        ],
        "problem": [
            "onegpy.problems", "Cos2XProblem", {"n_data": 10}
        ],
        "sequential": [
            ["onegpy.operators", "PopulationOnePointCrossover", {"c_rate": 0.9, "destructive": False}],
            ["onegpy.operators", "PopulationPointMutation", {"m_rate": 0.1}],
            ["onegpy.operators", "TournamentSelection", {"k": 500, "tournament_size": 3}]
        ],
        "observer": [
            "onegpy.viewers", "DefaultObserver", {"verbose": 1}
        ],
        "terminal_condition": [
            ["onegpy.terminator", "GenerationTerminator", {"t_gene": 10}],
            ["onegpy.terminator", "EvalCountTerminator", {"t_eval_cnt": 100000}]
        ],
    }

    gp = gp_from_config(config)
    gp()
