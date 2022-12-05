import itertools


def first_equation(variable_init, data_init):
  for j, k in itertools.product(data_init.DEMAND_NODE_IDS, data_init.ITEMSET_IDS):
      constraint = variable_init.solver.RowConstraint(1, 1, f'equation 1: (j, k) = ({j}, {k})')
      for i in data_init.SUPPLY_NODE_IDS:
        constraint.SetCoefficient(variable_init.z[i, j, k], 1)



#######################
#######################

def second_equation(variable_init, data_init):

  infinity = variable_init.solver.infinity()


  for i, j, k in itertools.product(data_init.SUPPLY_NODE_IDS, data_init.DEMAND_NODE_IDS, data_init.ITEMSET_IDS):
    
    constraint = variable_init.solver.RowConstraint(-infinity, 0, f'equation 2: z({i},{j},{k})')
    constraint.SetCoefficient(variable_init.z[i, j, k], data_init.demand_nodes[j, k]['demand'])
    constraint.SetCoefficient(variable_init.x[i, j, k], -1)




#######################
#######################


def third_equation(variable_init, data_init):

  infinity = variable_init.solver.infinity()
  
  
  for i, r in itertools.product(data_init.SUPPLY_NODE_IDS, data_init.SKU_IDS):
    constraint = variable_init.solver.RowConstraint(-infinity, data_init.supply[i, r]['current_quantity'], 'equation 3:')

    for j, k in itertools.product(data_init.DEMAND_NODE_IDS, data_init.ITEMSET_IDS):
      if (k, r) in data_init.itemsets:
        constraint.SetCoefficient(variable_init.x[i, j, k], 1)

    constraint.SetCoefficient(variable_init.y[i, r], -1)



#######################
#######################


def fourth_equation(variable_init, data_init):

  infinity = variable_init.solver.infinity()

  for i, r in itertools.product(data_init.SUPPLY_NODE_IDS, data_init.SKU_IDS):
    constraint = variable_init.solver.RowConstraint(-infinity, -data_init.supply[i, r]['current_quantity'], 'equation 4:')

    for j, k in itertools.product(data_init.DEMAND_NODE_IDS, data_init.ITEMSET_IDS):
      if (k, r) in data_init.itemsets:
        constraint.SetCoefficient(variable_init.x[i, j, k], -1)

    constraint.SetCoefficient(variable_init.v[i, r], -1)




#######################
#######################


def fifth_equation(variable_init, data_init):

  infinity = variable_init.solver.infinity()

  for i in data_init.SUPPLY_NODE_IDS:

    constraint = variable_init.solver.RowConstraint(-infinity, data_init.supply_nodes[i]['capacity'])

    for j, k in itertools.product(data_init.DEMAND_NODE_IDS, data_init.ITEMSET_IDS):
      constraint.SetCoefficient(variable_init.x[i, j, k], data_init.itemset_sku_id_count[k])

    for r in data_init.SKU_IDS:
      constraint.SetCoefficient(variable_init.v[i, r], 1)



#######################
#######################


def declare_objective(variable_init, data_init):

  objective = variable_init.solver.Objective()

  for i, j, k in itertools.product(data_init.SUPPLY_NODE_IDS, data_init.DEMAND_NODE_IDS, data_init.ITEMSET_IDS):
    objective.SetCoefficient(variable_init.x[i, j, k], data_init.itemset_sku_id_count[k]*data_init.shipping[i, j]['cost'])

  for i, r in itertools.product(data_init.SUPPLY_NODE_IDS, data_init.SKU_IDS):
    objective.SetCoefficient(variable_init.y[i, r], data_init.supply[i, r]['cost'])

  objective.SetMinimization()

  return objective


#######################
#######################
