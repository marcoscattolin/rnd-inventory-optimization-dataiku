import itertools

class ConstraintManager():

    
    def __init__(
        self,
        data,
        solver,
        variables
    ):
        self.data = data
        self.solver = solver
        self.variables = variables
        self.infinity = self.solver.infinity
        
        self.first_equation()
        self.second_equation()
        self.third_equation()
        self.fourth_equation()
    
    
    def first_equation(self):
        
        for store, itemset in self.data.DEMAND_NODE_IDS_ITEMSET_IDS:
            constraint = self.solver.solver.RowConstraint(
                self.data.demand_nodes[store, itemset]['demand_mean'], 
                self.infinity, 
                f'equation 1 ({store}, {itemset}): \
                number of demand itemset {itemset} at store {store}'
            )
            for warehouse in self.data.SUPPLY_NODE_IDS:
                constraint.SetCoefficient(
                    self.variables.x[warehouse, store, itemset], 1)

                
    def second_equation(self):
        
        for warehouse, sku in itertools.product(
            self.data.SUPPLY_NODE_IDS, self.data.SKU_IDS):
            constraint = self.solver.solver.RowConstraint(
                -self.infinity, 
                self.data.supply[warehouse, sku]['current_quantity'], 
                f'equation 2 ({warehouse}, {sku}): number of procurement of \
                {sku} sku at {warehouse} warehouse'
            )

            for itemset in self.data.query_itemsets_by_sku[sku]:
                try:
                    for store in self.data.query_stores_by_itemset[itemset]:
                        constraint.SetCoefficient(
                            self.variables.x[warehouse, store, itemset], 1)
                except:
                    pass

            constraint.SetCoefficient(self.variables.y[warehouse, sku], -1)

            
    def third_equation(self):

        for warehouse, sku in itertools.product(
            self.data.SUPPLY_NODE_IDS, self.data.SKU_IDS):
            constraint = self.solver.solver.RowConstraint(
                
                self.data.supply[warehouse, sku]['current_quantity'], 
                self.infinity, 
                f'equation 3 ({warehouse}, {sku}): number of unused {sku} sku \
                at {warehouse} warehouse'
            )

            for itemset in self.data.query_itemsets_by_sku[sku]:
                try:
                    for store in self.data.query_stores_by_itemset[itemset]:
                        constraint.SetCoefficient(
                            self.variables.x[warehouse, store, itemset], 1)
                except:
                    pass
            constraint.SetCoefficient(self.variables.v[warehouse, sku], 1)


    def fourth_equation(self):

        for warehouse in self.data.SUPPLY_NODE_IDS:
            constraint = self.solver.solver.RowConstraint(
                -self.infinity, 
                self.data.supply_nodes[warehouse]['capacity'],
                f'equation 4 ({warehouse}): capacity at {warehouse} warehouse'
            )

            for store, itemset in self.data.DEMAND_NODE_IDS_ITEMSET_IDS:
                constraint.SetCoefficient(
                    self.variables.x[warehouse, store, itemset], 
                    self.data.itemset_sku_id_count[itemset]
                )

            for sku in self.data.SKU_IDS:
                constraint.SetCoefficient(self.variables.v[warehouse, sku], 1)

