from dsm_helper_classes import *
from clustering_functions import *
from plotting_functions import *

import numpy as np
import sys
import matplotlib.pyplot as plt

if __name__ == "__main__":
    cparams = ClusterParameters(
        pow_cc = 1,
        pow_bid = 1,
        pow_dep = 4,
        max_cluster_size = 8,
        rand_accept = 16,
        rand_bid = 16,
        times = 2,
        stable_limit = 2,
        max_repeat = 10
    )

    # d_mat = np.array([
    #     [0, 0, 1, 0, 0, 1, 0, 1],
    #     [1, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 1, 0, 0, 0, 1],
    #     [0, 0, 1, 0, 0, 0, 0, 1],
    #     [0, 0, 0, 0, 0, 1, 0, 0],
    #     [0, 1, 0, 0, 0, 0, 1, 0],
    #     [1, 0, 0, 1, 0, 0, 0, 0],
    #     [0, 0, 1, 0, 0, 0, 0, 0]
    # ])
    d_mat = np.array([
        [1, 1, 1, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 0],
        [1, 1, 0, 1, 0, 0, 1, 0],
        [0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 1, 1]
    ])
    d = DSMMatrix(d_mat)
    d_orig = DSMMatrix(d_mat)

    print_flag = 0
    extract_elements = [1, 4, 6, 7]

    for i in range(len(extract_elements)):
        d.mat[extract_elements[i],:] = 0
        d.mat[:,extract_elements[i]] = 0

    cg = ClusterGenerator(dsm_mat = d)
    cg.params = cparams

    (c_orig, total_coord_cost, cost_history) = cg.cluster(d)
    c = ClusterMatrix.reorder(c_orig)

    # import pdb; pdb.set_trace()
    d_new = DSMMatrix.reorder_by_cluster(d, c)

    d_g = DSMMatrix.place_diag(d)
    d_new_g = DSMMatrix.place_diag(d_new)

    graph_matrix(d_g, cluster_matrix=None,
        x_title='Element', y_title='Element', graph_title='DSM Matrix (Original)',
        x_tcklabel=None, y_tcklabel=None, print_flag=0)
    graph_matrix(c_orig, cluster_matrix=None,
        x_title='Element', y_title='Cluster', graph_title='Cluster Matrix',
        x_tcklabel=None, y_tcklabel=None, print_flag=0)

    graph_matrix(d_new_g, cluster_matrix=c,
        x_title='Element', y_title='Cluster', graph_title='New DSM Matrix (total cost: {})'.format(total_coord_cost),
        x_tcklabel=None, y_tcklabel=None, print_flag=0)
    block_exit()
