import itertools
import numpy as np

def help_fun(x):
  return int(abs(np.random.normal(loc=x['demand_mean'], scale=x['demand_variance'])))

class DataInit():

  def __init__(self, shipping_df, itemsets_df, supply_nodes_df, supply_df, demand_nodes_df):

    self.shipping = shipping_df.set_index(['source_node_id', 'destination_node_id']).to_dict('index')
    self.itemsets = list(itemsets_df.itertuples(index=False, name=None))
    self.supply_nodes = supply_nodes_df.set_index('node_id').to_dict('index')
    self.supply = supply_df.set_index(['node_id', 'sku_id']).to_dict('index')



    demand_nodes_df['demand'] = demand_nodes_df[['demand_mean', 'demand_variance']].apply(help_fun, axis=1)
    self.demand_nodes = demand_nodes_df.set_index(['node_id', 'itemset_id']).to_dict('index')


    self.itemset_sku_id_count = itemsets_df.groupby(['itemset_id'])['itemset_id'].count().to_dict()



    self.SUPPLY_NODE_IDS = list(supply_nodes_df.node_id.unique())
    self.DEMAND_NODE_IDS = list(demand_nodes_df.node_id.unique())
    self.ITEMSET_IDS = list(itemsets_df.itemset_id.unique())
    self.SKU_IDS = list(itemsets_df.sku_id.unique())


    self.SUPPLY_NODE_NUMBER_CONST = len(self.SUPPLY_NODE_IDS)
    self.DEMAND_NODE_NUMBER_CONST = len(self.DEMAND_NODE_IDS)
    self.ITEMSET_NUMBER_CONST = len(self.ITEMSET_IDS)
    self.SKU_NUMBER_CONST = len(self.SKU_IDS)


    


  def check_demand(self):
    itemsets_ids_temp = [temp[0] for temp in self.itemsets]
    capacity_arr_temp = [self.supply_nodes[key]['capacity'] for key in self.supply_nodes.keys()]

    demand_array = []

    for j,k in itertools.product(self.DEMAND_NODE_IDS, itemsets_ids_temp):
      demand_array.append(self.demand_nodes[j, k]['demand'])

    assert sum(capacity_arr_temp) >= sum(demand_array), "Demand has to be less than capacity"