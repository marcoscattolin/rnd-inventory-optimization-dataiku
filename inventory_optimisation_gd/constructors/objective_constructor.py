import itertools

class ObjectiveManager():
    
    def __init__(
        self,
        data,
        solver,
        variables
    ):
        self.data = data
        self.solver = solver
        self.variables = variables
        
        self.objective = self.solver.solver.Objective()
        for store, itemset in self.data.DEMAND_NODE_IDS_ITEMSET_IDS:
            for warehouse in self.data.SUPPLY_NODE_IDS:
                self.objective.SetCoefficient(
                    self.variables.x[warehouse, store, itemset], 
                    self.data.itemset_sku_id_count[itemset]*
                    self.data.shipping[warehouse, store]['cost']
                )

        for warehouse, sku in itertools.product(
            self.data.SUPPLY_NODE_IDS, self.data.SKU_IDS
        ):
            self.objective.SetCoefficient(
                self.variables.y[warehouse, sku], 
                self.data.supply[warehouse, sku]['cost']
            )

        self.objective.SetMinimization()
    
    @classmethod
    def objective_func(self):
        return self.objective
    
    def value(self):
        return self.objective.Value()