import itertools

class ConstraintManager():

    
    def __init__(
        self,
        data,
        solver,
        variables,
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
        
        # la somma delle spedizioni dai warehouse è maggiore o uguale alla domanda in ogni store, itemset
        for store, itemset in self.data.DEMAND_NODE_IDS_ITEMSET_IDS:
            constraint = self.solver.solver.RowConstraint(
                self.data.demand_nodes[store, itemset][
                    self.data.demand_schema['col_demand_demand_mean']
                ], 
                self.infinity, 
                f'equation 1 ({store}, {itemset}): \
                number of demand itemset {itemset} at store {store}'
            )
            # per ogni (store, itemset, warehouse) creo una variabile decisonale con coefficiente 1 che varrà la quantità di itemset da spedire
            for warehouse in self.data.SUPPLY_NODE_IDS:
                constraint.SetCoefficient(
                    self.variables.x[warehouse, store, itemset], 1)

                
    def second_equation(self):

        # per ogni warehouse, sku: la somma delle spedizioni meno ciò che ho in magazzino (ie. fabbisogno) è minore o uguale a variabile decisionale y (ie. ciò che devo acquistare procurement)
        for warehouse, sku in itertools.product(
            self.data.SUPPLY_NODE_IDS, self.data.SKU_IDS):
            constraint = self.solver.solver.RowConstraint(
                -self.infinity, 
                self.data.supply[warehouse, sku][
                    self.data.supply_schema['col_supply_current_quantity']
                    ], 
                f'equation 2 ({warehouse}, {sku}): number of procurement of \
                {sku} sku at {warehouse} warehouse'
            )
            # TODO unclear
            for itemset in self.data.query_itemsets_by_sku[sku]:
                try:
                    for store in self.data.query_stores_by_itemset[itemset]:
                        constraint.SetCoefficient(
                            self.variables.x[warehouse, store, itemset], 1)
                except:
                    pass

            constraint.SetCoefficient(self.variables.y[warehouse, sku], -1)

            
    def third_equation(self):

        # per ogni warehouse, sku: la somma di ciò che ho in magazzino meno ciò che spedisco è minore o uguale a variabile decisionale v (ie. ciò che resta in magazzino)
        for warehouse, sku in itertools.product(
            self.data.SUPPLY_NODE_IDS, self.data.SKU_IDS):
            constraint = self.solver.solver.RowConstraint(
                
                self.data.supply[warehouse, sku][
                    self.data.supply_schema['col_supply_current_quantity']
                ], 
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

        # per ogni magazzino la somma di ciò che spedisco + ciò che mi rimane non supera la capacity
        for warehouse in self.data.SUPPLY_NODE_IDS:
            constraint = self.solver.solver.RowConstraint(
                -self.infinity, 
                self.data.supply_nodes[warehouse][
                    self.data.supply_nodes_schema['col_capacity_capacity']
                    ],
                f'equation 4 ({warehouse}): capacity at {warehouse} warehouse'
            )

            for store, itemset in self.data.DEMAND_NODE_IDS_ITEMSET_IDS:
                constraint.SetCoefficient(
                    self.variables.x[warehouse, store, itemset], 
                    self.data.itemset_sku_id_count[itemset]
                )

            for sku in self.data.SKU_IDS:
                constraint.SetCoefficient(self.variables.v[warehouse, sku], 1)

