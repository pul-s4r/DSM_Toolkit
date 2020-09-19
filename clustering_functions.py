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
        # self._coordination_cost = np.copy(_dsm_rowvector)
        self._cluster_size = np.copy(_dsm_rowvector)
        self._new_cluster_mat = np.zeros([self._DSM_size, self._DSM_size])
        self._new_cluster_size = np.copy(_dsm_rowvector)
        self._cluster_bid = np.copy(_dsm_rowvector)
        self._new_cluster_bid = np.copy(_dsm_rowvector)
        # self._new_coordination_cost = np.copy(_dsm_rowvector)
        # self._rnd_elem_array = np.copy(_dsm_rowvector)
        self._cluster_list = np.copy(_dsm_rowvector)
        
        # Initialise cluster matrix along diagonals
        # Initial condition: nth cluster contains nth element
        self._cluster_diagonals = np.ones([1, self._n_clusters])
        self._cluster_mat = ClusterMatrix.from_mat(np.diag(self._cluster_diagonals.flatten()))
        self._cluster_size = np.ones([self._n_clusters, 1])
        
        # Calculate initial starting condition
        # self._total_coord_cost = self.coord_cost(self._dsm_mat.mat, self._cluster_mat, self._cluster_size, pow_cc = self._params.pow_cc)
        # self._best_coord_cost = self._total_coord_cost
        
        self._cost_history = np.zeros([10000, 1])
        self._history_index = 0
        
        # Store the best cluster matrix and corresponding cost and size 
        # self._best_curr_cost = self._total_coord_cost
        # self._best_curr_cluster_mat = self._cluster_mat
        # self._best_curr_cluster_size = self._cluster_size
    
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

    @staticmethod
    def _coord_cost(DSM_matrix, cluster_matrix, cluster_size, pow_cc=None): 
        """
        Calculate the coordination cost of the cluster matrix. 
        This routine checks all DSM interactions and adds to a total the cost of all intra-cluster interactions. Interactions outside of clusters are assigned a higher cost.  
        As per Thebeau (2000) the cost formula is, for each interdependent/coupled activity i and j: 
        (In cluster) (DSM[i] + DSM[j])*cluster_size[cluster_n]^pow_cc
        (Out of cluster) (DSM[i] + DSM[j])*DSM_size^pow_cc
        Sum each term to obtain the total. 
        """
        assert isinstance(dsm_matrix, DSMMatrix)
        assert isinstance(cluster_matrix, ClusterMatrix)
    
        if isinstance(pow_cc, int): 
            pass
        elif not pow_cc and self._params: 
            pow_cc = self._params.pow_cc
        else: 
            pow_cc = 1
            
        # get the number of clusters and size of the DSM
        n_clusters = cluster_matrix.mat.shape[0]
        DSM_size = cluster_matrix.mat.shape[1]
        
        # initialise coordination costs 
        total_coord_cost = 0
        coordination_cost = np.zeros([1, DSM_size])
        
        # dummy variable for reorder function
        DSM_labels = [str(x+1) for x in range(DSM_size)]
        
        # reorder the DSM according to the cluster matrix 
        new_DSM_matrix = DSMMatrix.reorder_by_cluster(DSM_matrix, cluster_matrix)
        new_DSM_size = new_DSM_matrix.mat.shape[0]
        
        num_cluster_elements = np.sum(cluster_matrix, axis=1)
        n = 1
        new_cluster_matrix = ClusterMatrix.from_mat(np.zeros([new_DSM_size, new_DSM_size]))
        
        # Create a new cluster matrix that matches the reordered DSM matrix 
        # 
        for i in range(n_clusters): 
            new_cluster_matrix.mat[i,n:n+num_cluster_elements[i]-1] = np.ones(1, num_cluster_elements[i])
            n += num_cluster_elements[i]
        
        # get new cluster size array matching matrix 
        new_cluster_size = np.sum(new_cluster_matrix, axis=1)
        
        # replace old data with new data for cost calculation 
        DSM_size = new_DSM_size
        DSM_matrix = new_DSM_matrix
        cluster_matrix = new_cluster_matrix
        cluster_size = new_cluster_size

        # get the number of clusters and size of the DSM
        n_clusters = cluster_matrix.mat.shape[0]
        DSM_size = cluster_matrix.mat.shape[1]
        total_coord_cost = 0
        coordination_cost = np.zeros([1, DSM_size])
        
        # Calculate the cost of the solution
        
        for i in range(DSM_size): 
            for j in range(i+1, DSM_size): 
                if dsm_matrix.mat[i,j] > 0 or dsm_matrix.mat[j,i] > 0: 
                    cost_total = 0
                    
                    for cluster_index in range(n_clusters): 
                        if cluster_matrix.mat[cluster_index,i]+cluster_matrix(cluster_index,j] == 2: 
                            cost_total += dsm_matrix.mat[i,j] + dsm_matrix.mat[j,i]
                    
                    if cost_total > 0: 
                        cost_c = cost_total
                    else: 
                        cost_c = (dsm_matrix.mat[i,j] + dsm_matrix.mat[j,i])*DSM_size^pow_cc
                    coordination_cost[i] += cost_c

        total_coord_cost = np.sum(coordination_cost)
        return total_coord_cost 
        
    def _make_bid(self):
        pass

    def cluster(self):
        pass
