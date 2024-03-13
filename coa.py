#!/usr/bin/env python3

from ioh import get_problem, ProblemClass, ProblemType
import ioh
import random
import numpy as np

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

        np.random.seed(seed)
        random.seed(seed)

        self.r_1 = np.random.uniform(0,1)
        self.r_2 = np.random.uniform(0,1)
        
    def init_population(self):
        self.world = []

        i = 0

        while i < self.population_size:
            new_pack_size = random.randint(1, self.max_pack_size)
            if (new_pack_size > self.population_size - i):
                new_pack_size = self.population_size - i
            i += new_pack_size
            
            pack = self.Pack()
            for _ in range(random.randint(1, new_pack_size)):
                initial_social_condition = [(self.lb + np.random.uniform(0,1)*(self.ub-self.lb)) for _ in range(self.dimension)]
                pack.coyotes.append(self.Coyote(initial_social_condition))
            self.world.append(pack)
        


    def verify_adaptation(self, problem):
        for p in self.world:
            for c in p.coyotes:
                c.obj_value = problem(c.social_condition)

    def calculate_alpha_coyote(self, pack):
        index_alpha = 0
        highest_obj_value = pack.coyotes[0].obj_value

        for c in pack.coyotes:
            if c.obj_value > highest_obj_value:
                highest_obj_value = c.obj_value
                index_alpha = pack.coyotes.index(c)

        pack.alpha = pack.coyotes[index_alpha]

    def calculate_social_tendency(self, pack):
        sorted_pack = sorted(pack.coyotes, key=lambda obj: obj.obj_value)
        if (len(sorted_pack) % 2 == 1): # odd
            pack.social_tendency = sorted_pack[((len(sorted_pack) +1) // 2) - 1].social_condition
        else:
            pack.social_tendency = [(sorted_pack[len(sorted_pack) // 2 - 1].social_condition[i] + sorted_pack[len(sorted_pack) // 2].social_condition[i]) / 2 for i in range(self.dimension)]


    def update(self, problem, c, pack):
        cr_1 = random.randint(0, len(pack.coyotes)-1)
        cr_2 = random.randint(0, len(pack.coyotes)-1)

        delta_1 = [(pack.alpha.social_condition[i] - pack.coyotes[cr_1].social_condition[i]) for i in range(self.dimension)]
        delta_2 = [(pack.social_tendency[i] - pack.coyotes[cr_2].social_condition[i]) for i in range(self.dimension)]

        print("old: ", c.social_condition)

        new_social_condition = [(c.social_condition[i] + self.r_1*delta_1[i] + self.r_2*delta_2[i]) for i in range(self.dimension)]


        print("new: ", new_social_condition)

        new_fitness = problem(new_social_condition)

        if new_fitness > c.obj_value:
            c.social_condition = new_social_condition
            c.obj_value = new_fitness

    def transition(self):
        for p in self.world:
            for c in p.coyotes:
                N_c = len(p.coyotes)
                P_e = 0.005*N_c*N_c
                if (P_e < np.random.uniform(0,1)):
                   
                    p.coyotes.remove(c)
                    if (len(p.coyotes) == 0):
                        self.world.remove(p)

                    new_pack_nr = random.randint(0, len(self.world))
                    if (new_pack_nr == len(self.world)):
                        new_pack = self.Pack()
                        new_pack.coyotes.append(c)
                        self.world.append(new_pack)
                    else:
                        self.world[new_pack_nr].coyotes.append(c)



    def birth_and_death(self, problem, pack):
        j_1 = random.randint(0, dimension - 1)
        j_2 = random.randint(0, dimension - 1)

        r_1 = random.randint(0, len(pack.coyotes) - 1)
        r_2 = random.randint(0, len(pack.coyotes) - 1)

        pup_social_condition = [0 for _ in range(dimension)]
        for j in range(dimension):
            rnd_j = random.uniform(0,1)
            if (rnd_j < self.P_s or j == j_1):
                pup_social_condition[j] = pack.coyotes[r_1].social_condition[j]
            elif (rnd_j >= self.P_s + self.P_a or j == j_2):
                pup_social_condition[j] = pack.coyotes[r_2].social_condition[j]
            else:
                pup_social_condition[j] = (random.uniform(lb,ub))

        pup_fitness = problem(pup_social_condition)

        phi = len(pack.coyotes)
        omega = []

        for c in pack.coyotes:
            if (c.obj_value < pup_fitness):
                omega.append(c)

        if (phi == 1):
            pack.coyotes = []
            pack.coyotes.append(self.Coyote(pup_social_condition))
        elif (phi > 1):
            if (len(omega) > 0):
                oldest_coyote = omega[0]
                for c in omega:
                    if (c.age > oldest_coyote.age):
                        oldest_coyote = c
                pack.coyotes.remove(oldest_coyote)
            pack.coyotes.append(self.Coyote(pup_social_condition))


    def update_age(self):
        for p in self.world:
            for c in p.coyotes:
                c.age += 1

    def best_coyote_fitness(self):
        best_coyote_fitness = self.world[0].coyotes[0].obj_value
        best_coyote = self.world[0].coyotes[0]
        for pack in self.world:
            for coyote in pack.coyotes:
                if coyote.obj_value > best_coyote_fitness:
                    best_coyote_fitness = coyote.obj_value
                    best_coyote = coyote

        print(best_coyote.social_condition)
        return best_coyote_fitness
    
    def __call__(self, problem: ioh.ProblemType):
        """Optimize the given problem using the COA algorithm"""

        # initialize the population
        self.init_population()

        # calculate objective function for each coyote (social condition)
        self.verify_adaptation(problem)

        # main loop
        for _ in range(self.max_iterations):

            #for each pack p
            for pack in self.world:

                # define alpha coyote
                self.calculate_alpha_coyote(pack)
                
                # compute social tendency of the pack
                self.calculate_social_tendency(pack)

                # for each coyote c in p
                for coyote in pack.coyotes:
                    # update
                    self.update(problem, coyote, pack)
                    
                self.birth_and_death(problem, pack)
            
            self.transition()

            self.update_age()


        return self.best_coyote_fitness()



if __name__ == '__main__':
    lb = 0
    ub = 1
    dimension = 5
    population_size = 100
    iterations = 5
    seed = 42
    problem = get_problem(24, 1, dimension, ProblemClass.BBOB)
    alg = COA(dimension, population_size, iterations, seed, lb, ub)
    #logger = ioh.logger.Analyzer(algorithm_name="COA", folder_name="COA")
    #problem.attach_logger()

    opti = alg(problem)
    print(opti)
    #logger.close()
    exit(0)
    