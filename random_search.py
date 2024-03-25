import numpy as np

class RandomSearch:
    def __init__(self, dimension, iterations, seed, lb, ub):
        self.dimension = dimension
        self.iterations = iterations
        self.seed = seed
        self.lb = lb
        self.ub = ub
    
    def __call__(self, problem):
        np.random.seed(self.seed)
        best_fitness = float('inf')
        for _ in range(self.iterations):
            solution = np.random.uniform(self.lb, self.ub, self.dimension)
            fitness = problem(solution)
            if fitness < best_fitness:
                best_fitness = fitness
        return best_fitness