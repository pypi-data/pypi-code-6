import pydecode.model
import numpy as np

def test_sparse_feature():
    label_features = [(np.array([1,2,3]), np.array([2,1,4])),
                      (np.array([3,1,3]), np.array([2,2,4]))]
    templates = [(5,10), (10, 5)]
    res = pydecode.model.sparse_feature_indices(label_features, templates)
    res2 = np.array([[12, 67], [21, 57], [34, 69]])
    assert (res == res2).all()
    res = pydecode.model.sparse_feature_indices(label_features, templates, 50)
    res2 = np.array([[12, 17], [21, 7], [34, 19]])
    assert (res == res2).all()

    w = np.zeros((50, 1))
    w += pydecode.model.fast_vector(res, 50)
    assert (w[19] == 1)
    assert (w[0] == 0)
    print w.T
    assert False
