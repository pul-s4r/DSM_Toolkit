from dsm_helper_classes import *
import copy
import numpy as np
import sys

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
        self._total_coord_cost = ClusterGenerator._coord_cost(self._dsm_mat, self._cluster_mat, self._params)
        self._best_coord_cost = self._total_coord_cost

        self._cost_history = np.zeros([10000, 1])
        self._history_index = 0

        # Store the best cluster matrix and corresponding cost and size
        self._best_curr_cost = self._total_coord_cost
        self._best_curr_cluster_mat = self._cluster_mat
        self._best_curr_cluster_size = self._cluster_size

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
    def _coord_cost(DSM_matrix, cluster_matrix, params):
        """
        Calculate the coordination cost of the cluster matrix.
        This routine checks all DSM interactions and adds to a total the cost of all intra-cluster interactions. Interactions outside of clusters are assigned a higher cost.
        As per Thebeau (2000) the cost formula is, for each interdependent/coupled activity i and j:
        (In cluster) (DSM[i] + DSM[j])*cluster_size[cluster_n]^pow_cc
        (Out of cluster) (DSM[i] + DSM[j])*DSM_size^pow_cc
        Sum each term to obtain the total.
        """
        assert isinstance(DSM_matrix, DSMMatrix)
        assert isinstance(cluster_matrix, ClusterMatrix)
        assert isinstance(params, ClusterParameters)

        if params:
            pow_cc = params.pow_cc
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

        num_cluster_elements = np.sum(cluster_matrix.mat, axis=1, dtype=np.int)
        n = 0 # indexing starts from zero
        new_cluster_mat = ClusterMatrix.from_mat(np.zeros([new_DSM_size, new_DSM_size]))

        # Create a new cluster matrix that matches the reordered DSM matrix
        #

        # formerly n_clusters - changed due to shape
        # Check again to replicate MATLAB functionality - this is not a permanent fix
        for i in range(n_clusters):
            if i < new_DSM_size:
                new_cluster_mat.mat[i,n:n+num_cluster_elements[i]] = np.ones([1, num_cluster_elements[i]])
                n += num_cluster_elements[i]
            else:
                new_cluster_mat.mat = np.vstack([new_cluster_mat.mat, np.zeros(new_cluster_mat.mat.shape[1])])
                new_cluster_mat.mat[i,n:n+num_cluster_elements[i]] = np.ones([1, num_cluster_elements[i]])
                n += num_cluster_elements[i]

        # import pdb; pdb.set_trace()
        # get new cluster size array matching matrix
        # new_cluster_size = np.sum(new_cluster_mat.mat, axis=1)
        new_cluster_mat.update_cluster_size()

        # replace old data with new data for cost calculation
        DSM_matrix = new_DSM_matrix
        DSM_size = new_DSM_size
        cluster_matrix = new_cluster_mat
        # cluster_size = new_cluster_size

        # get the number of clusters and size of the DSM
        n_clusters = cluster_matrix.mat.shape[0]
        DSM_size = cluster_matrix.mat.shape[1]
        total_coord_cost = 0
        coordination_cost = np.zeros([DSM_size, 1])

        # Calculate the cost of the solution
        for i in range(DSM_size):
            for j in range(i+1, DSM_size):
                if DSM_matrix.mat[i,j] > 0 or DSM_matrix.mat[j,i] > 0:
                    cost_total = 0

                    for cluster_index in range(n_clusters):
                        if cluster_matrix.mat[cluster_index,i]+cluster_matrix.mat[cluster_index,j] == 2:
                            # cost_total += (DSM_matrix.mat[i,j] + DSM_matrix.mat[j,i]) * cluster_size[cluster_index]**pow_cc
                            cost_total += (DSM_matrix.mat[i,j] + DSM_matrix.mat[j,i]) * cluster_matrix.cluster_size[cluster_index]**pow_cc

                    if cost_total > 0:
                        cost_c = cost_total
                    else:
                        cost_c = (DSM_matrix.mat[i,j] + DSM_matrix.mat[j,i])*DSM_size**pow_cc
                    coordination_cost[i] += cost_c

        total_coord_cost = np.sum(coordination_cost)
        return total_coord_cost

    def _make_bid(self, elmt, DSM_matrix, cluster_matrix):
        # note already has self.params
        assert isinstance(DSM_matrix, DSMMatrix)
        assert isinstance(cluster_matrix, ClusterMatrix)

        n_clusters = cluster_matrix.mat.shape[0]
        DSM_size = cluster_matrix.mat.shape[1]

        cluster_bid = np.zeros([n_clusters, 1])

        # For each cluster, if any element in the cluster has an interaction with
        # the selected element then add the number of interactions with the selected
        # element. Then use the number of interactions to calculate the bid.
        for i in range(n_clusters):
            var_in = 0
            var_out = 0
            # If element j is in cluster i, need j != element to avoid diagonal
            for j in range(DSM_size):
                if cluster_matrix.mat[i,j] == 1 and j != elmt:
                    if DSM_matrix.mat[j, elmt] > 0:
                        var_in += DSM_matrix.mat[j, elmt];
                    if DSM_matrix.mat[elmt, j] > 0:
                        var_out += DSM_matrix.mat[elmt, j]

            # If there were any interactions with cluster members, make a bid
            if var_in > 0 or var_out > 0:
                # if cluster_size[i] == self._params.max_cluster_size:
                if cluster_matrix.cluster_size[i] == self._params.max_cluster_size:
                    cluster_bid[i] = 0
                else:
                    cluster_bid[i] = ( (var_in+var_out)**self._params.pow_dep \
                        /(cluster_matrix.cluster_size[i]**self._params.pow_bid) )

        return cluster_bid

    def delete_clusters(self, cluster_mat):
        cluster_matrix = ClusterMatrix.from_mat(cluster_mat.mat)
        n_clusters = cluster_matrix.mat.shape[0]
        n_elements = cluster_matrix.mat.shape[1]

        # import pdb; pdb.set_trace()
        cluster_size = cluster_mat.cluster_size

        new_cluster_mat = ClusterMatrix.from_mat(np.zeros([n_clusters, n_elements]))
        new_cluster_size = np.zeros([n_clusters])

        # If clusters are equal or cluster j is completely contained in i
        # Delete cluster j
        for i in range(n_clusters):
            for j in range(i+1, n_clusters):
                if cluster_size[i] >= cluster_size[j] and cluster_size[j] > 0:
                    if (np.logical_and(cluster_matrix.mat[i,:], \
                        cluster_matrix.mat[j,:]) == cluster_matrix.mat[j,:]
                        ).all():
                        cluster_matrix.mat[j,:] = 0
                        cluster_size[j] = 0

        # If cluster i is completely contained in j
        # Delete cluster i
        for i in range(n_clusters):
            for j in range(i+1, n_clusters):
                if cluster_size[i] < cluster_size[j] and cluster_size[i] > 0:
                    if (np.logical_and(cluster_matrix.mat[i,:], \
                        cluster_matrix.mat[j,:]) == cluster_matrix.mat[i,:]
                        ).all():
                        cluster_matrix.mat[i,:] = 0
                        cluster_size[i] = 0

        # Delete clusters with no tasks
        non_empty_cluster_index = np.array(cluster_size != 0)

        new_cluster_mat.mat[0:np.sum(non_empty_cluster_index),:] = cluster_matrix.mat[non_empty_cluster_index.flatten(),:]
        new_cluster_size[0:np.sum(non_empty_cluster_index)] = cluster_size[non_empty_cluster_index.flatten()]

        new_cluster_mat.cluster_size = new_cluster_size
        # new_cluster_mat.update_cluster_size()

        return new_cluster_mat

    def cluster(self, DSM_matrix):
        assert isinstance(DSM_matrix, DSMMatrix)

        DSM_size = DSM_matrix.mat.shape[1]
        n_clusters = DSM_size
        max_repeat = 10

        # Initialise states/history
        coordination_cost = np.zeros([DSM_size, 1])
        cluster_size = np.zeros([DSM_size, 1])
        new_cluster_mat = ClusterMatrix.from_mat(np.zeros([n_clusters, n_clusters]))
        new_cluster_size = np.zeros([DSM_size,1])
        cluster_bid = np.zeros([DSM_size,1])
        new_cluster_bid = np.zeros([DSM_size,1])
        new_coordination_cost = np.zeros([DSM_size,1])
        rnd_elmt_arr = np.zeros([DSM_size,1])
        cluster_list = np.zeros([DSM_size,1])

        # # Initialise cluster matrix (note this is already initialised at the start of the function, need to decide whether to use or not)
        cluster_diagonals = np.ones([1, self._n_clusters])
        cluster_mat = ClusterMatrix.from_mat(np.diag(cluster_diagonals.flatten()))
        cluster_mat.update_cluster_size()
        cluster_size = np.ones([self._n_clusters, 1])

        # # Initial clustering starting cost
        total_coord_cost = ClusterGenerator._coord_cost(DSM_matrix, cluster_mat, self._params)
        best_coord_cost = total_coord_cost

        # # Initialise cost history
        cost_history = np.zeros([10000, 1])
        history_index = 0

        # # Store the best cluster matrix and corresponding cost and size
        best_curr_cost = total_coord_cost
        best_curr_cluster_mat = cluster_mat
        best_curr_cluster_size = cluster_size

        # Initialise control parameters
        stable = 0;			#	toggle to indicate if the algorithm has met the stability criteria
        change = 0;			#	toggle to indicate if a change should be made
        accept1= 0;			#	toggle to indicate if the solution should be acccepted
        first_run = 1;		#	toggle to indicate if it is the first run through
        attempt = 0;		#	index to count the number of passes through the algorithm

        # Initialise best cost history
        cluster_matrix_history = []
        cluster_size_history = []
        total_coord_cost_history = []
        cluster_matrix_history.append(cluster_mat)
        cluster_size_history.append(cluster_size)
        total_coord_cost_history.append(total_coord_cost)

        # import pdb; pdb.set_trace()
        while total_coord_cost > best_coord_cost and attempt <= max_repeat or first_run == 1:
            if first_run == 0:
                cluster_matrix_history.append(cluster_mat)
                cluster_size_history.append(cluster_size)
                total_coord_cost_history.append(total_coord_cost)
                total_coord_cost 	= best_curr_cost
                cluster_mat 	= best_curr_cluster_mat.copy()
                # cluster_mat.cluster_size = best_cluster_size.copy()
                # cluster_mat.update_cluster_size()
                cluster_size 		= best_cluster_size.copy()
                history_index 		= history_index+1
                cost_history[history_index,0] = total_coord_cost

            first_run = 0
            stable = 0
            accept1 = 0
            change = 0


            print("Attempt: " + str(attempt))
            while stable <= self._params.stable_limit:
                for k in range(DSM_size*self._params.times):
                    # print("Total coord cost: " + str(total_coord_cost) + ", stable: " + str(stable) + ", change: ", str(change))

                    cluster_mat.update_cluster_size()

                    elmt = np.ceil(np.random.randint(low=0, high=DSM_size-1))
                    elmt = int(elmt)
                    cluster_bid = self._make_bid(elmt, DSM_matrix, cluster_mat)

                    best_cluster_bid = np.max(cluster_bid)
                    second_best_cluster_bid = np.max(cluster_bid[cluster_bid != best_cluster_bid]) if cluster_bid[cluster_bid != best_cluster_bid].shape[0] else 0

                    if np.floor(self._params.rand_bid * np.random.uniform()) == 0:
                        best_cluster_bid = second_best_cluster_bid

                    if best_cluster_bid > 0:
                        # Determine if the bid is acceptable
                        cluster_list[:,0] = 0
                        # Determine the list of clusters affected
                        cluster_list[0:n_clusters,0] = np.logical_and((cluster_bid == best_cluster_bid).flatten(), (cluster_mat.mat[:,elmt] == 0).flatten())

                        # copy the cluster matrix into new matrices
                        new_cluster_mat = cluster_mat.copy()
                        new_cluster_mat = cluster_mat.copy()
                        new_cluster_size = cluster_size

                        # proceed with cluster changes in the new cluster
                        new_cluster_mat.mat[0:n_clusters, elmt] = np.logical_or(new_cluster_mat.mat[0:n_clusters, elmt].flatten(), cluster_list.flatten())
                        new_cluster_mat.update_cluster_size()
                        new_cluster_size[0:n_clusters,0] = new_cluster_size[0:n_clusters,0] + (cluster_list == 1).flatten()*1

                        # import pdb; pdb.set_trace()
                        # delete duplicate and empty clusters
                        new_cluster_mat = self.delete_clusters(new_cluster_mat)

                        # determine the change in the coordination cost
                        new_total_coord_cost = ClusterGenerator._coord_cost(DSM_matrix, new_cluster_mat, self._params)
                        if new_total_coord_cost <= total_coord_cost:
                            accept1 = 1
                        else:
                            # still accept 1 out of approx random_accept times
                            if (np.floor(self._params.rand_accept*np.random.uniform()) == 0):
                                accept1 = 1
                                # if we are going to accept a total cost that is not less than our current cost
                                #  then
                                # save the current cost as the best current cost found so far (only if the current cost
                                # is lower than any best current cost previously saved) because we may not find
                                # a cost that is better than the current cost.
                                # When we think we are finished we will check the final cost against any best cost
                                # if the final cost is not better than the lowest cost found, then we will move back to that best cost
                                if total_coord_cost < best_curr_cost:
                                    best_curr_cost = total_coord_cost
                                    best_curr_cluster_mat = cluster_mat
                                    best_cluster_size = cluster_size
                                else:
                                    accept1 = 0

                    if accept1 == 1:
                        accept1 = 0

                        # Update the clusters
                        total_coord_cost = new_total_coord_cost
                        cluster_mat = new_cluster_mat.copy()
                        cluster_size = new_cluster_size
                        history_index += 1
                        cost_history[history_index,0] = total_coord_cost

                        if (best_coord_cost > total_coord_cost):
                            best_coord_cost = total_coord_cost
                            change += 1

                # Test the system for instability
                if change > 0:
                    stable = 0
                    change = 0
                else:
                    stable += 1

                    pass

                attempt += 1
            pass
        return (cluster_mat, total_coord_cost, cost_history)


        pass
