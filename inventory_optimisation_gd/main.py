

import yaml
import os
import sys
import pandas as pd

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.dirname(dir_path))

from inventory_optimisation_gd.constructors.data_constructor import DataManager
from inventory_optimisation_gd.constructors.solver_constructor import SolverManager
from inventory_optimisation_gd.constructors.variable_constructor import VariableManager
from inventory_optimisation_gd.constructors.constraint_constructor import ConstraintManager
from inventory_optimisation_gd.constructors.objective_constructor import ObjectiveManager
from inventory_optimisation_gd.constructors.output_constructor import OutputManager

def pipeline(
    shipping_df, 
    itemsets_df, 
    supply_nodes_df, 
    supply_df, 
    demand_nodes_df,
    config
):
    data_init = DataManager(
        shipping_df, 
        itemsets_df, 
        supply_nodes_df, 
        supply_df, 
        demand_nodes_df,
        config
    )
    data_init.check_demand()

    solver_init = SolverManager(
        config['solver']['solver'], 
        config['solver']['mip_gap'],
        config['solver']['verbose'],
        )
    variables_init = VariableManager(data_init, solver_init)
    _ = ConstraintManager(data_init, solver_init, variables_init)
    objective_init = ObjectiveManager(data_init, solver_init, variables_init)

    solver_init.solve()

    output = OutputManager(
        data_init, 
        solver_init, 
        variables_init, 
        objective_init
        )

    return output

if __name__ == '__main__':

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

    solution = pipeline(
        pd.read_csv(os.path.join(path, schema_config['shipping_file']['file_name'])),
        pd.read_csv(os.path.join(path, schema_config['itemset_file']['file_name'])),
        pd.read_csv(os.path.join(path, schema_config['capacity_file']['file_name'])),
        pd.read_csv(os.path.join(path, schema_config['supply_file']['file_name'])),
        pd.read_csv(os.path.join(path, schema_config['demand_file']['file_name'])),
        config
    )

    # print solution
    # init pandas excel writer
    writer = pd.ExcelWriter(os.path.join(path, 'solution.xlsx'), engine='xlsxwriter')

    # write sheets
    solution.df_warehouse_store_qty.to_excel(writer, sheet_name='warehouse_store_qty')
    solution.df_warehouse_sku_qty.to_excel(writer, sheet_name='warehouse_sku_qty')
    solution.df_warehouse_sku_proc.to_excel(writer, sheet_name='warehouse_sku_proc')
    solution.df_warehouse_sku_left.to_excel(writer, sheet_name='warehouse_sku_left')

