from onegpy.utils.config import gp_from_config


if __name__ == '__main__':
    config = {
        'gp': ['onegpy.base', 'PopulationGP'],
        'initializer': [
            'onegpy.operators', 'PopulationRandomInitializer', [500, 0.1, 10]
        ],
        'problem': [
            'onegpy.problems', 'EvenParity', {'dim': 3}
        ],
        'sequential': [
            ['onegpy.operators', 'PopulationOnePointCrossover', {'c_rate': 0.5, 'destructive': False}],
            ['onegpy.operators', 'PopulationPointMutation', {'m_rate': 0.2}],
            ['onegpy.operators', 'TournamentSelection', {'k': 500, 'tournament_size': 5}]
        ],
        'observer': [
            'onegpy.viewers', 'DefaultObserver', {'verbose': 3}
        ],
        "terminal_condition": [
            ["onegpy.terminator", "GenerationTerminator", {"t_gene": 10}],
            ["onegpy.terminator", "EvalCountTerminator", {"t_eval_cnt": 100000}]
        ],
    }

    gp = gp_from_config(config)
    gp()