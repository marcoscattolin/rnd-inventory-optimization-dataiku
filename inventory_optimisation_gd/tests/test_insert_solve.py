import pytest
import numpy as np
import pandas as pd
from inventory_optimisation_gd import pipeline

def config_unittest():
    return {'solver': {'solver': 'SCIP', 'mip_gap': 0.05, 'verbose': True}}

def data_for_unittest_0():
    shipping_df = pd.DataFrame({"source_node_id":[0,0,0,1,1,1,2,2,2],  "destination_node_id":[0,1,2,0,1,2,0,1,2],  "cost":[1,10,10,10,1,10,10,10,1]})
    itemsets_df = pd.DataFrame({"itemset_id":[0,0],  "sku_id":[0,1]})
    supply_nodes_df = pd.DataFrame({"node_id":[0,1,2],"capacity":[10,10,10]})
    supply_df = pd.DataFrame({"node_id":[0,0,1,1,2,2],  "sku_id":[0,1,0,1,0,1],  "cost":[1,10,10,1,10,10], "current_quantity":[5,5,5,5,5,5]})
    demand_nodes_df = pd.DataFrame({"node_id":[0,1,2], "itemset_id":[0,0,0], "demand_mean":[5,5,5], "demand_variance":[0,0,0]}) 
    config = config_unittest()
    return (shipping_df, itemsets_df, supply_nodes_df, supply_df, demand_nodes_df, config)


def data_for_unittest_1():
    shipping_df = pd.DataFrame({"source_node_id":[0,0,0,1,1,1,2,2,2],  "destination_node_id":[0,1,2,0,1,2,0,1,2],  "cost":[1,10,10,10,1,10,10,10,1]})
    itemsets_df = pd.DataFrame({"itemset_id":[0,0],  "sku_id":[0,1]})
    supply_nodes_df = pd.DataFrame({"node_id":[0,1,2],"capacity":[10,10,10]})
    supply_df = pd.DataFrame({"node_id":[0,0,1,1,2,2],  "sku_id":[0,1,0,1,0,1],  "cost":[1,10,10,1,10,10], "current_quantity":[0,0,0,0,0,0]})
    demand_nodes_df = pd.DataFrame({"node_id":[0,1,2], "itemset_id":[0,0,0], "demand_mean":[5,5,5], "demand_variance":[0,0,0]}) 
    config = config_unittest()
    return (shipping_df, itemsets_df, supply_nodes_df, supply_df, demand_nodes_df, config)

def data_for_unittest_2():
    shipping_df = pd.DataFrame({"source_node_id":[0,0,0,1,1,1,2,2,2],  "destination_node_id":[0,1,2,0,1,2,0,1,2],  "cost":[1,10,10,10,1,10,10,10,1]})
    itemsets_df = pd.DataFrame({"itemset_id":[0,0],  "sku_id":[0,1]})
    supply_nodes_df = pd.DataFrame({"node_id":[0,1,2],"capacity":[10,10,10]})
    supply_df = pd.DataFrame({"node_id":[0,0,1,1,2,2],  "sku_id":[0,1,0,1,0,1],  "cost":[1,10,10,1,10,10], "current_quantity":[5,5,5,5,5,5]})
    demand_nodes_df = pd.DataFrame({"node_id":[0,1,2], "itemset_id":[0,0,0], "demand_mean":[15,0,0], "demand_variance":[0,0,0]}) 
    config = config_unittest()
    return (shipping_df, itemsets_df, supply_nodes_df, supply_df, demand_nodes_df, config)

def data_for_unittest_3():
    shipping_df = pd.DataFrame({"source_node_id":[0,0,0,1,1,1,2,2,2],  "destination_node_id":[0,1,2,0,1,2,0,1,2],  "cost":[1,10,10,10,1,10,10,10,1]})
    itemsets_df = pd.DataFrame({"itemset_id":[0,0],  "sku_id":[0,1]})
    supply_nodes_df = pd.DataFrame({"node_id":[0,1,2],"capacity":[10,10,10]})
    supply_df = pd.DataFrame({"node_id":[0,0,1,1,2,2],  "sku_id":[0,1,0,1,0,1],  "cost":[1,10,10,1,10,10], "current_quantity":[5,5,0,0,0,0]})
    demand_nodes_df = pd.DataFrame({"node_id":[0,1,2], "itemset_id":[0,0,0], "demand_mean":[15,0,0], "demand_variance":[0,0,0]})
    config = config_unittest()
    return (shipping_df, itemsets_df, supply_nodes_df, supply_df, demand_nodes_df, config)


def test_0_itemsets():

    data = data_for_unittest_0()

    output = pipeline(*data)

    assert np.allclose(dict_to_test['itemsets_output'][0], np.array([[5, 0, 0], [0, 5, 0], [0, 0, 5]]))


def test_0_skus():

    data = data_for_unittest_0()

    output = pipeline(*data)
    
    assert np.allclose(dict_to_test['procurement_output'], np.array([[0, 0], [0, 0], [0, 0]]))


def test_0_objective_value():

    data = data_for_unittest_0()

    output = pipeline(*data)
    
    assert np.allclose(dict_to_test['objective_value'], 30)






####

def test_1_itemsets():

    data = data_for_unittest_1()

    output = pipeline(*data)

    assert np.allclose(dict_to_test['itemsets_output'][0], np.array([[5, 0, 0], [0, 5, 0], [0, 0, 5]]))


def test_1_skus():

    data = data_for_unittest_1()

    output = pipeline(*data)
    
    assert np.allclose(dict_to_test['procurement_output'], np.array([[5, 5], [5, 5], [5, 5]]))


def test_1_objective_value():

    data = data_for_unittest_1()

    output = pipeline(*data)
    
    assert np.allclose(dict_to_test['objective_value'], 240)


#########


def test_2_itemsets():

    data = data_for_unittest_2()

    output = pipeline(*data)

    assert np.allclose(dict_to_test['itemsets_output'][0], np.array([[5, 5, 5], [0, 0, 0], [0, 0, 0]]))


def test_2_skus():

    data = data_for_unittest_2()

    output = pipeline(*data)
    
    assert np.allclose(dict_to_test['procurement_output'], np.array([[0, 0], [0, 0], [0, 0]]))


def test_2_objective_value():

    data = data_for_unittest_2()

    output = pipeline(*data)
    
    assert np.allclose(dict_to_test['objective_value'], 210)


########

def test_3_itemsets():

    data = data_for_unittest_3()

    output = pipeline(*data)

    assert np.allclose(output['itemsets_output'][0], np.array([[5, 5, 5], [0, 0, 0], [0, 0, 0]]))


def test_3_skus():

    data = data_for_unittest_3()

    output = pipeline(*data)
    
    assert np.allclose(dict_to_test['procurement_output'], np.array([[0, 0], [5, 5], [5, 5]]))


def test_3_objective_value():

    data = data_for_unittest_3()

    output = pipeline(*data)
    
    assert np.allclose(dict_to_test['objective_value'], 365)





