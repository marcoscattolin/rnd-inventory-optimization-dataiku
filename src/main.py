
import numpy as np
import pandas as pd
import itertools
from scripts.DataInit import DataInit
from scripts.VariableOptInit import VariableOptInit
from scripts.equations import first_equation, second_equation, third_equation, fourth_equation, fifth_equation, declare_objective

def insert_and_solve(shipping_df, itemsets_df, supply_nodes_df, supply_df, demand_nodes_df): 
  
  data_init = DataInit(shipping_df, itemsets_df, supply_nodes_df, supply_df, demand_nodes_df)
  data_init.check_demand()
  variable_init = VariableOptInit('SCIP', data_init)
  first_equation(variable_init, data_init)
  second_equation(variable_init, data_init)
  third_equation(variable_init, data_init)
  fourth_equation(variable_init, data_init)
  fifth_equation(variable_init, data_init)
  objective = declare_objective(variable_init, data_init)
  variable_init.solve(objective)
  assert variable_init.verify_solution() == True, 'solution not verified'
  
  
  
  objective_value = variable_init.objective_value

  itemsets_output = []

  for i in data_init.ITEMSET_IDS:
    itemsets_output.append(variable_init.get_itemset_results(i))

  procurement_output = variable_init.get_quantity_results()

  return {
      'itemsets_output' : itemsets_output,
      'procurement_output' : procurement_output,
      'objective_value' : objective_value
  }



if __name__ == "__main__":

    shipping_df = pd.DataFrame({"source_node_id":[0,0,0,1,1,1,2,2,2],  "destination_node_id":[0,1,2,0,1,2,0,1,2],  "cost":[1,10,10,10,1,10,10,10,1]})
    itemsets_df = pd.DataFrame({"itemset_id":[0,0],  "sku_id":[0,1]})
    supply_nodes_df = pd.DataFrame({"node_id":[0,1,2],"capacity":[10,10,10]})
    supply_df = pd.DataFrame({"node_id":[0,0,1,1,2,2],  "sku_id":[0,1,0,1,0,1],  "cost":[1,10,10,1,10,10], "current_quantity":[0,0,0,0,0,0]})
    demand_nodes_df = pd.DataFrame({"node_id":[0,1,2], "itemset_id":[0,0,0], "demand_mean":[5,5,5], "demand_variance":[0,0,0]}) 

    dict_to_test = insert_and_solve(shipping_df, itemsets_df, supply_nodes_df, supply_df, demand_nodes_df)

    print('UNIT TEST 1')
    print('ITEMSETS PASSED') if np.allclose(dict_to_test['itemsets_output'][0], np.array([[5, 0, 0], [0, 5, 0], [0, 0, 5]])) else print("ITEMSETS FAILED")
    print('SKUS PASSED') if np.allclose(dict_to_test['procurement_output'], np.array([[5, 5], [5, 5], [5, 5]])) else print('SKUS FAILED')
    print('OBJECTIVE VALUE PASSED') if np.allclose(dict_to_test['objective_value'], 240) else print('OBJECTIVE VALUE FAILED')






    shipping_df = pd.DataFrame({"source_node_id":[0,0,0,1,1,1,2,2,2],  "destination_node_id":[0,1,2,0,1,2,0,1,2],  "cost":[1,10,10,10,1,10,10,10,1]})
    itemsets_df = pd.DataFrame({"itemset_id":[0,0],  "sku_id":[0,1]})
    supply_nodes_df = pd.DataFrame({"node_id":[0,1,2],"capacity":[10,10,10]})
    supply_df = pd.DataFrame({"node_id":[0,0,1,1,2,2],  "sku_id":[0,1,0,1,0,1],  "cost":[1,10,10,1,10,10], "current_quantity":[5,5,5,5,5,5]})
    demand_nodes_df = pd.DataFrame({"node_id":[0,1,2], "itemset_id":[0,0,0], "demand_mean":[15,0,0], "demand_variance":[0,0,0]}) 


    dict_to_test = insert_and_solve(shipping_df, itemsets_df, supply_nodes_df, supply_df, demand_nodes_df)

    print('UNIT TEST 2')
    print('ITEMSETS PASSED') if np.allclose(dict_to_test['itemsets_output'][0], np.array([[5, 5, 5], [0, 0, 0], [0, 0, 0]])) else print("ITEMSETS FAILED")
    print('SKUS PASSED') if np.allclose(dict_to_test['procurement_output'], np.array([[0, 0], [0, 0], [0, 0]])) else print('SKUS FAILED')
    print('OBJECTIVE VALUE PASSED') if np.allclose(dict_to_test['objective_value'], 110) else print('OBJECTIVE VALUE FAILED')







    shipping_df = pd.DataFrame({"source_node_id":[0,0,0,1,1,1,2,2,2],  "destination_node_id":[0,1,2,0,1,2,0,1,2],  "cost":[1,10,10,10,1,10,10,10,1]})
    itemsets_df = pd.DataFrame({"itemset_id":[0,0],  "sku_id":[0,1]})
    supply_nodes_df = pd.DataFrame({"node_id":[0,1,2],"capacity":[10,10,10]})
    supply_df = pd.DataFrame({"node_id":[0,0,1,1,2,2],  "sku_id":[0,1,0,1,0,1],  "cost":[1,10,10,1,10,10], "current_quantity":[5,5,0,0,0,0]})
    demand_nodes_df = pd.DataFrame({"node_id":[0,1,2], "itemset_id":[0,0,0], "demand_mean":[15,0,0], "demand_variance":[0,0,0]})

    dict_to_test = insert_and_solve(shipping_df, itemsets_df, supply_nodes_df, supply_df, demand_nodes_df)

    print('UNIT TEST 3')
    print('ITEMSETS PASSED') if np.allclose(dict_to_test['itemsets_output'][0], np.array([[5, 5, 5], [0, 0, 0], [0, 0, 0]])) else print("ITEMSETS FAILED")
    print('SKUS PASSED') if np.allclose(dict_to_test['procurement_output'], np.array([[0, 0], [5, 5], [5, 5]])) else print('SKUS FAILED')
    print('OBJECTIVE VALUE PASSED') if np.allclose(dict_to_test['objective_value'], 265) else print('OBJECTIVE VALUE FAILED')



