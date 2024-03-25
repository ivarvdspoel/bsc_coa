#!/usr/bin/env python3

from coa import COA
from random_search import RandomSearch
from ioh import get_problem, ProblemClass, Experiment

if __name__ == '__main__':
    dimension = 10
    population_size = 100

    iterations = 5000

    seed = 42
    
    problem = get_problem(24, 1, dimension, ProblemClass.BBOB)
    
    print(problem.optimum)
    lb = problem.bounds.lb
    ub = problem.bounds.ub
    alg = COA(dimension, population_size, iterations, seed, lb, ub)
    random_search = RandomSearch(dimension, iterations, seed, lb, ub)
    #logger = ioh.logger.Analyzer(algorithm_name="COA", folder_name="COA")
    #problem.attach_logger()

    opti = alg(problem)
    random_result = random_search(problem)
    print("COA: ", opti)
    print("Random Search:", random_result)
    #logger.close()
    exit(0)
    # example 1, expeirment the algorithm step by step
    print('###############################Example 1###############################')
    # step 1, get a BBOB problem (with fid 1, instance id 1, dimensionality 20)
    problem = get_problem(fid=1, instance=1, dimension=20,
                        problem_class=ProblemClass.BBOB)
    # step 2, create a ioh.logger to log the experiment data for further analyzing
    # on IOHanalyzer
    l = logger.Analyzer(
        root="data_examples",
        folder_name="example_1",
        algorithm_name="random search, example 1",
        algorithm_info=""
    )
    # step 3, attach the logger to the problem
    problem.attach_logger(l)
    # step 4, run the algorithm that optimize on the problem attached by logger
    RandomSearch(problem)
    del l, problem

    # example 2, a quick start of ioh.Experiment
    print('###############################Example 2###############################')
    # a very basic setup of ioh.Experiment
    exp = Experiment(algorithm=RandomSearch, fids=[1, 5, 24], iids=[1],
                    dims=[5, 20], reps=10, problem_class=ProblemClass.BBOB,
                    output_directory="data_examples", folder_name="example_2",
                    algorithm_name="random search, example 2", algorithm_info="")
    # run the experiment
    exp()

    # example 3, a more comprehensive example of ioh.Experiment
    print('###############################Example 2###############################')
    exp = Experiment(algorithm=RandomSearch, fids=list(range(1, 25)), iids=[1],
                    dims=[2, 3, 5, 10, 20, 40], reps=10,
                    problem_class=ProblemClass.BBOB,
                    output_directory="data_examples", folder_name="example_3",
                    algorithm_name="random search, example 3", algorithm_info="",
                    store_positions=True, merge_output=True, zip_output=True, 
                    remove_data=True)
    exp()