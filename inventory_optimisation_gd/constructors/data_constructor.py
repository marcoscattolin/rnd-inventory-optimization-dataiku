import itertools

class DataManager():

    def __init__(
        self, 
        shipping_df, 
        itemsets_df, 
        supply_nodes_df, 
        supply_df, 
        demand_nodes_df, 
        config
    ):

        self.config = config
        self.demand_schema = self.config['schema']['demand_file']
        self.supply_nodes_schema = self.config['schema']['capacity_file']
        self.itemset_sku_schema = self.config['schema']['itemset_file']

        self.DEMAND_NODE_IDS_ITEMSET_IDS = demand_nodes_df.loc[
                lambda df: df[self.demand_schema['col_demand_demand_mean']] > 0, [
                    self.demand_schema['col_demand_demand_node_id'] , 
                    self.demand_schema['col_demand_itemset_id']
            ]
            ].astype(str).drop_duplicates().values


        self.SUPPLY_NODE_IDS = list(supply_nodes_df[
            self.supply_nodes_schema['col_capacity_supply_node_id']
        ].unique())
        self.DEMAND_NODE_IDS = list(demand_nodes_df[
            self.demand_schema['col_demand_demand_node_id']
        ].unique())

        self.ITEMSET_IDS = list(itemsets_df[
            self.itemset_sku_schema['col_itemsets_itemset_id']
        ].unique())
        self.SKU_IDS = list(itemsets_df[
            self.itemset_sku_schema['col_itemsets_sku_id']
        ].unique())

        # STORE, WAREHOUSE -> COST
        self.shipping_schema = self.config['schema']['shipping_file']
        self.shipping = shipping_df.set_index(
            [
                self.shipping_schema['col_shipping_source_node_id'], 
                self.shipping_schema['col_shipping_destination_node_id']
            ]
        ).to_dict('index')

        # WAREHOUSE -> CAPACITY
        self.supply_nodes = supply_nodes_df.set_index(
            self.supply_nodes_schema['col_capacity_supply_node_id']
        ).to_dict('index')

        # WAREHOUSE, SKU -> QUANTITY
        self.supply_schema = self.config['schema']['supply_file']
        self.supply = supply_df.set_index(
            [
                self.supply_schema['col_supply_supply_node_id'], 
                self.supply_schema['col_supply_sku_id']
            ]
        ).to_dict('index')

        # SKU -> ITEMSET
        self.query_itemsets_by_sku = {}
        for itemset, sku in itemsets_df.values:
            self.query_itemsets_by_sku[sku] = self.query_itemsets_by_sku.get(sku, []) + [itemset]

        # ITEMSET -> STORE
        self.query_stores_by_itemset = {}
        for store, itemset in self.DEMAND_NODE_IDS_ITEMSET_IDS:
            self.query_stores_by_itemset[itemset] = self.query_stores_by_itemset.get(itemset, []) + [store]

        # STORE, ITEMSET -> DEMAND 
        self.demand_nodes = demand_nodes_df.set_index(
            [
                self.demand_schema['col_demand_demand_node_id'], 
                self.demand_schema['col_demand_itemset_id']
            ]
        ).to_dict('index')


        # ITEMSET -> NUM OF SKUS
        self.itemset_sku_id_count = itemsets_df.groupby(
            [
                self.itemset_sku_schema['col_itemsets_itemset_id']
            ]
            )[self.itemset_sku_schema['col_itemsets_itemset_id']].count().to_dict()

        self.itemsets = list(itemsets_df.itertuples(index=False, name=None))

    
    def check_demand(self):
        itemsets_ids_temp = [temp[0] for temp in self.itemsets]
        capacity_arr_temp = [self.supply_nodes[key][
            self.supply_nodes_schema['col_capacity_capacity']
            ] for key in self.supply_nodes.keys()]

        demand_array = []

        for j,k in itertools.product(self.DEMAND_NODE_IDS, itemsets_ids_temp):
            demand_array.append(self.demand_nodes[j, k][
                self.demand_schema['col_demand_demand_mean']
            ])

        assert sum(capacity_arr_temp) >= sum(demand_array), "Demand has to be less than capacity"