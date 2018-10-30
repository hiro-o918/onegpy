from gplib.utils.config import gp_from_config


if __name__ == '__main__':
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
            "gplib.loggers", "DefaultLogger"
        ]
    }

    gp = gp_from_config(config)
    gp()
