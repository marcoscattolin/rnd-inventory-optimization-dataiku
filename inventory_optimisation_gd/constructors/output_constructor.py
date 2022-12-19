import pandas as pd

class OutputManager():
    
    def __init__(
        self,
        data,
        solver,
        variables,
        objective
    ):
        self.data = data
        self.solver = solver
        self.variables = variables
        self.objective = objective
        
        self.df_wearhouse_store_qty = self.df_wearhouse_store_qty()
        self.df_wearhouse_sku_qty = self.df_wearhouse_sku_qty()
        self.df_wearhouse_sku_proc = self.df_wearhouse_sku_proc()
        self.df_wearhouse_sku_left = self.df_wearhouse_sku_left()
        self.cost = self.objective_cost()
        
    def df_wearhouse_store_qty(self):
        df_wearhouse_store_qty = pd.DataFrame(
            self.variables.x.values(), index = self.variables.x.keys(), columns=['quantity']
        )

        df_wearhouse_store_qty['quantity'] = df_wearhouse_store_qty['quantity'].apply(
            lambda x: x.SolutionValue()
        )

        df_wearhouse_store_qty = df_wearhouse_store_qty.loc[
            lambda df: df['quantity'] > 0
        ].reset_index().rename(
            {'level_0': 'wearhouses', 'level_1': 'store', 'level_2':'itemset'}, axis=1
        )
        return df_wearhouse_store_qty
    
    
    def df_wearhouse_sku_qty(self):
        df_wearhouse_sku_qty = self.df_wearhouse_store_qty.copy()
        df_wearhouse_sku_qty['sku'] = df_wearhouse_sku_qty['itemset'].\
            str.replace("[","", regex=True).str.replace("]","", regex=True).\
            str.split(', ')
        df_wearhouse_sku_qty = df_wearhouse_sku_qty.explode('sku')
        df_wearhouse_sku_qty = df_wearhouse_sku_qty.groupby(
            ['wearhouses', 'sku'], as_index=False
        )['quantity'].sum()
        return df_wearhouse_sku_qty
    
    def df_wearhouse_sku_proc(self):
        df_wearhouse_sku_proc = pd.DataFrame(
            self.variables.y.values(), index = self.variables.y.keys(), columns=['procurement_quantity']
        )

        df_wearhouse_sku_proc['procurement_quantity'] = df_wearhouse_sku_proc['procurement_quantity'].apply(
            lambda x: x.SolutionValue()
        )

        df_wearhouse_sku_proc = df_wearhouse_sku_proc.loc[
            lambda df: df['procurement_quantity'] > 0
        ].reset_index().rename(
            {'level_0': 'wearhouses', 'level_1': 'sku'}, axis=1
        )
        return df_wearhouse_sku_proc
    
    def df_wearhouse_sku_left(self):
        df_wearhouse_sku_left = pd.DataFrame(
            self.variables.v.values(), index = self.variables.v.keys(), columns=['unused_quantity']
        )

        df_wearhouse_sku_left['unused_quantity'] = df_wearhouse_sku_left['unused_quantity'].apply(
            lambda x: x.SolutionValue()
        )

        df_wearhouse_sku_left = df_wearhouse_sku_left.loc[
            lambda df: df['unused_quantity'] > 0
        ].reset_index().rename(
            {'level_0': 'wearhouses', 'level_1': 'sku'}, axis=1
        )
        return df_wearhouse_sku_left
    
    
    def objective_cost(self):
        return self.objective.value()