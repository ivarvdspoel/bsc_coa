#!/usr/bin/env python3

from ioh import get_problem, ProblemClass, ProblemType
import ioh
import random
import numpy as np

def median(lst):
    s = sorted(lst)
    if len(s) % 2 == 0:
        return (s[len(s) // 2 - 1] + s[len(s) // 2]) / 2
    else:
        return s[len(s) // 2]

class COA:
    """Class for the Coyote Optimization Algorithm"""
    
    class Coyote:
        """Class for the coyote"""
        def __init__(self, social_condition):
            self.age = 0
            self.social_condition = social_condition
            self.obj_value = 0
        
    class Pack:
        """Class for the pack of coyotes"""
        def __init__(self):
            self.coyotes = []
            self.alpha = None
            self.social_tendency = None

    def __init__(self, dimension=5, population_size=100, max_iterations=1000, seed=0, lb=0, ub=1):
        self.dimension = dimension
        self.population_size = population_size
        self.max_iterations = max_iterations
        self.lb = lb
        self.ub = ub
        self.P_s = 1/dimension
        self.P_a = (1-self.P_s)/2
        self.world = [] #List of packs

        self.max_pack_size = 14 # Value from the paper

        # uniformly distributed random number in the range [0,1]
        self.r_1 = np.random.uniform(0,1)
        self.r_2 = np.random.uniform(0,1)

        np.random.seed(seed)
        random.seed(seed)
        
    def init_population(self):
        self.world = []

        i = 0
        while i < self.population_size:
            
            new_pack_size = random.randint(1, self.max_pack_size)
            if (new_pack_size > self.population_size - i):
                new_pack_size = self.population_size - i
            i += new_pack_size
            
            pack = self.Pack()
            for i in range(random.randint(1, new_pack_size)):
                initial_social_condition = [(self.lb + np.random.uniform(0,1)*(self.ub-self.lb)) for _ in range(self.dimension)]
                pack.coyotes.append(self.Coyote(initial_social_condition))
            self.world.append(pack)
        


    def verify_adaptation(self):
        for p in self.world:
            for c in p.coyotes:
                c.obj_value = self.problem(c.social_condition)

    def calculate_alpha_coyote(self, pack):
        index_alpha = 0
        highest_obj_value = 0

        for c in pack.coyotes:
            if c.obj_value > highest_obj_value:
                highest_obj_value = c.obj_value
                index_alpha = pack.coyotes.index(c)

        pack.alpha = pack.coyotes[index_alpha]

    def calculate_social_tendency(self, pack):
        sorted_pack = sorted(pack, key=lambda obj: obj.obj_value)
        middle_index = len(sorted_pack) // 2 #DIT IS NOG NIET JUIST   
        pack.social_tendency = pack.coyotes[middle_index].social_condition

    def update(self, problem, c, pack):
        cr_1 = random.randint(0, len(pack.coyotes)-1)
        cr_2 = random.randint(0, len(pack.coyotes)-1)
        delta_1 = [(pack.alpha.social_condition[i] - pack.coyotes[cr_1].social_condition[i]) for i in range(self.dimension)]
        delta_2 = [(pack.alpha.social_condition[i] - pack.coyotes[cr_2].social_condition[i]) for i in range(self.dimension)]

        new_social_condition = [(c.social_condition[i] + self.r_1*delta_1[i] + self.r_2*delta_2[i]) for i in range(self.dimension)]

        new_fitness = problem(new_social_condition)

        if new_fitness > c.obj_value:
            c.social_condition = new_social_condition

    def transition(self):
        pass

    def birth_and_death(self):
        pass



    def __call__(self, problem: ioh.ProblemType):
        """Optimize the given problem using the COA algorithm"""

        # initialize the population
        self.init_population()

        # calculate objective function for each coyote (social condition)
        self.verify_adaptation()

        # main loop
        for _ in range(self.max_iterations):

            #for each pack p
            for p in self.world:

                # define alpha coyote
                self.calculate_alpha_coyote(p)
                
                # compute social tendency of the pack
                self.calculate_social_tendency(p)

                # for each coyote c in p
                for c in p.coyotes:
                    # update
                    self.update(problem, c, p)
                    
            self.transition()
            self.birth_and_death()

        return problem([0, 1, 2, 3, 4])



if __name__ == '__main__':
    lb = 0
    ub = 1
    dimension = 5
    population_size = 100
    iterations = 1000
    seed = 42
    problem = get_problem(24, 1, dimension, ProblemClass.BBOB)
    alg = COA(dimension, population_size, iterations, seed, lb, ub)
    #logger = ioh.logger.Analyzer(algorithm_name="COA", folder_name="COA")
    #problem.attach_logger()

    opti = alg(problem)
    print(opti)
    #logger.close()
    exit(0)
    