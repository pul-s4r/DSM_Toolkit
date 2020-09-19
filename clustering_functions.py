from dsm_helper_classes import *
import copy 
import numpy as np

class ClusterGenerator(object): 
    """ 
    Takes a dependency structure matrix of n activities and assorted cluster control parameters and outputs a cluster matrix. 
    Encapsulates the clustering algorithm proper, coordination cost calculation and element-cluster bids
    """
    _dsm_mat = None
    _cluster_mat = None
    _params = None
    
    def __init__(self, dsm_mat = None, default_size = 2):  
        if isinstance(dsm_mat, DSMMatrix): 
            self._dsm_mat = dsm_mat
        else: 
            self._dsm_mat = DSMMatrix.from_size(default_size)
        
        # Set clustering control parameters
        max_size = self._dsm_mat.mat.shape[0]
        self._params = set_default_cluster_parameters(max_size)
        
        # Initialise matrices and arrays 
        self._DSM_size = self._dsm_mat.mat.shape[1]
        self._n_clusters = max_size
        self._max_repeat = 10
        
        _dsm_rowvector = np.zeros([self._DSM_size, 1])
        self._coordination_cost = np.copy(_dsm_rowvector)
        self._cluster_size = np.copy(_dsm_rowvector)
        self._new_cluster_mat = np.zeros([self._DSM_size, self._DSM_size])
        self._new_cluster_size = np.copy(_dsm_rowvector)
        self._cluster_bid = np.copy(_dsm_rowvector)
        self._new_cluster_bid = np.copy(_dsm_rowvector)
        self._new_coordination_cost = np.copy(_dsm_rowvector)
        self._rnd_elem_array = np.copy(_dsm_rowvector)
        self._cluster_list = np.copy(_dsm_rowvector)
        
        # Initialise cluster matrix along diagonals
        # Initial condition: nth cluster contains nth element
        self._cluster_diagonals = np.ones([1, self._n_clusters])
        self._cluster_mat = np.diag(self._cluster_diagonals.flatten())
        self._cluster_size = np.ones([self._n_clusters, 1])
        
        # Calculate initial starting condition
        self._total_coord_cost = self.coord_cost(self._dsm_mat.mat, self._cluster_mat, self._cluster_size, pow_cc = self._params.pow_cc)
        self._best_coord_cost = self._total_coord_cost
        
        self._cost_history = np.zeros([10000, 1])
        self._history_index = 0
    
    @property 
    def dsm(self): 
        return self._dsm_mat
        
    @dsm.setter
    def dsm(self, mat_object): 
        assert isinstance(mat_object, DSMMatrix)
        self._dsm_mat = mat_object
        new_max_size = mat_object.mat.shape[0]
        self._params.max_cluster_size = new_max_size
        self._params.rand_accept = 1/(2*new_max_size)
        self._params.max_cluster_size = 1/(2*new_max_size)
    
    @property 
    def params(self): 
        return self._params 
    
    @params.setter
    def params(self, param_object): 
        assert isinstance(param_object, ClusterParameters)
        assert param_object.max_cluster_size >= self._dsm_mat.mat.shape[0]
        self._params = param_object

    def _coord_cost(self, cluster_matrix, cluster_size, pow_cc=None): 
        
    
        if isinstance(pow_cc, int): 
            pass
        elif not pow_cc and self._params: 
            pow_cc = self._params.pow_cc
        else: 
            pow_cc = 1

    def _make_bid(self):
        pass

    def cluster(self):
        pass
