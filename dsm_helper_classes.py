""" Contains helper classes for containing the relevant DSM data
    1. ClusterParameters is for defining the behaviour of a specific optimisation algorithm
    2. DSMMatrix
    3. ClusterMatrix
"""
from collections import Counter
import copy
import numpy as np

# ----- Cluster Parameters -----------------------------------------------------
class ClusterParameters(object):
    """ Constants that define the behaviour of the optimisation algorithm
    """
    def __init__(self, pow_cc, pow_bid, pow_dep, max_cluster_size, rand_accept,              rand_bid, times, stable_limit, max_repeat):
        # Penalty functions for the clusters
        self.pow_cc = pow_cc
        self.pow_bid = pow_bid
        self.pow_dep = pow_dep

        # Parameters dictating the prob of accepting a non-better solution
        self.rand_accept = rand_accept
        self.rand_bid = rand_bid

        # Sets limits for the number of calculations/passes carried out
        self.max_cluster_size = max_cluster_size
        self.max_repeat = max_repeat
        self.times = times

        # Dictates the limit for which the algorithm is considered converged
        self.stable_limit = stable_limit

def set_default_cluster_parameters(max_size):
    """ Sets the cluster_parameters following the guidelines by R Thebeau (2000)
    """
    return ClusterParameters(
        pow_cc = 1,
        pow_bid = 1,
        pow_dep = 4,
        max_cluster_size = max_size,
        rand_accept = 1 / (2 * max_size),
        rand_bid = 1 / (2 * max_size),
        times = 2,
        stable_limit = 2,
        max_repeat = 10
    )
# ------------------------------------------------------------------------------

class DSMMatrix(object):
    """ Lists activities in act_labels and dependencies in mat (2-d matrix)
    """
    def __init__(self, mat, activity_labels=None):
        """ Default constructor is to accept a matrix and list of labels. Checks size of matrix and labels for correctness
        """
        assert len(mat.shape) == 2, "Input matrix must be two-dimensional"
        assert mat.shape[0] == mat.shape[1], "Input matrix must be square"
        assert activity_labels == None or isinstance(activity_labels, list), "Labels must be a list. If no labels are provided, use None"

        self._mat = mat
        self._labels = []
        self._system_elements = [];
        if activity_labels: 
            assert len(activity_labels) == mat.shape[0], "Labels must match matrix"
            self._labels = activity_labels
        else: 
            self._labels = self._make_labels()
            
    @classmethod
    def from_size(cls, size):
        """ Alternate constructor for DSM matrix creating a blank matrix of given size and act_labels with all "None" values
        """
        mat = np.zeros([size, size])
        act_labels = [None for _ in range(size)]
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
 
    @property
    def labels(self): 
        return self._labels
    
    @labels.setter
    def labels(self, val): 
        assert len(val) == mat.shape[1], "Labels must match matrix"
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