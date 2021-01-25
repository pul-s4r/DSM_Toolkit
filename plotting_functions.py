from ClusterParameters import ClusterParameters, set_default_cluster_parameters
from ClusterMatrix import ClusterMatrix
from DSMMatrix import DSMMatrix
import copy
import numpy as np
import sys
import matplotlib.pyplot as plt

def graph_matrix(gen_matrix, cluster_matrix=None,
    x_title='Element', y_title='Element', graph_title='DSM Matrix',
    x_tcklabel=None, y_tcklabel=None, print_flag=0):
    """ Graph the DSM and cluster matrix.

    """
    assert isinstance(gen_matrix, DSMMatrix) or isinstance(gen_matrix, ClusterMatrix)
    # if not isinstance(cluster_matrix, ClusterMatrix)

    ds_mat = gen_matrix.mat

    (row_in, col_out) = np.where(ds_mat)
    m_value = ds_mat[ds_mat != 0]

    max_row = np.max(row_in)
    max_col = np.max(col_out)

    axis = np.array([0, max_col, max_row]);

    max_value = np.max(m_value)
    data_scale = np.ceil(500/max_value)/20

    if x_tcklabel is None and isinstance(gen_matrix, DSMMatrix):
        x_tcklabel = gen_matrix.labels
    elif isinstance(x_tcklabel, list):
        if len(x_tcklabel) != ds_mat.shape[0]:
            x_tcklabel = [str(x+1) for x in range(ds_mat.shape[0])]
    else:
        x_tcklabel = [str(x+1) for x in range(ds_mat.shape[0])]

    if y_tcklabel is None and isinstance(gen_matrix, DSMMatrix):
        y_tcklabel = gen_matrix.labels
    elif isinstance(y_tcklabel, list):
        if len(y_tcklabel) != ds_mat.shape[0]:
            y_tcklabel = [str(x+1) for x in range(ds_mat.shape[0])]
    else:
        y_tcklabel = [str(x+1) for x in range(ds_mat.shape[0])]

    if isinstance(cluster_matrix, ClusterMatrix):
        new_gen_matrix = DSMMatrix.annotate_clusters(gen_matrix, cluster_matrix)
        orig_ds_mat = gen_matrix.mat
        ds_mat = new_gen_matrix.mat

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
    plt.draw()

def block_exit():
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
    graph_matrix(c)
    block_exit()
