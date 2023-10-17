import pandas as pd
import os
import sys
import yaml
from pathlib import Path
from inventory_optimisation_gd.constructors.data_constructor import DataManager
from pyomo.environ import Objective, ConcreteModel, Var, SolverFactory, Constraint, minimize, NonNegativeIntegers, NonPositiveIntegers, value, Set


def load_data():

    print("Loading data...")
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

    print("Done!")

    return data_init


def init_model(data):

    print("Initializing model...")

    model = ConcreteModel()
    model.warehouses = Set(initialize=data.SUPPLY_NODE_IDS)
    model.stores = Set(initialize=data.DEMAND_NODE_IDS)
    model.itemsets = Set(initialize=data.ITEMSET_IDS)
    model.skus = Set(initialize=data.SKU_IDS)
    model.store_itemsets = Set(initialize=[(i, j) for i, j in data.DEMAND_NODE_IDS_ITEMSET_IDS])


    shipping_cost = {}
    for key, value in data.shipping.items():
        shipping_cost[key] = value['product_shipping_cost']

    procurement_cost = {}
    q = {}
    for key, value in data.supply.items():
        procurement_cost[key] = value['product_unit_procurement_cost']
        q[key] = value['product_stock_in_warehouses']

    demand = {}
    for key, value in data.demand_nodes.items():
        demand[key] = value['demand_mean']

    itemset_sku_id_count = data.itemset_sku_id_count

    capacity = {}
    for key, val in data.supply_nodes.items():
        capacity[key] = val['location_capacity']

    # variables
    model.x = Var(model.warehouses, model.store_itemsets, within=NonNegativeIntegers)
    model.y = Var(data.SUPPLY_NODE_IDS, data.SKU_IDS, within=NonNegativeIntegers)
    model.v = Var(data.SUPPLY_NODE_IDS, data.SKU_IDS, within=NonNegativeIntegers)

    # objective function
    model.value = Objective(expr=sum((model.x[(i, j, k)] * shipping_cost[(i, j)] * itemset_sku_id_count[k]) for i in model.warehouses for j, k in model.store_itemsets) + sum(model.y[(i, r)] * procurement_cost[(i, r)] for i in model.warehouses for r in model.skus), sense=minimize)

    # constraints
    def eq1(m, j, k):
        return sum(m.x[(i, j, k)] for i in model.warehouses) >= demand[(j, k)]
    model.eq1 = Constraint(model.store_itemsets, rule=eq1)

    def eq2(m, r, i):
        return sum(m.x[(i, j, k)] * itemset_sku_id_count[k] for j, k in model.store_itemsets) - q[(i, r)] <= m.y[(i, r)]
    model.eq2 = Constraint(model.skus, model.warehouses, rule=eq2)

    def eq3(m, r, i):
        return q[(i, r)] - sum(m.x[(i, j, k)] * itemset_sku_id_count[k] for j, k in model.store_itemsets) <= m.v[(i, r)]
    model.eq3 = Constraint(model.skus, model.warehouses, rule=eq3)

    def eq4(m, i):
        return sum(model.x[(i, j, k)] * itemset_sku_id_count[k] for j, k in model.store_itemsets) + sum(m.v[(i, r)] for r in model.skus) <= capacity[i]
    model.eq4 = Constraint(data.SUPPLY_NODE_IDS, rule=eq4)

    print("Done!")

    return model


def save_data(model):

    print("Saving data...")

    # x variables
    keys = list(model.x.keys())
    index = pd.MultiIndex.from_tuples(keys, names=["supply_node_id", "demand_node_id", "itemset_id"])
    df_x = pd.Series(index=index, dtype="float64")
    for key in keys:
        df_x[key] = value(model.x[key])
    df_x = df_x.reset_index()

    # y variables
    keys = list(model.y.keys())
    index = pd.MultiIndex.from_tuples(keys, names=["supply_node_id", "sku_id"])
    df_y = pd.Series(index=index, dtype="float64")
    for key in keys:
        df_y[key] = value(model.y[key])
    df_y = df_y.reset_index()

    # v variables
    keys = list(model.v.keys())
    index = pd.MultiIndex.from_tuples(keys, names=["supply_node_id", "sku_id"])
    df_v = pd.Series(index=index, dtype="float64")
    for key in keys:
        df_v[key] = value(model.v[key])
    df_v = df_v.reset_index()

    # init pandas excel writer
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(
        os.path.abspath(
            os.path.join(dir_path, os.pardir)
            ),
        'data'
    )
    writer = pd.ExcelWriter(os.path.join(path, 'pyomo_solution.xlsx'), engine='xlsxwriter')

    df_x.to_excel(writer, sheet_name='solution_warehouse_store_qty')
    df_y.to_excel(writer, sheet_name='solution_warehouse_sku_proc')
    df_v.to_excel(writer, sheet_name='solution_warehouse_sku_left')
    writer.close()

    print("Done!")


if __name__ == '__main__':

    data = load_data()

    # init model
    model = init_model(data)

    print("Solving")
    SolverFactory('glpk').solve(model)
    print("Done!")

    # save data
    save_data(model)

