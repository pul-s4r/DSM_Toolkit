"""
    DSMMatrix describes interactions between two tasks
    i.e. whether one task depends on the input/output of another.
    If there is such an interaction the tasks are considered coupled.
"""
from collections import Counter
import copy
import numpy as np
import json
from cluster_matrix import ClusterMatrix

class DSMMatrix(object):
    """ Lists activities in act_labels and dependencies in mat (2-d matrix)
    """
    def __init__(self, mat, activity_labels=None):
        """ Default constructor is to accept a matrix and list of labels. Checks size of matrix and labels for correctness
        """
        assert len(mat.shape) == 2, "Input matrix must be two-dimensional"
        assert mat.shape[0] == mat.shape[1], "Input matrix must be square"
        assert activity_labels == None or isinstance(activity_labels, list), "Labels must be a list. If no labels are provided, use None"

        self._mat = mat.copy()
        self._labels = []
        self._system_elements = [];
        if activity_labels:
            assert len(activity_labels) == mat.shape[0], "Labels must match matrix"
            # self._labels = activity_labels
            self._labels = [str(a) for a in activity_labels]
        else:
            self._labels = self._make_labels()

    def __repr__(self):
        return str(self._mat)

    def __str__(self):
        return "DSMMatrix(" + str(self._mat) + ")"

    @classmethod
    def from_size(cls, size):
        """ Alternate constructor for DSM matrix creating a blank matrix of given size and act_labels with all "None" values
        """
        mat = np.zeros([size, size])
        act_labels = [str(x+1) for x in range(size)]
        return cls(mat, act_labels)

    def __repr__(self):
        return self._mat

    def __len__(self):
        """ Built in len() method gives characteristic dimension of container
        """
        return len(self._labels)

    @property
    def mat(self):
        return self._mat

    @mat.setter
    def mat(self, val):
        self._mat = val

    def _set(self, row, col, val=1):
        self._mat[row, col] = val

    def set(self, row=-1, col=-1):
        if row >= 0 and row < self._mat.shape[0] and col >= 0 and col < self._mat.shape[1]:
            self._set(row, col, val=1)
        else:
            raise ArithmeticError

    def unset(self, row=-1, col=-1):
        if row >= 0 and row < self._mat.shape[0] and col >= 0 and col < self._mat.shape[1]:
            self._set(row, col, val=0)
        else:
            raise ArithmeticError

    def clear_elements(self, elems):
        assert isinstance(elems, list) and all(isinstance(x, int) for x in elems)
        assert(all(x >= 0 and x < self._mat.shape[0] for x in elems))
        for i in elems:
            self._mat[i,:] = 0
            self._mat[:,i] = 0

    def tolist(self):
        return self._mat.tolist()

    def tojson(self):
        return json.dumps(self._mat.tolist())

    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, val):
        assert len(val) == self._mat.shape[1], "Labels must match matrix"
        self._labels = val

    def _make_labels(self):
        """ Returns numerical labels for each element in the matrix
        """
        return [str(x+1) for x in range(self.mat.shape[1])]

    def autolabel(self):
        self._labels = self._make_labels();

    @staticmethod
    def reorder_by_cluster(dsm_matrix, cluster_matrix):
        """ Returns a new dsm_matrix object expanding out the elements in multiple clusters, also recalculating the size of this matrix
        """
        assert isinstance(dsm_matrix, DSMMatrix)
        assert isinstance(cluster_matrix, ClusterMatrix)
        assert cluster_matrix.num_activities == len(dsm_matrix), "Number of activities in cluster_matrix should be same as the dsm_matrix"

        cl_mat = cluster_matrix.mat
        ds_mat = dsm_matrix.mat

        ds_mat = np.tril(ds_mat, k=-1) + np.diag(np.zeros(ds_mat.shape[0])) + np.triu(ds_mat, k=1)

        num_ele = cl_mat[cl_mat > 0].size
        temp_mat = np.zeros([num_ele, len(dsm_matrix)])
        new_ds_mat = DSMMatrix.from_size(num_ele)

        ii = 0
        for cluster in cl_mat:
            for ind, flag in enumerate(cluster):
                if flag:
                    temp_mat[ii,:] = ds_mat[ind,:]
                    new_ds_mat.labels[ii] = ind
                    ii += 1

        for ind, col in enumerate(new_ds_mat.labels):
            new_ds_mat.mat[:,ind] = temp_mat[:,col]
            new_ds_mat.labels[ind] = dsm_matrix.labels[col]

        return new_ds_mat

    @staticmethod
    def place_diag(dsm_matrix):
        """ Returns a new dsm_matrix object with the matrix diagonal populated
        """
        assert isinstance(dsm_matrix, DSMMatrix)

        ds_mat = dsm_matrix.mat

        num_ele = ds_mat.shape[0]
        new_ds_mat = DSMMatrix.from_size(num_ele)

        new_ds_mat.mat = np.tril(ds_mat, k=-1) + np.diag(np.ones(num_ele)) + np.triu(ds_mat, k=1)
        new_ds_mat.labels = dsm_matrix.labels

        return new_ds_mat

    @staticmethod
    def annotate_clusters(DSM_matrix, cluster_matrix):
        assert isinstance(DSM_matrix, DSMMatrix)
        assert isinstance(cluster_matrix, ClusterMatrix)
        new_ds_mat = DSMMatrix(np.zeros(DSM_matrix.mat.shape))
        new_ds_mat.mat = DSM_matrix.mat
        new_clu_mat = ClusterMatrix.from_mat(np.zeros(cluster_matrix.mat.shape))
        new_clu_mat.mat = cluster_matrix.mat

        new_ds_mat.mat -= 1;

        cluster_count = 1
        s_i = 0
        for c_i in range(cluster_matrix.mat.shape[0]):
            n_el = np.sum(cluster_matrix.mat[c_i,:], axis=0, dtype=np.int)
            for i in range(s_i, s_i+n_el):
                for j in range(s_i, s_i+n_el):
                    new_ds_mat.mat[i,j] = cluster_count if DSM_matrix.mat[i,j] >= 0 else 0
            s_i += n_el
            cluster_count += 1

        return new_ds_mat
