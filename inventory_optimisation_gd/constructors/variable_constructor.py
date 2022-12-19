import itertools

class VariableManager():

    def __init__(
        self,
        data,
        solver
    ):
        self.data = data
        self.solver = solver
        self.infinity = self.solver.infinity
        
        self.x = self.x()
        self.y = self.y()
        self.v = self.v()
    
    def x(self):
        x = {}
        for j, k in self.data.DEMAND_NODE_IDS_ITEMSET_IDS:
            for i in self.data.SUPPLY_NODE_IDS:
                x[i, j, k] = self.solver.solver.IntVar(0, self.infinity, f'x[{i}][{j}][{k}]')
        return x
    
    def y(self):
        y = {}
        for i, r in itertools.product(self.data.SUPPLY_NODE_IDS, self.data.SKU_IDS):
            y[i, r] = self.solver.solver.IntVar(0, self.infinity, f'y[{i}][{r}]')
        return y
    
    def v(self):
        v = {}
        for i, r in itertools.product(self.data.SUPPLY_NODE_IDS, self.data.SKU_IDS):
            v[i, r] = self.solver.solver.IntVar(0, self.infinity, f'v[{i}][{r}]')
        return v
    
    def get_variable_number(self):
        return self.solver.NumVariables()