""" Tests for the implemented functions
"""
import unittest

from clustering_functions import *
from dsm_helper_classes import *
from plotting_functions import *

# Test case for DSMMatrix.reorder_by_cluster
class DSMReorderTestCase(unittest.TestCase):    
    # d_mat = np.identity(3) 
    d_mat = np.array([[1, 0, 0, 0], [0, 0, 0, 0], [1, 0, 1, 0], [0, 0, 1, 1]])
    d_list = ["1", "2", "3", "4"]
    d = DSMMatrix(d_mat, d_list)
    # print("Original DSM: ")
    # print(d.mat)

    c_mat = np.array([[1, 0, 1, 1], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    c = ClusterMatrix.from_mat(c_mat)
    # print("Original Cluster: ")
    # print(c.mat)

    new_d_mat = DSMMatrix.reorder_by_cluster(d, c)
    # print("Reordered DSM: ")
    # print(new_d_mat.mat)
    # print(new_d_mat.act_labels)
    val_comp_1 = new_d_mat.mat == np.array([[0, 0, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]])
    lab_comp_1 = new_d_mat.act_labels == ['1', '3', '4', '2']
    assert val_comp_1.all()
    assert lab_comp_1
    
    
    d_mat_2 = np.array([[1, 0, 0, 1], [0, 0, 0, 0], [1, 0, 1, 0], [0, 0, 1, 1]])
    d_list_2 = ["1", "2", "3", "4"]
    d_2 = DSMMatrix(d_mat_2, d_list_2)
    # print("Original DSM: ")
    # print(d_2.mat)

    c_mat_2 = np.array([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]])
    c_2 = ClusterMatrix.from_mat(c_mat_2)
    # print("Original Cluster: ")
    # print(c_2.mat)

    new_d_mat_2 = DSMMatrix.reorder_by_cluster(d_2, c_2)
    # print("Reordered DSM: ")
    # print(new_d_mat_2.mat)
    # print(new_d_mat_2.act_labels)
    val_comp_2 = new_d_mat_2.mat == np.array([[0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 0, 0], [1, 0, 0, 0]])
    lab_comp_2 = new_d_mat_2.act_labels == ['4', '3', '2', '1']
    assert val_comp_2.all()
    assert lab_comp_2


# Test case for ClusterMatrix.reorder
class ClusterReorderTestCase(unittest.TestCase):
    c_mat = np.array([[1, 1, 0], [1, 0, 1], [1, 1, 1]])
    c = ClusterMatrix.from_mat(c_mat)
    new_c_mat = ClusterMatrix.reorder(c)
    # print("Original: ")
    # print(c.mat)
    # print("Reordered: ")
    # print(new_c_mat.mat)
    # print("Reordered size: ")
    # print(new_c_mat.cluster_size)
    val_comp = new_c_mat.mat == np.array([c_mat[2], c_mat[1], c_mat[0]])
    size_comp = new_c_mat.cluster_size == np.array([3, 2, 2])
    assert val_comp.all()
    assert size_comp.all()
    
    c_mat_2 = np.array([[1, 1, 0], [0, 1, 0], [1, 1, 1]])
    c_2 = ClusterMatrix.from_mat(c_mat_2)
    new_c_mat_2 = ClusterMatrix.reorder(c_2)
    
    # print("Original: ")
    # print(c_2.mat)
    # print("Reordered: ")
    # print(new_c_mat_2.mat)
    # print("Reordered size: ")
    # print(new_c_mat_2.cluster_size)

    val_comp_2 = new_c_mat_2.mat == np.array([c_mat_2[2], c_mat_2[0], c_mat_2[1]])
    size_comp_2 = new_c_mat_2.cluster_size == np.array([3, 2, 1])
    assert val_comp_2.all()
    assert size_comp_2.all()
    
    # Checks that a new cluster matrix (once reordered) is invariant under reordering
    # import pdb; pdb.set_trace()
    newer_c_mat = ClusterMatrix.reorder(new_c_mat)
    # print(newer_c_mat.mat)
    assert (newer_c_mat.mat == new_c_mat.mat).all()


# Tests for dsm_helper_classes
class ClusterParametersTestCase(unittest.TestCase):
    raise NotImplementedError

class DSMMatrixTestCase(unittest.TestCase):
    raise NotImplementedError

class ClusterMatrixTestCase(unittest.TestCase):
    raise NotImplementedError

# Tests for clustering_functions
class BidTestCase(unittest.TestCase):
    raise NotImplementedError

class ClusterTestCase(unittest.TestCase):
    raise NotImplementedError

if __name__ == "__main__":
    unittest.main()