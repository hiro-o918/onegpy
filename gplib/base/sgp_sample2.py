from gplib.utils.config import gp_from_config


if __name__ == '__main__':
    config = {
        "gp": ["gplib.base", "PopulationGP", [100]],
        "initializer": [
            "gplib.operators", "PopulationRandomInitializer", [500, 0.1, 10]
        ],
        "problem": [
            "gplib.problems", "Cos2XProblem", {"data": 20}
        ],
        "sequential": [
            ["gplib.operators", "PopulationOnePointCrossover", {"c_rate": 0.9, "destructive": False}],
            ["gplib.operators", "PopulationPointMutation", {"m_rate": 0.1}],
            # ["gplib.operators", "EliteSelection", {"k": 1}],
            ["gplib.operators", "TournamentSelection", {"k": 500, "tournament_size": 3}]
        ],
        "viewer": [
            "gplib.viewer", "DefaultViewer"
        ]
    }

    gp = gp_from_config(config)
    gp()
