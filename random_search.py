import numpy as np


class RandomSearch:
    def __init__(self, problem, budget=None):
        self.dimension = problem.meta_data.n_variables
        self.iterations = 1000000
        self.seed = 42
        self.lb = problem.bounds.lb
        self.ub = problem.bounds.ub
        self.__call__(problem)
    
    def __call__(self, problem):
        np.random.seed(self.seed)
        best_fitness = float('inf')
        for _ in range(self.iterations):
            solution = np.random.uniform(self.lb, self.ub, self.dimension)
            fitness = problem(solution)
            if fitness < best_fitness:
                best_fitness = fitness
        return best_fitness