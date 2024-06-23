#!/usr/bin/env python3

from coa import COA
from random_search import RandomSearch
from ioh import get_problem, ProblemClass, Experiment, logger

import numpy
import random

if __name__ == '__main__':
    seed = 42

    dims = [2, 3, 5, 10, 20, 30, 40, 50]
    reps = 5

    numpy.random.seed(seed)
    random.seed(seed)
    expRS = Experiment(algorithm=RandomSearch, fids=list(range(1, 25)), iids=[1],
                    dims=dims, reps=reps,
                    problem_class=ProblemClass.BBOB,
                    output_directory="RS_data", 
                    folder_name="RS_exp_d20_i2500000",
                    algorithm_name="RS", 
                    algorithm_info="",
                    store_positions=True,
                    merge_output=True,
                    zip_output=True,
                    remove_data=True
                    )
    
    expCOA = Experiment(algorithm=COA(P_e=0.1), fids=list(range(1, 25)), iids=[1],
                    dims=dims, reps=reps,
                    problem_class=ProblemClass.BBOB,
                    output_directory="COA_data", 
                    folder_name="COA",
                    algorithm_name="COA", 
                    algorithm_info="",
                    store_positions=True,
                    merge_output=True,
                    zip_output=True,
                    remove_data=True
                    )
    
    expCOA()
    expRS()