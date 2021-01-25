# """ Tests for the implemented functions
# """
import unittest
import pdb, traceback, sys

from clustering_functions import *
from ClusterParameters import ClusterParameters, set_default_cluster_parameters
from ClusterMatrix import ClusterMatrix
from DSMMatrix import DSMMatrix
from plotting_functions import *

# Test case for DSMMatrix.reorder_by_cluster
class DSMReorderTestCase(unittest.TestCase):
    def test_reorder1(self):
        # d_mat = np.identity(3)
        d_mat = np.array([[1, 0, 0, 0], [0, 0, 0, 0], [1, 0, 1, 0], [0, 0, 1, 1]])
        d_list = ["1", "2", "3", "4"]
        d = DSMMatrix(d_mat, d_list)
        # print("Original DSM: ")
        # print(d.mat)

        c_mat = np.array([[1, 0, 1, 1], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        c = ClusterMatrix.from_mat(c_mat)
        # print("Original Cluster: ")
        # print(c.mat)

        new_d_mat = DSMMatrix.reorder_by_cluster(d, c)
        # print("Reordered DSM: ")
        # print(new_d_mat.mat)
        # print(new_d_mat.labels)
        val_comp_1 = new_d_mat.mat == np.array([[0, 0, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]])
        lab_comp_1 = new_d_mat.labels == ['1', '3', '4', '2']
        assert val_comp_1.all()
        assert lab_comp_1

    def test_reorder2(self):
        d_mat_2 = np.array([[1, 0, 0, 1], [0, 0, 0, 0], [1, 0, 1, 0], [0, 0, 1, 1]])
        d_list_2 = ["1", "2", "3", "4"]
        d_2 = DSMMatrix(d_mat_2, d_list_2)
        # print("Original DSM: ")
        # print(d_2.mat)

        c_mat_2 = np.array([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]])
        c_2 = ClusterMatrix.from_mat(c_mat_2)
        # print("Original Cluster: ")
        # print(c_2.mat)

        new_d_mat_2 = DSMMatrix.reorder_by_cluster(d_2, c_2)
        # print("Reordered DSM: ")
        # print(new_d_mat_2.mat)
        # print(new_d_mat_2.labels)
        val_comp_2 = new_d_mat_2.mat == np.array([[0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 0, 0], [1, 0, 0, 0]])
        lab_comp_2 = new_d_mat_2.labels == ['4', '3', '2', '1']
        assert val_comp_2.all()
        assert lab_comp_2


# Test case for ClusterMatrix.reorder
class ClusterReorderTestCase(unittest.TestCase):
    def test_reorder1(self):
        c_mat = np.array([[1, 1, 0], [1, 0, 1], [1, 1, 1]])
        c = ClusterMatrix.from_mat(c_mat)
        new_c_mat = ClusterMatrix.reorder(c)
        # print("Original: ")
        # print(c.mat)
        # print("Reordered: ")
        # print(new_c_mat.mat)
        # print("Reordered size: ")
        # print(new_c_mat.cluster_size)
        val_comp = new_c_mat.mat == np.array([c_mat[2], c_mat[1], c_mat[0]])
        size_comp = new_c_mat.cluster_size == np.array([3, 2, 2])
        assert val_comp.all()
        assert size_comp.all()

    def test_reorder2(self):
        c_mat_2 = np.array([[1, 1, 0], [0, 1, 0], [1, 1, 1]])
        c_2 = ClusterMatrix.from_mat(c_mat_2)
        new_c_mat_2 = ClusterMatrix.reorder(c_2)

        # print("Original: ")
        # print(c_2.mat)
        # print("Reordered: ")
        # print(new_c_mat_2.mat)
        # print("Reordered size: ")
        # print(new_c_mat_2.cluster_size)

        val_comp_2 = new_c_mat_2.mat == np.array([c_mat_2[2], c_mat_2[0], c_mat_2[1]])
        size_comp_2 = new_c_mat_2.cluster_size == np.array([3, 2, 1])
        assert val_comp_2.all()
        assert size_comp_2.all()

    def test_invariance(self):
        # Checks that a new cluster matrix (once reordered) is invariant under reordering
        c_mat = np.array([[1, 1, 0], [1, 0, 1], [1, 1, 1]])
        c = ClusterMatrix.from_mat(c_mat)
        new_c_mat = ClusterMatrix.reorder(c)
        # import pdb; pdb.set_trace()
        newer_c_mat = ClusterMatrix.reorder(new_c_mat)
        # print(newer_c_mat.mat)
        assert (newer_c_mat.mat == new_c_mat.mat).all()


# Tests for dsm_helper_classes
class ClusterParametersTestCase(unittest.TestCase):
    # raise NotImplementedError
    pass

class DSMMatrixTestCase(unittest.TestCase):
    def test_manual_labels(self):
        d_mat = np.array([[1, 0, 0, 0], [0, 0, 0, 0], [1, 0, 1, 0], [0, 0, 1, 1]])
        d_list = ["a", "b", "c", "d"]
        d = DSMMatrix(d_mat, activity_labels=d_list)
        # print(d.labels)

    def test_auto_labels(self):
        d2_mat = np.array([[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 1, 0], [0, 0, 1, 1]])
        d2 = DSMMatrix(d2_mat)
        # print(d2.labels)
        assert d2.labels == ['1', '2', '3', '4']

    def test_from_size(self):
        d = DSMMatrix.from_size(3)
        # print(d.mat)

    def test_setunset(self):
        d_mat = np.array([[1, 0, 0, 0], [0, 0, 0, 0], [1, 0, 1, 0], [0, 0, 1, 1]])
        d_list = ["a", "b", "c", "d"]
        d = DSMMatrix(d_mat, activity_labels=d_list)
        d_mat[1,0] = 1
        d.set(1, 0)
        assert (d.mat == np.array([[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 1, 0], [0, 0, 1, 1]])).all()
        d_mat[2,1] = 1
        d.set(2, 1)
        assert (d.mat == np.array([[1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 1, 0], [0, 0, 1, 1]])).all()
        d_mat[3,2] = 0
        d.unset(3, 2)
        assert (d.mat == np.array([[1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 1, 0], [0, 0, 0, 1]])).all()
        # d_mat[3,2] = 0
        self.assertRaises(ArithmeticError, d.unset, 4, 6)
        self.assertRaises(ArithmeticError, d.unset, -1, 0)

    def test_clear_systemelems(self):
        d_mat = np.array([[1, 0, 1, 0], [1, 1, 1, 0], [1, 1, 1, 0], [0, 0, 1, 1]])
        d = DSMMatrix(d_mat)
        d.clear_elements([0])
        assert (d.mat == np.array([[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 1, 1]])).all()
        d.clear_elements([1, 3])
        # print(d.mat)
        assert (d.mat == np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 0]])).all()
        d.clear_elements([])
        assert (d.mat == np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 0]])).all()
        self.assertRaises(AssertionError, d.clear_elements, ["e"])
        self.assertRaises(AssertionError, d.clear_elements, ["2", 1])
        self.assertRaises(AssertionError, d.clear_elements, [6])

# class ClusterMatrixTestCase(unittest.TestCase):
    # raise NotImplementedError

# # Tests for clustering_functions
# class BidTestCase(unittest.TestCase):
    # raise NotImplementedError

class ClusterTestCase(unittest.TestCase):
    def test_cluster(self):
        d_mat = np.array([
            [1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 1, 0, 0],
            [0, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0],
            [0, 0, 0, 1, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 1, 1]
        ])
        d_list = ["a", "b", "c", "d", "e", "f", "g", "h"]
        d = DSMMatrix(d_mat, activity_labels=d_list)
        # print(d.mat.shape)

        cg = ClusterGenerator(dsm_mat = d)
        # print(cg.dsm.mat)
        # print(cg._coord_cost(cg.params))
        # print(cg._cluster_list)
        # print(cg._cluster_mat.mat.shape)

    def test_coord_cost(self):
        d_mat = np.array([
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0],
            [0, 0, 0, 1, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 1, 1]
        ])
        d_list = ["a", "b", "c", "d", "e", "f", "g", "h"]
        d = DSMMatrix(d_mat, activity_labels=d_list)

        c_mat = np.diag(np.ones([8]))
        c = ClusterMatrix.from_mat(c_mat)
        pow_cc = 1

        cg = ClusterGenerator(dsm_mat = d)

        initial_cost = ClusterGenerator._coord_cost(d, c, cg.params)
        assert(initial_cost == 64)


        d_mat = np.array([
            [1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 0, 0, 0],
            [1, 0, 0, 1, 0, 0, 1, 0],
            [0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 1, 1]
        ])
        d_list = ["a", "b", "c", "d", "e", "f", "g", "h"]
        d = DSMMatrix(d_mat, activity_labels=d_list)

        c_mat = np.diag(np.ones([8]))
        c = ClusterMatrix.from_mat(c_mat)
        pow_cc = 1

        # cg = ClusterGenerator(dsm_mat = d)

        initial_cost = ClusterGenerator._coord_cost(d, c, cg.params)
        assert(initial_cost == 80)

    def test_coord_cost_2(self):
        d_mat = np.array([
            [1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 0, 0, 0],
            [1, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ])
        d_list = ["a", "b", "c", "d", "e", "f", "g", "h"]
        d = DSMMatrix(d_mat, activity_labels=d_list)

        c_mat = np.array([
            [1., 0., 1., 0., 0., 0., 0., 0.],
            [0., 1., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 1., 0., 0., 0., 0.],
            [0., 0., 0., 0., 1., 0., 0., 0.],
            [0., 0., 0., 0., 0., 1., 0., 0.],
            [0., 0., 0., 0., 0., 0., 1., 0.],
            [0., 0., 0., 0., 0., 0., 0., 1.],
            [0., 0., 0., 0., 0., 0., 0., 0.]
          ])
        c = ClusterMatrix.from_mat(c_mat)
        pow_cc = 1

        cg = ClusterGenerator(dsm_mat = d)

        # import pdb; pdb.set_trace()
        initial_cost = ClusterGenerator._coord_cost(d, c, cg.params)
        print(initial_cost)
        assert(initial_cost == 20)

    def test_bid(self):
        d_mat = np.array([
            [1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 1, 0, 0],
            [1, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ])
        d_list = ["a", "b", "c", "d", "e", "f", "g", "h"]
        d = DSMMatrix(d_mat, activity_labels=d_list)
        c_mat = np.diag(np.ones([8]))
        c = ClusterMatrix.from_mat(c_mat)

        cg = ClusterGenerator(
            dsm_mat = d)
        cg.params = ClusterParameters(
            pow_cc = 1,
            pow_bid = 1,
            pow_dep = 4,
            max_cluster_size = 16,
            rand_accept = 32,
            rand_bid = 32,
            times = 2,
            stable_limit = 2,
            max_repeat = 10
        )

        elmt = 7
        cluster_bid = cg._make_bid(elmt, d, c)
        # print(cluster_bid)
        assert np.equal(cluster_bid, np.zeros([8, 1])).all()

        d_mat2 = np.array([
            [1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 0, 0, 0],
            [1, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ])
        d2 = DSMMatrix(d_mat2, activity_labels=d_list)
        cg2 = ClusterGenerator(
            dsm_mat = d2)
        cg2.params = ClusterParameters(
            pow_cc = 1,
            pow_bid = 1,
            pow_dep = 4,
            max_cluster_size = 16,
            rand_accept = 32,
            rand_bid = 32,
            times = 2,
            stable_limit = 2,
            max_repeat = 10
        )

        elmt = 0
        cluster_bid_2 = cg2._make_bid(elmt, d, c)
        # print("CB2: ", cluster_bid_2)
        assert np.equal(cluster_bid_2, np.array([[0],[0],[16],[1],[0],[0],[0],[0]])).all()

    def test_delete_clusters(self):
        c_mat = np.diag(np.ones([8]))
        c_mat[0, 3] = 1
        c_mat[5, 3] = 1
        c = ClusterMatrix.from_mat(c_mat)
        c_size = np.array([[2],[1],[1],[1],[1],[2],[1],[1]])

        cg = ClusterGenerator(default_size=8)

        new_c = cg.delete_clusters(c)
        new_c_size = new_c.cluster_size
        new_c_result_mat = np.array([
            [1, 0, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ])

        new_c_result = ClusterMatrix.from_mat(new_c_result_mat)
        new_c_size_result = np.array([2,1,1,1,2,1,1,0])
        assert np.equal(new_c.mat, new_c_result.mat).all()
        assert np.equal(new_c_size, new_c_size_result).all()

    def test_delete_clusters_2(self):
        c_mat = np.diag(np.ones([5]))
        c_mat[1, 0] = 1
        c = ClusterMatrix.from_mat(c_mat)

        cg = ClusterGenerator(default_size=8)

        # import pdb; pdb.set_trace()
        new_c = cg.delete_clusters(c)
        new_c_size = new_c.cluster_size
        new_c_result_mat = np.array([
            [1, 1, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0],
        ])

        new_c_result = ClusterMatrix.from_mat(new_c_result_mat)
        new_c_size_result = np.array([2,1,1,1,0])
        assert np.equal(new_c.mat, new_c_result.mat).all()
        assert np.equal(new_c_size, new_c_size_result).all()

    def test_delete_clusters_3(self):
        c_mat = np.array([
            [1, 1, 0, 0, 0],
            [0, 0, 1, 1, 1],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ])
        c = ClusterMatrix.from_mat(c_mat)

        cg = ClusterGenerator(default_size=8)

        new_c = cg.delete_clusters(c)
        new_c_size = new_c.cluster_size
        new_c_result_mat = np.array([
            [1, 1, 0, 0, 0],
            [0, 0, 1, 1, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ])

        new_c_result = ClusterMatrix.from_mat(new_c_result_mat)
        new_c_size_result = np.array([2,3,0,0,0])
        assert np.equal(new_c.mat, new_c_result.mat).all()
        assert np.equal(new_c_size, new_c_size_result).all()

    def test_cluster(self):
        d_mat = np.array([
            [1, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 0, 0, 0],
            [1, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ])
        d_list = ["a", "b", "c", "d", "e", "f", "g", "h"]
        d = DSMMatrix(d_mat, activity_labels=d_list)

        cg = ClusterGenerator(default_size=8)

        # try:
        (cluster_matrix, total_coord_cost, cost_history) = cg.cluster(d)
        # except:
        #     extype, value, tb = sys.exc_info()
        #     traceback.print_exc()
        #     pdb.post_mortem(tb)
            # pdb.runcall(DSMMatrix.reorder_by_cluster, DSM_matrix, cluster_matrix)

        c_mat_result = np.array([
            [1, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ])
        c_result = ClusterMatrix.from_mat(c_mat_result)
        c_size_result = np.array([[2],[1],[2],[1],[1],[1],[0],[0]])
        print(cluster_matrix.mat)

        # import pdb; pdb.set_trace()
        # assert np.equal(cluster_matrix.mat, c_result.mat).all()
        initial_cost = ClusterGenerator._coord_cost(d, cluster_matrix, cg.params)
        print("Cost: " + str(initial_cost))
        assert(initial_cost == 14 or initial_cost == 16)

    def test_place_diag(self):
        d_mat = np.array([
            [0, 0, 1, 0, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 1],
            [0, 0, 1, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [1, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0]
        ])
        d_list = ["a", "b", "c", "d", "e", "f", "g", "h"]
        d = DSMMatrix(d_mat, activity_labels=d_list)

        d_diag = DSMMatrix.place_diag(d)

        d_mat_result = np.array([
            [1, 0, 1, 0, 0, 1, 0, 1],
            [1, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0, 1],
            [0, 0, 1, 1, 0, 0, 0, 1],
            [0, 0, 0, 0, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 1, 0],
            [1, 0, 0, 1, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 0, 0, 1]
        ])
        d_result = DSMMatrix(d_mat_result, activity_labels=d_list)

        assert np.equal(d_diag.mat, d_result.mat).all()



if __name__ == "__main__":
    # CTC = ClusterTestCase()
    # CTC.test_cluster()
    # CTC.test_coord_cost_2()
    unittest.main()
