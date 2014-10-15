from scipy.spatial import KDTree

from . import InterestModel
from ..exceptions import ExplautoBootstrapError

# TODO: pick code from PyCDLL

def iter_tree(tree):
    " Return a generator from a KDTree.node instance"
    yield tree
    if isinstance(tree, KDTree.innernode):
        for node in iter_tree(tree.less):
            yield node
        for node in iter_tree(tree.greater):
            yield node

class RIAC(InterestModel):
    def __init__(self, conf, expl_dims, leaf_size =70):
        self.data = zeros((10000, len(expl_dims)))
        self.leaf_size = leaf_size
        self.conf = conf
        self.t = 0

    def sample():
        if self.t < 1:
            raise ExplautoBootstrapError("RIAC model not bootstraped yet (need more update(.) calls)")
        self.kdtree = KDTree(self.data, self.leaf_size)
        for node in iter_tree(self.kdtree.tree):
            if isinstance(node, KDTree.leafnode):
                if len(node.idx) >= self.leaf_size / 2.:
                    cells['node']
