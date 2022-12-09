import pytest
import numpy as np
import pandas as pd
from .pipeline import insert_solve


def data_for_unittest_1():
    shipping_df = pd.DataFrame({"source_node_id":[0,0,0,1,1,1,2,2,2],  "destination_node_id":[0,1,2,0,1,2,0,1,2],  "cost":[1,10,10,10,1,10,10,10,1]})
    itemsets_df = pd.DataFrame({"itemset_id":[0,0],  "sku_id":[0,1]})
    supply_nodes_df = pd.DataFrame({"node_id":[0,1,2],"capacity":[10,10,10]})
    supply_df = pd.DataFrame({"node_id":[0,0,1,1,2,2],  "sku_id":[0,1,0,1,0,1],  "cost":[1,10,10,1,10,10], "current_quantity":[0,0,0,0,0,0]})
    demand_nodes_df = pd.DataFrame({"node_id":[0,1,2], "itemset_id":[0,0,0], "demand_mean":[5,5,5], "demand_variance":[0,0,0]}) 

    return (shipping_df, itemsets_df, supply_nodes_df, supply_df, demand_nodes_df)

def data_for_unittest_2():
    shipping_df = pd.DataFrame({"source_node_id":[0,0,0,1,1,1,2,2,2],  "destination_node_id":[0,1,2,0,1,2,0,1,2],  "cost":[1,10,10,10,1,10,10,10,1]})
    itemsets_df = pd.DataFrame({"itemset_id":[0,0],  "sku_id":[0,1]})
    supply_nodes_df = pd.DataFrame({"node_id":[0,1,2],"capacity":[10,10,10]})
    supply_df = pd.DataFrame({"node_id":[0,0,1,1,2,2],  "sku_id":[0,1,0,1,0,1],  "cost":[1,10,10,1,10,10], "current_quantity":[5,5,5,5,5,5]})
    demand_nodes_df = pd.DataFrame({"node_id":[0,1,2], "itemset_id":[0,0,0], "demand_mean":[15,0,0], "demand_variance":[0,0,0]}) 
    
    return (shipping_df, itemsets_df, supply_nodes_df, supply_df, demand_nodes_df)

def data_for_unittest_3():
    shipping_df = pd.DataFrame({"source_node_id":[0,0,0,1,1,1,2,2,2],  "destination_node_id":[0,1,2,0,1,2,0,1,2],  "cost":[1,10,10,10,1,10,10,10,1]})
    itemsets_df = pd.DataFrame({"itemset_id":[0,0],  "sku_id":[0,1]})
    supply_nodes_df = pd.DataFrame({"node_id":[0,1,2],"capacity":[10,10,10]})
    supply_df = pd.DataFrame({"node_id":[0,0,1,1,2,2],  "sku_id":[0,1,0,1,0,1],  "cost":[1,10,10,1,10,10], "current_quantity":[5,5,0,0,0,0]})
    demand_nodes_df = pd.DataFrame({"node_id":[0,1,2], "itemset_id":[0,0,0], "demand_mean":[15,0,0], "demand_variance":[0,0,0]})

    return (shipping_df, itemsets_df, supply_nodes_df, supply_df, demand_nodes_df)


def test_1_itemsets():

    data = data_for_unittest_1()

    dict_to_test = insert_solve(*data)

    assert np.allclose(dict_to_test['itemsets_output'][0], np.array([[5, 0, 0], [0, 5, 0], [0, 0, 5]]))


def test_1_skus():

    data = data_for_unittest_1()

    dict_to_test = insert_solve(*data)
    
    assert np.allclose(dict_to_test['procurement_output'], np.array([[5, 5], [5, 5], [5, 5]]))


def test_1_objective_value():

    data = data_for_unittest_1()

    dict_to_test = insert_solve(*data)
    
    assert np.allclose(dict_to_test['objective_value'], 240)


#########


def test_2_itemsets():

    data = data_for_unittest_2()

    dict_to_test = insert_solve(*data)

    assert np.allclose(dict_to_test['itemsets_output'][0], np.array([[5, 5, 5], [0, 0, 0], [0, 0, 0]]))


def test_2_skus():

    data = data_for_unittest_2()

    dict_to_test = insert_solve(*data)
    
    assert np.allclose(dict_to_test['procurement_output'], np.array([[0, 0], [0, 0], [0, 0]]))


def test_2_objective_value():

    data = data_for_unittest_2()

    dict_to_test = insert_solve(*data)
    
    assert np.allclose(dict_to_test['objective_value'], 110)


########

def test_3_itemsets():

    data = data_for_unittest_3()

    dict_to_test = insert_solve(*data)

    assert np.allclose(dict_to_test['itemsets_output'][0], np.array([[5, 5, 5], [0, 0, 0], [0, 0, 0]]))


def test_3_skus():

    data = data_for_unittest_3()

    dict_to_test = insert_solve(*data)
    
    assert np.allclose(dict_to_test['procurement_output'], np.array([[0, 0], [5, 5], [5, 5]]))


def test_3_objective_value():

    data = data_for_unittest_3()

    dict_to_test = insert_solve(*data)
    
    assert np.allclose(dict_to_test['objective_value'], 265)






# if __name__ == "__main__":
#     test_1_itemsets()

