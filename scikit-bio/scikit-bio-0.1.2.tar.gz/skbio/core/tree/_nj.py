from __future__ import absolute_import, division, print_function

# ----------------------------------------------------------------------------
# Copyright (c) 2013--, scikit-bio development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

import numpy as np

from skbio.core.distance import DistanceMatrix
from skbio.core.tree import TreeNode


def nj(dm, disallow_negative_branch_length=True, result_constructor=None):
    """ Apply neighbor joining for phylogenetic reconstruction.

    Parameters
    ----------
    dm : skbio.core.distance.DistanceMatrix
        Input distance matrix containing distances between OTUs.
    disallow_negative_branch_length : bool, optional
        Neighbor joining can result in negative branch lengths, which don't
        make sense in an evolutionary context. If `True`, negative branch
        lengths will be returned as zero, a common strategy for handling this
        issue that was proposed by the original developers of the algorithm.
    result_constructor : function, optional
        Function to apply to construct the result object. This must take a
        newick-formatted string as input. The result of applying this function
        to a newick-formatted string will be returned from this function. This
        defaults to ``TreeNode.from_newick``.

    Returns
    -------
    TreeNode
        By default, the result object is a `TreeNode`, though this can be
        overridden by passing `result_constructor`.

    See Also
    --------
    TreeNode.root_at_midpoint

    Notes
    -----
    Neighbor joining was initially described in Saitou and Nei (1987) [1]_. The
    example presented here is derived from the Wikipedia page on neighbor
    joining [2]_. The Phylip manual also describes the method [3]_ and Phylip
    itself provides an implementation which is useful for comparison.

    Neighbor joining, by definition, creates unrooted trees. One strategy for
    rooting the resulting trees is midpoint rooting, which is accessible as
    ``TreeNode.root_at_midpoint``.

    References
    ----------
    .. [1] Saitou N, and Nei M. (1987) "The neighbor-joining method: a new
       method for reconstructing phylogenetic trees." Molecular Biology and
       Evolution. PMID: 3447015.
    .. [2] http://en.wikipedia.org/wiki/Neighbour_joining
    .. [3] http://evolution.genetics.washington.edu/phylip/doc/neighbor.html

    Examples
    --------
    Define a new distance matrix object describing the distances between five
    OTUs: a, b, c, d, and e.

    >>> from skbio.core.distance import DistanceMatrix
    >>> from skbio.core.tree import nj

    >>> data = [[0,  5,  9,  9,  8],
    ...         [5,  0, 10, 10,  9],
    ...         [9, 10,  0,  8,  7],
    ...         [9, 10,  8,  0,  3],
    ...         [8,  9,  7,  3,  0]]
    >>> ids = list('abcde')
    >>> dm = DistanceMatrix(data, ids)

    Contstruct the neighbor joining tree representing the relationship between
    those OTUs. This is returned as a TreeNode object.

    >>> tree = nj(dm)
    >>> print(tree.ascii_art())
              /-d
             |
             |          /-c
             |---------|
    ---------|         |          /-b
             |          \--------|
             |                    \-a
             |
              \-e

    Again, construct the neighbor joining tree, but instead return the newick
    string representing the tree, rather than the TreeNode object. (Note that
    in this example the string output is truncated when printed to facilitate
    rendering.)

    >>> newick_str = nj(dm, result_constructor=str)
    >>> print(newick_str[:55], "...")
    (d:2.000000, (c:4.000000, (b:3.000000, a:2.000000):3.00 ...

    """
    if dm.shape[0] < 3:
        raise ValueError(
            "Distance matrix must be at least 3x3 to "
            "generate a neighbor joining tree.")

    if result_constructor is None:
        result_constructor = TreeNode.from_newick

    # initialize variables
    node_definition = None

    # while there are still more than three distances in the distance matrix,
    # join neighboring nodes.
    while(dm.shape[0] > 3):
        # compute the Q matrix
        q = _compute_q(dm)

        # identify the pair of nodes that have the lowest Q value. if multiple
        # pairs have equally low Q values, the first pair identified (closest
        # to the top-left of the matrix) will be chosen. these will be joined
        # in the current node.
        idx1, idx2 = _lowest_index(q)
        pair_member_1 = dm.ids[idx1]
        pair_member_2 = dm.ids[idx2]
        # determine the distance of each node to the new node connecting them.
        pair_member_1_len, pair_member_2_len = _pair_members_to_new_node(
            dm, idx1, idx2, disallow_negative_branch_length)
        # define the new node in newick style
        node_definition = "(%s:%f, %s:%f)" % (pair_member_1,
                                              pair_member_1_len,
                                              pair_member_2,
                                              pair_member_2_len)
        # compute the new distance matrix, which will contain distances of all
        # other nodes to this new node
        dm = _compute_collapsed_dm(
            dm, pair_member_1, pair_member_2,
            disallow_negative_branch_length=disallow_negative_branch_length,
            new_node_id=node_definition)

    # When there are three distances left in the distance matrix, we have a
    # fully defined tree. The last node is internal, and its distances are
    # defined by these last three values.
    # First determine the distance between the last two nodes to be joined in
    # a pair...
    pair_member_1 = dm.ids[1]
    pair_member_2 = dm.ids[2]
    pair_member_1_len, pair_member_2_len = \
        _pair_members_to_new_node(dm, pair_member_1, pair_member_2,
                                  disallow_negative_branch_length)
    # ...then determine their distance to the other remaining node, but first
    # handle the trival case where the input dm was only 3 x 3
    node_definition = node_definition or dm.ids[0]
    internal_len = _otu_to_new_node(
        dm, pair_member_1, pair_member_2, node_definition,
        disallow_negative_branch_length=disallow_negative_branch_length)
    # ...and finally create the newick string describing the whole tree.
    newick = "(%s:%f, %s:%f, %s:%f);" % (pair_member_1, pair_member_1_len,
                                         node_definition, internal_len,
                                         pair_member_2, pair_member_2_len)

    # package the result as requested by the user and return it.
    return result_constructor(newick)


def _compute_q(dm):
    """Compute Q matrix, used to identify the next pair of nodes to join.

    """
    q = np.zeros(dm.shape)
    n = dm.shape[0]
    for i in range(n):
        for j in range(i):
            q[i, j] = q[j, i] = \
                ((n - 2) * dm[i, j]) - dm[i].sum() - dm[j].sum()
    return DistanceMatrix(q, dm.ids)


def _compute_collapsed_dm(dm, i, j, disallow_negative_branch_length,
                          new_node_id):
    """Return the distance matrix resulting from joining ids i and j in a node.

    If the input distance matrix has shape ``(n, n)``, the result will have
    shape ``(n-1, n-1)`` as the ids `i` and `j` are collapsed to a single new
    ids.

    """
    in_n = dm.shape[0]
    out_n = in_n - 1
    out_ids = [new_node_id]
    out_ids.extend([e for e in dm.ids if e not in (i, j)])
    result = np.zeros((out_n, out_n))
    for idx1, out_id1 in enumerate(out_ids[1:]):
        result[0, idx1 + 1] = result[idx1 + 1, 0] = _otu_to_new_node(
            dm, i, j, out_id1, disallow_negative_branch_length)
        for idx2, out_id2 in enumerate(out_ids[1:idx1+1]):
            result[idx1+1, idx2+1] = result[idx2+1, idx1+1] = \
                dm[out_id1, out_id2]
    return DistanceMatrix(result, out_ids)


def _lowest_index(dm):
    """Return the index of the lowest value in the input distance matrix.

    If there are ties for the lowest value, the index of top-left most
    occurrence of that value will be returned.

    This should be ultimately be replaced with a new DistanceMatrix object
    method (#228).

    """
    lowest_value = np.inf
    for i in range(dm.shape[0]):
        for j in range(i):
            curr_index = i, j
            curr_value = dm[curr_index]
            if curr_value < lowest_value:
                lowest_value = curr_value
                result = curr_index
    return result


def _otu_to_new_node(dm, i, j, k, disallow_negative_branch_length):
    """Return the distance between a new node and some other node.

    Parameters
    ----------
    dm : skbio.core.distance.DistanceMatrix
        The input distance matrix.
    i, j : str
        Identifiers of entries in the distance matrix to be collapsed. These
        get collapsed to a new node, internally represented as `u`.
    k : str
        Identifier of the entry in the distance matrix for which distance to
        `u` will be computed.
    disallow_negative_branch_length : bool
        Neighbor joining can result in negative branch lengths, which don't
        make sense in an evolutionary context. If `True`, negative branch
        lengths will be returned as zero, a common strategy for handling this
        issue that was proposed by the original developers of the algorithm.

    """
    k_to_u = 0.5 * (dm[i, k] + dm[j, k] - dm[i, j])

    if disallow_negative_branch_length and k_to_u < 0:
        k_to_u = 0

    return k_to_u


def _pair_members_to_new_node(dm, i, j, disallow_negative_branch_length):
    """Return the distance between a new node and decendants of that new node.

    Parameters
    ----------
    dm : skbio.core.distance.DistanceMatrix
        The input distance matrix.
    i, j : str
        Identifiers of entries in the distance matrix to be collapsed (i.e.,
        the descendents of the new node, which is internally represented as
        `u`).
    disallow_negative_branch_length : bool
        Neighbor joining can result in negative branch lengths, which don't
        make sense in an evolutionary context. If `True`, negative branch
        lengths will be returned as zero, a common strategy for handling this
        issue that was proposed by the original developers of the algorithm.

    """
    n = dm.shape[0]
    i_to_j = dm[i, j]
    i_to_u = (0.5 * i_to_j) + ((dm[i].sum() - dm[j].sum()) / (2 * (n - 2)))

    if disallow_negative_branch_length and i_to_u < 0:
        i_to_u = 0

    j_to_u = i_to_j - i_to_u

    if disallow_negative_branch_length and j_to_u < 0:
        j_to_u = 0

    return i_to_u, j_to_u
