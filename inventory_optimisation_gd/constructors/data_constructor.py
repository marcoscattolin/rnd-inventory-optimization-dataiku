import itertools

class DataManager():

    def __init__(self, shipping_df, itemsets_df, supply_nodes_df, supply_df, demand_nodes_df):

        self.DEMAND_NODE_IDS_ITEMSET_IDS = demand_nodes_df.loc[
                lambda df: df['demand_mean'] > 0, ['node_id' , 'itemset_id']
            ].astype(str).drop_duplicates().values
        self.SUPPLY_NODE_IDS = list(supply_nodes_df.node_id.unique())
        self.DEMAND_NODE_IDS = list(demand_nodes_df.node_id.unique())
        self.ITEMSET_IDS = list(itemsets_df.itemset_id.unique())
        self.SKU_IDS = list(itemsets_df.sku_id.unique())

        # STORE, WAREHOUSE -> COST
        self.shipping = shipping_df.set_index(['source_node_id', 'destination_node_id']).to_dict('index')

        # WAREHOUSE -> CAPACITY
        self.supply_nodes = supply_nodes_df.set_index('node_id').to_dict('index')

        # WAREHOUSE, SKU -> QUANTITY
        self.supply = supply_df.set_index(['node_id', 'sku_id']).to_dict('index')

        # SKU -> ITEMSET
        self.query_itemsets_by_sku = {}
        for itemset, sku in itemsets_df.values:
            self.query_itemsets_by_sku[sku] = self.query_itemsets_by_sku.get(sku, []) + [itemset]

        # ITEMSET -> STORE
        self.query_stores_by_itemset = {}
        for store, itemset in self.DEMAND_NODE_IDS_ITEMSET_IDS:
            self.query_stores_by_itemset[itemset] = self.query_stores_by_itemset.get(itemset, []) + [store]

        # STORE, ITEMSET -> DEMAND 
        self.demand_nodes = demand_nodes_df.set_index(['node_id', 'itemset_id']).to_dict('index')

        # ITEMSET -> NUM OF SKUS
        self.itemset_sku_id_count = itemsets_df.groupby(['itemset_id'])['itemset_id'].count().to_dict()

        self.itemsets = list(itemsets_df.itertuples(index=False, name=None))

    
    def check_demand(self):
        itemsets_ids_temp = [temp[0] for temp in self.itemsets]
        capacity_arr_temp = [self.supply_nodes[key]['capacity'] for key in self.supply_nodes.keys()]

        demand_array = []

        for j,k in itertools.product(self.DEMAND_NODE_IDS, itemsets_ids_temp):
            demand_array.append(self.demand_nodes[j, k]['demand_mean'])

        assert sum(capacity_arr_temp) >= sum(demand_array), "Demand has to be less than capacity"