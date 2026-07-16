class BaseOptimizer:
    def __init__(self, search_space, n_trials=50):
        self.search_space = search_space
        self.n_trials = n_trials
        self.best_params = {}
        self.best_score = float('-inf')
        
    def optimize(self, model, eval_func):
        raise NotImplementedError
