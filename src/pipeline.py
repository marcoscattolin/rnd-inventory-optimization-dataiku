from .data_initialization import DataInit
from .variable_initialization import VariableOptInit
from . import constraints
from . import objective_function



def insert_solve(shipping_df, itemsets_df, supply_nodes_df, supply_df, demand_nodes_df): 
  
  data_init = DataInit(shipping_df, itemsets_df, supply_nodes_df, supply_df, demand_nodes_df)
  data_init.check_demand()
  variable_init = VariableOptInit('SCIP', data_init)
  constraints.first_equation(variable_init, data_init)
  constraints.second_equation(variable_init, data_init)
  constraints.third_equation(variable_init, data_init)
  constraints.fourth_equation(variable_init, data_init)
  constraints.fifth_equation(variable_init, data_init)
  objective = objective_function.declare_objective(variable_init, data_init)
  variable_init.solve(objective)
  assert variable_init.verify_solution() == True, 'solution not verified'
  
  
  
  objective_value = variable_init.objective_value

  itemsets_output = {}

  for i in data_init.ITEMSET_IDS:
    itemsets_output[i] = variable_init.get_itemset_results(i)

  procurement_output = variable_init.get_quantity_results()

  return {
      'itemsets_output' : itemsets_output,
      'procurement_output' : procurement_output,
      'supply_node_ids': data_init.SUPPLY_NODE_IDS,
      'demand_node_ids': data_init.DEMAND_NODE_IDS,
      'sku_ids' : data_init.SKU_IDS,
      'objective_value' : objective_value
  }