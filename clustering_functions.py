from dsm_helper_classes import *
import copy 
import numpy as np

class ClusterGenerator(object):         
    _dsm_mat = None
    _cluster_mat = None
    _params = None
    
    def __init__(self, dsm_mat = None, default_size = 2):  
        if isinstance(dsm_mat, DSMMatrix): 
            self._dsm_mat = dsm_mat
        else: 
            self._dsm_mat = DSMMatrix.from_size(default_size)
        
        max_size = self._dsm_mat.mat.shape[0]
        self._params = set_default_cluster_parameters(max_size)
    
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
        assert param_object.max_cluster_size == self._dsm_mat.mat.shape[0]
        self._params = param_object

    def coord_cost(self): 
        pass

    def make_bid(self):
        pass

    def cluster(self):
        pass
