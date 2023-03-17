import numpy as np
from ortools.linear_solver import pywraplp

class SolverManager():

    def __init__(
        self,
        solver_name='SCIP', 
        mip_gap=0.05,
        verbose=True
    ):
        self.solver = pywraplp.Solver.CreateSolver(solver_name)
        #solver.set_time_limit(1000) 
        if not self.solver:
            raise TypeError('Solver is NoneType')
            
        if verbose:
            self.solver.EnableOutput()
        
        self.mip_gap = mip_gap
        self.status = np.nan
        self.infinity = self.solver.infinity()


    def verify_solution(self, eps=1e-4):
        return self.solver.VerifySolution(eps, True)


    def solve(self):
        solverParams = pywraplp.MPSolverParameters()
        solverParams.SetDoubleParam(solverParams.RELATIVE_MIP_GAP, self.mip_gap)
        self.status = self.solver.Solve(solverParams)
        return self.status