#!/usr/bin/env python3

from ioh import ProblemType
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
            self.obj_value = float('inf')
        
    class Pack:
        """Class for the pack of coyotes"""
        def __init__(self):
            self.coyotes = []
            self.alpha = None
            self.social_tendency = None
    
    def __init__(self,  P_s=None, P_a=None, P_e=None, budget=None, population=200,
                 max_pack_size=14,stopping_condition=4000, initial_pack_size=[5,10]):
        self.population_size = population 
        self.max_iterations = stopping_condition
        
        self.max_pack_size = max_pack_size
        
        self.P_s = P_s
        self.P_a = P_a
        
        self.P_e = P_e
            
        
        self.initial_pack_size = initial_pack_size
    

        self.r_1 = np.random.uniform(0,1)
        self.r_2 = np.random.uniform(0,1)

        self.world = [] #List of packs



    def calc_P_e(self, N_c):
        if (self.P_e is None):
            return 0.005*N_c**2
        else:
            return self.P_e
    
    def init_population(self):
        self.world = [] 

        i = 0
    
        while i < self.population_size:
            # Create a new pack with a random size
            new_pack_size = random.randint(self.initial_pack_size[0],self.initial_pack_size[1]) # Hard values
            if (new_pack_size > self.population_size - i):
                # If the new pack size is too big, reduce it
                new_pack_size = self.population_size - i
            i += new_pack_size
            
            # Create the pack
            pack = self.Pack()
            for _ in range(new_pack_size):
                # Create a new coyote with a random social condition
                initial_social_condition = [(self.lb[i] + np.random.uniform(0,1)*(self.ub[i]-self.lb[i])) for i in range(self.dimension)]
                pack.coyotes.append(self.Coyote(initial_social_condition))
            self.world.append(pack)
        

    def verify_adaptation(self, problem):
        for p in self.world:
            for c in p.coyotes:
                c.obj_value = problem(c.social_condition)

    def calculate_alpha_coyote(self, pack):
        if (len(pack.coyotes) == 0):
            return
        
        # Find the alpha coyote
        
        index_alpha = 0
        highest_obj_value = float('inf')

        for c in pack.coyotes:
            if c.obj_value < highest_obj_value:
                highest_obj_value = c.obj_value
                index_alpha = pack.coyotes.index(c)

        # Set the alpha coyote
        pack.alpha = pack.coyotes[index_alpha]


    def calculate_social_tendency(self, pack):
        if(len(pack.coyotes) == 0):
            return
        
        sorted_pack = sorted(pack.coyotes, key=lambda obj: obj.obj_value)
        
        #Return the median of the sorted pack
        # Use equation 6 from original paper
        if (len(sorted_pack) % 2 == 1): # odd
            pack.social_tendency = sorted_pack[((len(sorted_pack) +1) // 2) - 1].social_condition
        else: # even
            pack.social_tendency = [(sorted_pack[len(sorted_pack) // 2 - 1].social_condition[i] + sorted_pack[len(sorted_pack) // 2].social_condition[i]) / 2 for i in range(self.dimension)]


    def update(self, problem, c, pack):
        if(len(pack.coyotes) == 0):
            return
        
        # Select two random coyotes
        cr_1 = random.randint(0, len(pack.coyotes)-1)
        cr_2 = random.randint(0, len(pack.coyotes)-1)

        # Calculate delta_1 and delta_2
        delta_1 = [(pack.alpha.social_condition[i] - pack.coyotes[cr_1].social_condition[i]) for i in range(self.dimension)]
        delta_2 = [(pack.social_tendency[i] - pack.coyotes[cr_2].social_condition[i]) for i in range(self.dimension)]

        # Calculate new social condition
        new_social_condition = [(c.social_condition[i] + self.r_1*delta_1[i] + self.r_2*delta_2[i]) for i in range(self.dimension)]

        # Check if new social condition is within bounds
        for i  in range(self.dimension):
            if new_social_condition[i] < self.lb[i]:
                new_social_condition[i] = self.lb[i]
            elif new_social_condition[i] > self.ub[i]:
                new_social_condition[i] = self.ub[i]

        # Calculate new fitness
        new_fitness = problem(new_social_condition)

        # Adaptation
        if new_fitness < c.obj_value:
            c.social_condition = new_social_condition
            c.obj_value = new_fitness




    def transition_evenly(self):
        for i, p in enumerate(self.world[:]):  # Iterate over a copy of the list to safely remove items
            for c in p.coyotes[:]:  # Similarly, iterate over a copy to safely remove items
                
                N_c = len(p.coyotes)
                
                chance = np.random.uniform(0, 1)
                
                if self.calc_P_e(N_c) > chance: # Default P_e = 0.005*N_c^2
                    
                    self.world[i].coyotes.remove(c)

                    pack_sizes = [len(pack.coyotes) for pack in self.world] # Get the size of each pack
                    
                    inverse_sizes = [1.0 / (size + 1) for size in pack_sizes] # Inverse of the size of each pack, +1 to avoid division by zero
                    
                    total_inverse_size = sum(inverse_sizes) # Sum of all inverse sizes
                    
                    probabilities = [inv_size / total_inverse_size for inv_size in inverse_sizes] # Probabilities of each pack

                    new_pack_nr = np.random.choice(len(self.world), p=probabilities) # Choose a pack based on the probabilities
                    
                    if len(self.world[new_pack_nr].coyotes) < self.max_pack_size:
                        self.world[new_pack_nr].coyotes.append(c)
                    else:
                        self._create_new_pack(c) # Create a new pack with the coyote

    def _create_new_pack(self, coyote):
        new_pack = self.Pack()
        new_pack.coyotes.append(coyote)
        self.world.append(new_pack)

    def transition(self):
        # Iterate over all packs
        for p in self.world:
            for c in p.coyotes:
                N_c = len(p.coyotes)
                chance = np.random.uniform(0,1)
                if (self.calc_P_e(N_c) > chance): # Default P_e = 0.005*N_c^2
                   
                    p.coyotes.remove(c)
                    if (len(p.coyotes) == 0):
                        self.world.remove(p)

                    # Choose a random pack
                    new_pack_nr = random.randint(0, len(self.world ) - 1)
                    if (len(self.world[new_pack_nr].coyotes) < self.max_pack_size):
                        self.world[new_pack_nr].coyotes.append(c)
                    else:
                        new_pack = self.Pack()
                        new_pack.coyotes.append(c)
                        self.world.append(new_pack)


    def birth_and_death(self, problem, pack):
        if(len(pack.coyotes) == 0):
            return
        
        # Select two random indexes
        j_1 = random.randint(0, self.dimension - 1)
        j_2 = random.randint(0, self.dimension - 1)

        # Select two random coyotes
        r_1 = random.randint(0, len(pack.coyotes) - 1)
        r_2 = random.randint(0, len(pack.coyotes) - 1)

        # Create new pup
        pup_social_condition = [0 for _ in range(self.dimension)]
        
        # Create social condition for the pup
        # Equation 6 in original paper
        for j in range(self.dimension):
            rnd_j = random.uniform(0,1)
            if (rnd_j < self.P_s or j == j_1):
                pup_social_condition[j] = pack.coyotes[r_1].social_condition[j]
            elif (rnd_j >= self.P_s + self.P_a or j == j_2):
                pup_social_condition[j] = pack.coyotes[r_2].social_condition[j]
            else:
                pup_social_condition[j] = (random.uniform(self.lb[j],self.ub[j]))

        # Calculate fitness of the pup
        pup_fitness = problem(pup_social_condition)


        phi = len(pack.coyotes)
        omega = []

        # omega is the set of coyotes with fitness higher than the pup
        for c in pack.coyotes:
            if (c.obj_value > pup_fitness):
                omega.append(c)

        if (phi == 1): # If the pack has only one coyote
            pack.coyotes[0] = self.Coyote(pup_social_condition)
        elif (phi > 1): # If the pack has more than one coyote
            if (len(omega) > 0):
                # Remove the oldest coyote from the pack
                oldest_coyote = omega[0]
                for c in omega:
                    if (c.age > oldest_coyote.age):
                        oldest_coyote = c
                pack.coyotes.remove(oldest_coyote) # Remove the oldest coyote from the pack
                pack.coyotes.append(self.Coyote(pup_social_condition)) # Add the pup to the pack


    def update_age(self):
        for p in self.world:    
            for c in p.coyotes:
                c.age += 1

    def best_coyote(self):
        # Find the best coyote in the world
        best_coyote_fitness = float('inf')
        best_coyote = None
        for pack in self.world:
            for coyote in pack.coyotes:
                if coyote.obj_value < best_coyote_fitness:
                    best_coyote_fitness = coyote.obj_value
                    best_coyote = coyote

        # Return the best coyote
        return best_coyote

    def remaining_inits(self, problem):
        
        #Remaining initializations
        self.problem = problem
        self.dimension = problem.meta_data.n_variables
        self.lb = problem.bounds.lb
        self.ub = problem.bounds.ub
        
        # remaining P_s edge case
        if self.P_s is None:
            self.P_s = 1 / self.dimension
        if self.P_a is None:
            self.P_a = (1 - self.P_s) / 2
    
    def __call__(self, problem: ioh.ProblemType):
        """Optimize the given problem using the COA algorithm"""
        
        self.remaining_inits(problem)
        
        # initialize the population
        self.init_population()

        # calculate objective function for each coyote (social condition)
        self.verify_adaptation(problem)

        # main loop

        i = 0

        while i < self.max_iterations:        
            for pack in self.world:

                # define alpha coyote
                self.calculate_alpha_coyote(pack)
                
                # compute social tendency of the pack
                self.calculate_social_tendency(pack)

                # for each coyote c in p
                for coyote in pack.coyotes:
                    # update
                    self.update(problem, coyote, pack)
                    
                # birth and death
                self.birth_and_death(problem, pack)
            
            # transition
            self.transition_evenly()

            # update age
            self.update_age()

            i += 1
            
        return self.best_coyote().obj_value



