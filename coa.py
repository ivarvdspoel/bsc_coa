#!/usr/bin/env python3

from ioh import get_problem, ProblemClass, ProblemType
import ioh

class COA:
    """Class for the Coyote Optimization Algorithm"""
    def __call__(self, problem: ioh.ProblemType):

        return problem([0, 1, 2, 3, 4])



if __name__ == '__main__':
    problem = get_problem(24, 1, 5, ProblemClass.BBOB)
    alg = COA()
    #logger = ioh.logger.Analyzer(algorithm_name="COA", folder_name="COA")
    #problem.attach_logger()

    opti = alg(problem)
    print(opti)
    #logger.close()
    exit(0)
    