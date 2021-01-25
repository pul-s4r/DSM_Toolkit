"""
    ClusterMatrix describes the membership of specific tasks to task clusters.
"""

import copy
import numpy as np

class ClusterMatrix(object):
    def __init__(self, n_clus):
        """ Default constructor is to create a symmetric matrix and vector to track the cluster sizes
        """
        self._mat = np.zeros((n_clus, n_clus))
        self._num_activities = n_clus
        self.update_cluster_size()
        self.total_coord_cost = 0

    def __repr__(self):
        return self._mat

    def __str__(self):
        return "ClusterMatrix(" + self._mat + ")"

    @classmethod
    def from_mat(cls, mat):
        """ Alternate constructor from a given input matrix
        """
        num_act = mat.shape[1]
        cluster_mat = ClusterMatrix(num_act)
        cluster_mat.mat = mat
        cluster_mat.update_cluster_size()

        return cluster_mat

    def copy(self):
        result = ClusterMatrix(self._num_activities)
        result._mat = self._mat.copy()
        return result

    @property
    def mat(self):
        return self._mat

    @mat.setter
    def mat(self, val):
        self._mat = val

    @property
    def num_clusters(self):
        return len(self.cluster_size)

    @property
    def num_activities(self):
        return self._num_activities

    def update_cluster_size(self):
        """ Updates the cluster_size array to reflect changes in mat
        """
        self.cluster_size = np.array([row[row > 0].size for row in self._mat])
        # self.cluster_size = np.sum(self._mat, axis=1)

    def update_mat(self, element, cluster_list):
        """ Updates the matrix to reflect a new bid in input cluster_list
        """
        assert len(cluster_list) == self.num_activities, "Number of elements in cluster_list must match the number of activities in this cluster matrix"
        self._mat[:,element] = \
            np.logical_or(self._mat[:,element], cluster_list)

    @staticmethod
    def reorder(cluster_matrix):
        """ Reorders the clusters in order of row size (sum along columns):

            For instance,
            (1) Input:
            [[1, 0],
             [1, 1]]
            becomes:
            [[1, 1],
             [1, 0]]

            (2) Input:
            [[1, 1, 0],
             [0, 1, 0],
             [1, 1, 1]]
            becomes:
            [[1, 1, 1],
             [1, 1, 0],
             [0, 1, 0]]

            If the input is an ordered cluster, the output is itself. If an equivalent ordering is found the original is returned.
        """
        # import pdb; pdb.set_trace()
        result = None

        new_clu_mat = ClusterMatrix.from_mat(np.zeros(cluster_matrix.mat.shape))
        row_elems = np.sum(cluster_matrix.mat, axis=1)
        row_elems_sorted = np.sort(row_elems, axis=0)
        row_elems_indices = np.argsort(row_elems, axis=0)
        row_elems_indices = np.flip(row_elems_indices, axis=0)

        new_clu_mat.mat = np.take(cluster_matrix.mat, row_elems_indices, axis=0)
        new_clu_mat.update_cluster_size()

        if (row_elems == np.sum(new_clu_mat.mat, axis=1)).all():
            result = cluster_matrix
        else:
            result = new_clu_mat

        return result
