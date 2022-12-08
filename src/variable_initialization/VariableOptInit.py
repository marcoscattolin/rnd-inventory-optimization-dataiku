import numpy as np
import pandas as pd
import itertools
from ortools.linear_solver import pywraplp

def get_solver(solver_name='SCIP'):
  solver = pywraplp.Solver.CreateSolver(solver_name)
  if not solver:
      return None
  
  return solver


class VariableOptInit():

  def __init__(self, solver_name, data):

    self.solver = get_solver(solver_name)
    self.x = {}
    self.y = {}
    self.z = {}
    self.v = {}
    self.status = np.nan
    self.objective_value = np.nan

    SUPPLY_NODE_IDS = data.SUPPLY_NODE_IDS
    DEMAND_NODE_IDS = data.DEMAND_NODE_IDS
    ITEMSET_IDS = data.ITEMSET_IDS
    SKU_IDS = data.SKU_IDS


    SUPPLY_NODE_NUMBER_CONST = data.SUPPLY_NODE_NUMBER_CONST
    DEMAND_NODE_NUMBER_CONST = data.DEMAND_NODE_NUMBER_CONST
    ITEMSET_NUMBER_CONST = data.ITEMSET_NUMBER_CONST
    SKU_NUMBER_CONST = data.SKU_NUMBER_CONST


    infinity = self.solver.infinity()

    for i, j, k in itertools.product(SUPPLY_NODE_IDS, DEMAND_NODE_IDS, ITEMSET_IDS):
      self.x[i, j, k] = self.solver.IntVar(0, infinity, f'x[{i}][{j}][{k}]')
      self.z[i, j, k] = self.solver.NumVar(0, 1, f'z[{i}][{j}][{k}]')

    for i, r in itertools.product(SUPPLY_NODE_IDS, SKU_IDS):
      self.y[i, r] = self.solver.IntVar(0, infinity, f'y[{i}][{r}]')
      self.v[i, r] = self.solver.IntVar(0, infinity, f'v[{i}][{r}]')


  def verify_solution(self, eps=1e-4):
    return self.solver.VerifySolution(eps, True)


  def get_variable_number(self):
    return self.solver.NumVariables()


  def solve(self, objective):
    self.status = self.solver.Solve()
    self.objective_value = objective.Value()
    return self.status


  def get_itemset_results(self, itemset_id):

    if self.status == pywraplp.Solver.OPTIMAL:
      temp_dict = {(key[0],key[1]): val.solution_value() for (key, val) in self.x.items() if key[2]==itemset_id}

      output_x = pd.DataFrame(temp_dict.values(), index=temp_dict.keys()).reset_index()

      return output_x.set_index(['level_0', 'level_1']).unstack().transform(np.abs).to_numpy().T

    return 0


  def get_quantity_results(self):
    if self.status == pywraplp.Solver.OPTIMAL:
      output_y = {key:val.solution_value() for (key, val) in self.y.items()}
      output_y = pd.DataFrame(output_y.values(), index=output_y.keys()).reset_index()

      return output_y.set_index(['level_0', 'level_1']).unstack().transform(np.abs).to_numpy()

    return 0