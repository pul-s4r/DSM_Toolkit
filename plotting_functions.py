from dsm_helper_classes import *
import copy
import numpy as np
import sys
import matplotlib.pyplot as plt

def graph_matrix(DSM_matrix, cluster_matrix=None,
    x_title='Element', y_title='Element', graph_title='DSM Matrix',
    x_tcklabel=None, y_tcklabel=None, print_flag=0):
    """ Graph the DSM and cluster matrix.

    """
    assert isinstance(DSM_matrix, DSMMatrix)
    # if not isinstance(cluster_matrix, ClusterMatrix)

    ds_mat = DSM_matrix.mat

    (row_in, col_out) = np.where(ds_mat)
    m_value = ds_mat[ds_mat != 0]

    max_row = np.max(row_in)
    max_col = np.max(col_out)

    axis = np.array([0, max_col, max_row]);

    max_value = np.max(m_value)
    data_scale = np.ceil(500/max_value)/20

    x_tcklabel = DSM_matrix.labels
    y_tcklabel = DSM_matrix.labels

    if isinstance(cluster_matrix, ClusterMatrix):
        new_DSM_matrix = DSMMatrix.annotate_clusters(DSM_matrix, cluster_matrix)
        orig_ds_mat = DSM_matrix.mat
        ds_mat = new_DSM_matrix.mat

    fig, ax = plt.subplots()
    im = ax.imshow(ds_mat, cmap=plt.cm.Blues)

    ax.set_xticks(np.arange(len(x_tcklabel)))
    ax.set_yticks(np.arange(len(y_tcklabel)))

    ax.set_xticklabels(x_tcklabel)
    ax.set_yticklabels(y_tcklabel)
    ax.set_xlabel(x_title)
    ax.set_ylabel(y_title)
    ax.xaxis.set_label_position('top')

    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # plt.setp(ax.get_xticklabels(), rotation=90, ha="right",
    #      rotation_mode="anchor")

    ax.set_title(graph_title)
    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    d_mat = np.array([
        [1, 0, 1, 0, 0, 1, 0, 1],
        [1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 1],
        [0, 0, 1, 1, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 1, 0, 0],
        [0, 1, 0, 0, 0, 1, 1, 0],
        [1, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 0, 0, 1]
    ])
    d = DSMMatrix(d_mat)

    c_mat = np.array([
        [0, 0, 0, 1, 0, 1, 0, 0],
        [1, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ])
    c = ClusterMatrix.from_mat(c_mat)

    graph_matrix(d, cluster_matrix=c)
