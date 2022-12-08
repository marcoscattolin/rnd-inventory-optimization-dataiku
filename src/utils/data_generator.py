import numpy as np
from numpy.random import multinomial
import pandas as pd
import itertools
import random
from pathlib import Path


columns_shipping = ['source_node_id', 'destination_node_id', 'cost']
columns_supply = ['node_id', 'sku_id', 'cost', 'current_quantity']
columns_demand_nodes = ['node_id', 'itemset_id', 'demand_mean', 'demand_variance']
columns_supply_nodes = ['node_id', 'capacity']
column_itemsets = ['itemset_id', 'sku_id']


##### GENERATE SHIPPING
## GRANULARITY = 1 WAREHOUSE X 1 MARKET

def generate_shipping(supply_node_number, demand_node_number, min_cost=5, max_cost=30):

  supply_node_ids = np.arange(supply_node_number)
  demand_node_ids = np.arange(demand_node_number)

  cost = np.random.randint(min_cost, max_cost, size=(supply_node_number*demand_node_number, 1))

  mat = np.array(list(itertools.product(supply_node_ids, demand_node_ids)))
  mat = np.hstack((mat, cost))


  return pd.DataFrame(mat, columns=columns_shipping)

##### GENEREATE SUPPLY NODES
## GRANULARITY = 1 WAREHOUSE

def generate_supply_nodes(node_number, capacity_min=10, capacity_max=20):
  node_ids = np.arange(node_number)
  capacity_array = np.random.randint(capacity_min, capacity_max, size=(node_number,))

  final_mat = np.vstack((node_ids, capacity_array)).T

  return pd.DataFrame(final_mat, columns=columns_supply_nodes)


##### GENERATE ITEMSETS
## GRANULARITY = 1 SKU X 1 ITEMSET

def generate_itemsets(itemset_num, sku_num, p=0.2):
  itemset_ids = np.arange(itemset_num)
  sku_ids = np.arange(sku_num)

  final_mat = list(itertools.product(itemset_ids, sku_ids))
  final_mat = np.array(random.sample(final_mat, int(len(final_mat) * p)))

  return pd.DataFrame(final_mat, columns=column_itemsets).sort_values("itemset_id").reset_index(drop=True)



##### GENERATE SUPPLY
## GRANULARITY = 1 WAREHOUSE X 1 SKU

## WORKS BUT MIGHT NEED ANOTHER WAY TO GENERATE NUMBERS OF SKUS (current_quantity)
def generate_supply(supply_nodes, itemsets, min_procurement_cost, max_procurement_cost):

  def constrained_sum_sample_pos(n, total):
    """Return a randomly chosen list of n positive integers summing to total.
    Each such list is equally likely to occur."""

    dividers = sorted(random.sample(range(0, total), n - 1))
    return [a - b for a, b in zip(dividers + [total], [0] + dividers)]




  skus = pd.DataFrame(itemsets.sku_id.unique(), columns=['sku_id'])
  skus['cost'] = np.random.randint(min_procurement_cost, max_procurement_cost, size=skus.shape)
  merged = supply_nodes.merge(skus, how='cross')
  merged['cost'] = merged['cost'] + np.random.randint(0, 8, size=merged['cost'].shape)
  merged['current_quantity'] = 0

  sku_num = itemsets.sku_id.unique().shape[0]
  node_list = merged.node_id.unique()

  for i in node_list:

    capacity_temp = merged[merged.node_id==i]['capacity'].iloc[0]
    current_storage = np.random.randint(capacity_temp)

    #### generate numbers

    #coeffs = np.random.random(size=(sku_num,))
    #get_each_sku_cap = np.round(coeffs / np.sum(coeffs) * current_storage)
    
 
    get_each_sku_cap = multinomial(current_storage, [1/sku_num] * sku_num)
   

    merged.loc[merged.node_id==i, 'current_quantity'] = get_each_sku_cap 



    assert current_storage == merged[merged.node_id==i]['current_quantity'].sum(), 'somethings wrong'


  return merged.drop(['capacity'], axis=1)

def generate_demand_nodes(demand_node_number, itemsets, min_mean_demand=5, max_mean_demand=15, min_var_demand=1, max_var_demand=4):
  ### DEMAND NODE FUNCTION

  demand_node_ids = list(np.arange(demand_node_number))
  itemset_ids = list(itemsets.itemset_id.unique())

  final_mat = np.array(list(itertools.product(demand_node_ids, itemset_ids)))

  demand_mean_array = np.random.randint(min_mean_demand, max_mean_demand, size=(final_mat.shape[0], 1))
  demand_var_array = np.round(np.random.uniform(min_var_demand, max_var_demand, size=(final_mat.shape[0], 1)), 2)

  final_mat = np.hstack((final_mat, demand_mean_array, demand_var_array))

  final_mat = pd.DataFrame(final_mat, columns=columns_demand_nodes)

  final_mat[['node_id', 'itemset_id', 'demand_mean']] =  final_mat[['node_id', 'itemset_id', 'demand_mean']].astype(int)

  return pd.DataFrame(final_mat, columns=columns_demand_nodes)

  



if __name__ == "__main__":

    ### testing


    SUPPLY_NODE_NUMBER = 3
    DEMAND_NODE_NUMBER = 7

    MIN_SHIPPING_COST = 5
    MAX_SHIPPING_COST = 10


    MIN_CAPACITY_SUPPLY_NODE = 40
    MAX_CAPACITY_SUPPLY_NODE = 100

    ITEMSET_NUMBER = 4
    SKU_NUMBER = 10

    MIN_PROCUREMENT_COST = 10
    MAX_PROCUREMENT_COST = 50

    MIN_MEAN_DEMAND = 2
    MAX_MEAN_DEMAND = 5

    MIN_VAR_DEMAND = 1
    MAX_VAR_DEMAND = 2


    ##### GENERATE DATA
    shipping = generate_shipping(SUPPLY_NODE_NUMBER, DEMAND_NODE_NUMBER, MIN_SHIPPING_COST, MAX_SHIPPING_COST)
    itemsets = generate_itemsets(ITEMSET_NUMBER, SKU_NUMBER)
    supply_nodes = generate_supply_nodes(SUPPLY_NODE_NUMBER, MIN_CAPACITY_SUPPLY_NODE, MAX_CAPACITY_SUPPLY_NODE)
    supply = generate_supply(supply_nodes, itemsets, MIN_PROCUREMENT_COST, MAX_PROCUREMENT_COST)
    demand_nodes = generate_demand_nodes(DEMAND_NODE_NUMBER, itemsets, MIN_MEAN_DEMAND, MAX_MEAN_DEMAND, MIN_VAR_DEMAND, MAX_VAR_DEMAND)


    print("Shipping size: ", shipping.shape)
    print("Itemsets size: ", itemsets.shape)
    print("Supply nodes size: ", supply_nodes.shape)
    print("Supply size: ", supply.shape)
    print("Demand nodes size: ", demand_nodes.shape)



    shipping.to_csv("data/shipping.csv", index=False)
    itemsets.to_csv("data/itemsets.csv", index=False)
    supply_nodes.to_csv("data/supply_nodes.csv", index=False)
    supply.to_csv("data/supply.csv", index=False)
    demand_nodes.to_csv("data/demand_nodes.csv", index=False)

