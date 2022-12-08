import itertools


def declare_objective(variable_init, data_init):

  objective = variable_init.solver.Objective()

  for i, j, k in itertools.product(data_init.SUPPLY_NODE_IDS, data_init.DEMAND_NODE_IDS, data_init.ITEMSET_IDS):
    objective.SetCoefficient(variable_init.x[i, j, k], data_init.itemset_sku_id_count[k]*data_init.shipping[i, j]['cost'])

  for i, r in itertools.product(data_init.SUPPLY_NODE_IDS, data_init.SKU_IDS):
    objective.SetCoefficient(variable_init.y[i, r], data_init.supply[i, r]['cost'])

  objective.SetMinimization()

  return objective
