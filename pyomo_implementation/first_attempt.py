import pandas as pd
import os
import sys
import yaml
from pathlib import Path
from inventory_optimisation_gd.constructors.data_constructor import DataManager
from pyomo.environ import Objective, ConcreteModel, Var, SolverFactory, Constraint, minimize, NonNegativeIntegers, NonPositiveIntegers, value


def load_data():

    dir_path = Path(__file__).parent.parent
    dir_path = os.path.join(dir_path, 'inventory_optimisation_gd')
    sys.path.insert(0, os.path.dirname(dir_path))

    with open(os.path.join(dir_path, 'config', 'solver.yaml')) as file:
        solver_config = yaml.safe_load(file)

    with open(os.path.join(dir_path, 'config', 'schema.yaml')) as file:
        schema_config = yaml.safe_load(file)

    config = {
        'solver': solver_config,
        'schema': schema_config
    }

    path = os.path.join(
            os.path.abspath(
                os.path.join(dir_path, os.pardir)
                ),
            'data'
        )

    shipping_cost = pd.read_csv(os.path.join(path, schema_config['shipping_file']['file_name']))
    itemset = pd.read_csv(os.path.join(path, schema_config['itemset_file']['file_name']))
    capacity = pd.read_csv(os.path.join(path, schema_config['capacity_file']['file_name']))
    supply = pd.read_csv(os.path.join(path, schema_config['supply_file']['file_name']))
    demand = pd.read_csv(os.path.join(path, schema_config['demand_file']['file_name']))

    data_init = DataManager(shipping_df=shipping_cost, itemsets_df=itemset, supply_nodes_df=capacity, supply_df=supply, demand_nodes_df=demand, config=config)

    return data_init


def init_model(data):

    print("Initializing model")

    model = ConcreteModel()

    # unpack model
    demand_ids = data.DEMAND_NODE_IDS
    itemset_ids = data.ITEMSET_IDS
    supply_ids = data.SUPPLY_NODE_IDS
    sku_ids = data.SKU_IDS
    itemset_sku_id_count = data.itemset_sku_id_count

    shipping_cost = {}
    for key, value in data.shipping.items():
        shipping_cost[key] = value['product_shipping_cost']

    procurement_cost = {}
    q = {}
    for key, value in data.supply.items():
        procurement_cost[key] = value['product_unit_procurement_cost']
        q[key] = value['product_stock_in_warehouses']

    model.x = Var(supply_ids, demand_ids, itemset_ids, within=NonNegativeIntegers)
    model.y = Var(supply_ids, sku_ids, within=NonNegativeIntegers)
    model.v = Var(supply_ids, sku_ids, within=NonNegativeIntegers)
    # define the objective function
    model.value = Objective(expr=sum((model.x[(i, j, k)] * shipping_cost[(i, j)] * itemset_sku_id_count[k]) for i in supply_ids for j in demand_ids for k in itemset_ids) + sum(model.y[(i, r)] * procurement_cost[(i, r)] for i in supply_ids for r in sku_ids), sense=minimize)

    def eq0(m, i, r):
        return m.v[(i, r)] == q[(i, r)] + m.y[(i, r)] - sum(m.x[(i, j, k)] * itemset_sku_id_count[k] for j in demand_ids for k in data.query_itemsets_by_sku[r])
    model.eq0 = Constraint(supply_ids, sku_ids, rule=eq0)

    def eq1(m, j, k):
        return sum(m.x[(i, j, k)] for i in supply_ids) <= data.demand_nodes[(j, k)]['demand_mean']
    model.eq1 = Constraint(demand_ids, itemset_ids, rule=eq1)

    def eq2(m, r, i):
        return sum(m.x[(i, j, k)] * itemset_sku_id_count[k] for j in demand_ids for k in data.query_itemsets_by_sku[r]) - q[(i, r)] <= m.y[(i, r)]
    model.eq2 = Constraint(sku_ids, supply_ids, rule=eq2)

    def eq3(m, r, i):
        return q[(i, r)] - sum(m.x[(i, j, k)] * itemset_sku_id_count[k] for j in demand_ids for k in data.query_itemsets_by_sku[r]) <= m.v[(i, r)]
    model.eq3 = Constraint(sku_ids, supply_ids, rule=eq3)

    def eq4(m, i):
        return sum(model.x[(i, j, k)] * itemset_sku_id_count[k] for j in demand_ids for k in itemset_ids) + sum(m.v[(i, r)] for r in sku_ids) <= data.supply_nodes[i]['location_capacity']
    model.eq4 = Constraint(supply_ids, rule=eq4)

    print("Done!")

    return model


data = load_data()
model = init_model(data)
print("Solving")
solution = SolverFactory('glpk').solve(model)
print("Done!")
