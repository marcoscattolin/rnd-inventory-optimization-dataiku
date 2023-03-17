import pandas as pd

class OutputManager():
    
    def __init__(
        self,
        data,
        solver,
        variables,
        objective
    ):
        # define object of class
        self.data = data
        self.solver = solver
        self.variables = variables
        self.objective = objective
        
        # extract column names
        self.demand_node_name = self.data.demand_schema['col_demand_demand_node_id']
        self.supply_node_name = self.data.supply_schema['col_supply_supply_node_id']
        self.sku_name = self.data.itemset_sku_schema['col_itemsets_sku_id']
        self.itemset_name = self.data.itemset_sku_schema['col_itemsets_itemset_id']
        self.quantity = self.data.config['schema']['output_column']['quantity']
        self.procurement_quantity = self.data.config['schema']['output_column']['procurement_quantity']
        self.unused_quantity = self.data.config['schema']['output_column']['unused_quantity']

        # call methods
        self.df_warehouse_store_qty = self.df_warehouse_store_qty()
        self.df_warehouse_sku_qty = self.df_warehouse_sku_qty()
        self.df_warehouse_sku_proc = self.df_warehouse_sku_proc()
        self.df_warehouse_sku_left = self.df_warehouse_sku_left()
        self.cost = self.objective_cost()
        
    def df_warehouse_store_qty(self):
        df_warehouse_store_qty = pd.DataFrame(
            self.variables.x.values(), index = self.variables.x.keys(), columns=[self.quantity]
        )

        df_warehouse_store_qty[self.quantity] = df_warehouse_store_qty[self.quantity].apply(
            lambda x: x.SolutionValue()
        )

        df_warehouse_store_qty = df_warehouse_store_qty.loc[
            lambda df: df[self.quantity] > 0
        ].reset_index().rename(
            {
                'level_0': self.supply_node_name, 
                'level_1': self.demand_node_name, 
                'level_2': self.itemset_name
            }, axis=1
        )
        return df_warehouse_store_qty
    
    
    def df_warehouse_sku_qty(self):
        df_warehouse_sku_qty = self.df_warehouse_store_qty.copy()
        df_warehouse_sku_qty[self.sku_name] = df_warehouse_sku_qty[self.itemset_name].\
            str.replace("[","", regex=True).str.replace("]","", regex=True).\
            str.split(', ')
        df_warehouse_sku_qty = df_warehouse_sku_qty.explode(self.sku_name)
        df_warehouse_sku_qty = df_warehouse_sku_qty.groupby(
            [self.supply_node_name, self.sku_name], as_index=False
        )[self.quantity].sum()
        return df_warehouse_sku_qty
    
    def df_warehouse_sku_proc(self):
        df_warehouse_sku_proc = pd.DataFrame(
            self.variables.y.values(), index = self.variables.y.keys(), columns=[self.procurement_quantity]
        )

        df_warehouse_sku_proc[self.procurement_quantity] = df_warehouse_sku_proc[self.procurement_quantity].apply(
            lambda x: x.SolutionValue()
        )

        df_warehouse_sku_proc = df_warehouse_sku_proc.loc[
            lambda df: df[self.procurement_quantity] > 0
        ].reset_index().rename(
            {'level_0': self.supply_node_name, 'level_1': self.sku_name}, axis=1
        )
        return df_warehouse_sku_proc
    
    def df_warehouse_sku_left(self):
        df_warehouse_sku_left = pd.DataFrame(
            self.variables.v.values(), index = self.variables.v.keys(), columns=[self.unused_quantity]
        )

        df_warehouse_sku_left[self.unused_quantity] = df_warehouse_sku_left[self.unused_quantity].apply(
            lambda x: x.SolutionValue()
        )

        df_warehouse_sku_left = df_warehouse_sku_left.loc[
            lambda df: df[self.unused_quantity] > 0
        ].reset_index().rename(
            {'level_0': self.supply_node_name, 'level_1': self.sku_name}, axis=1
        )
        return df_warehouse_sku_left
    
    
    def objective_cost(self):
        return self.objective.value()