## AUTHOR  : Zhenfei Yuan, Taizhong Hu
## EMAIL   : zfyuan@mail.ustc.edu.cn; thu@ustc.edu.cn
## URL     : taizhonglab.ustc.edu.cn/software/pycounts.html
## DATE    : Mar, 17, 2013
## LICENCE : GPL (>= 2)


# TODO:
# 1. [DONE] new versions of networkx.draw will hide labels on default. Add the 'with_labels=True'.
# 2. [DONE] fix *rvine_sim* for vine trees with two variables.


import pandas as ps
import numpy             as np
import numpy.linalg
import networkx          as nx
import matplotlib.pyplot as plt
import bvcopula          as bvcop
from scipy.optimize import fmin
from scipy.stats    import norm
from scipy          import arctanh, tanh
from itertools      import combinations
import copy



def node_labels(node):
    """
    Extract variable labels from one node of the vine structure.
    
    Parameter
    ---------
    node : str. One node from vine structure
    
    Return
    ------
    x : set of char.
    """
    return node.replace('|', ',').split(',')


def gen_node(node_1, node_2):
    """
    Generate one node name in next regular vine tree by two neighbor
    nodes named 'node_1' and 'node_2' in current tree.

    Parameter
    ---------

    node_1, node_2 : string. The format of 'node_1' and 'node_2' 
                     follows Bedford and Cook 2001, 2002 composed 
                     by conditioned set and conditioning set
                     seperated by '|'.

    Return
    ------
    x : string. The generated node name for the next regular vine
        tree.
    """
    label_set_1 = set(node_labels(node_1))
    label_set_2 = set(node_labels(node_2))

    conditioning_label_set = label_set_1 & label_set_2
    conditioned_label_set  = (label_set_1 | label_set_2) - \
                                conditioning_label_set

    conditioning_labels = list(conditioning_label_set)
    conditioned_labels  = list(conditioned_label_set)
    
    conditioning_labels.sort()
    conditioned_labels.sort()

    if conditioning_labels:
        return ','.join(conditioned_labels) + '|' + ','.join(conditioning_labels)
    else:
        return ','.join(conditioned_labels)



def partial_correlation(conditioned_vars, conditioning_vars, corr_mat):
    """
    Figure the partial correlation of the two variables in the list 'lstConditioned'
    given variables in list 'lstConditioning'.

    Parameter
    ---------

    lstConditioned : list of two int.

    lstConditioning : list of int.
    
    Return
    ------
    x : float. Partial correlation.
    """
    yInd = conditioned_vars + conditioning_vars
    xInd = [[x] for x in yInd]
    inv_mat = np.linalg.inv(corr_mat[xInd, yInd])
    sigma12 = inv_mat[0, 1]
    sigma11 = inv_mat[0, 0]
    sigma22 = inv_mat[1, 1]
    return - sigma12 / np.sqrt(sigma11 * sigma22)




def gen_next_vine_tree(current_tree, corr_mat, structure = 'R', family = 1):
    """
    Function for generating and modeling the next tree given current
    tree.

    Parameter
    ---------

    nxCurTree : vine tree with class networkx.Graph() like.

    cormat : 2-D array. Correlation matrix specified.

    Return
    ------

    x : a tuple of two networkx.Graph() elements. The next graph and
        the next tree.
    """
    # create next graph
    next_graph = nx.Graph()

    def gen_edge(neighbor_node_pair, node):
        prev_node_0, prev_node_1 = neighbor_node_pair

        ## n0 and n1 are two new nodes of next graph
        current_node_0 = gen_node(prev_node_0, node)
        current_node_1 = gen_node(prev_node_1, node)
        next_graph.add_edge(current_node_0, current_node_1)

        label_set_0 = set(current_node_0.replace('|', '')) - set(',')
        label_set_1 = set(current_node_1.replace('|', '')) - set(',')
    
        conditioning_label_set = set.intersection(label_set_0, label_set_1)
        conditioned_label_set  = set.union(label_set_0, label_set_1) - conditioning_label_set

        conditioning_vars = map(lambda x : int(x) - 1, list(conditioning_label_set))
        conditioned_vars  = map(lambda x : int(x) - 1, list(conditioned_label_set))

        partial_corr_rho = partial_correlation(conditioned_vars,
                                               conditioning_vars,
                                               corr_mat)

        next_graph[current_node_0][current_node_1]['rho'     ] = partial_corr_rho
        next_graph[current_node_0][current_node_1]['weight'  ] = 1- np.abs(partial_corr_rho)
        next_graph[current_node_0][current_node_1]['one_fold'] = [prev_node_0, prev_node_1, node]
        
        return


    for one_node in current_tree.nodes():
        neighbour_nodes = current_tree.neighbors(one_node)
        
        if len(neighbour_nodes) >= 2:
            ## first generate all of the 2-combination of neighbor
            ## nodes of the current node
            neighbour_nodes_pairs = combinations(neighbour_nodes, 2)
            ## then for each element of the 2-combination (n0,n1),
            ## generate the new edge (n0|node,n1|node) for the next
            ## graph
            for node_pair in neighbour_nodes_pairs:
                gen_edge(node_pair, one_node)

    ## after generate all the possible new edges for the next graph,
    ## we use prim algorithm to generate the next tree with maximum
    ## summation of weight
    if structure == 'R':
        next_tree = nx.minimum_spanning_tree(next_graph)
    elif structure == 'C':
        next_tree = next_graph.copy()
        node_weight_sum = {}
        for node in next_tree.nodes():
            neighbor_nodes = next_tree.neighbors(node)
            node_weight_sum[node] = sum([next_tree[node][one_node]['weight'] for one_node in neighbor_nodes])
         
        star_node = min(node_weight_sum, key = node_weight_sum.get)
        star_node_neighbors = next_tree.neighbors(star_node)
        paired_nodes = combinations(star_node_neighbors, 2)
 
        for e in paired_nodes:
            next_tree.remove_edge(*e)
        
    for edge in next_tree.edges():
        n0, n1 = edge
        next_tree[n0][n1]['family'] = family
        next_tree[n0][n1]['par'   ] = np.zeros(2, dtype = np.float)
        
    return next_tree, next_graph




def corr_mat_to_vine(corr_mat, structure = 'R', family_0 = 1, family_1 = 1):
    """
    Generate Rvine structure from correlation matrix.

    Parameter
    ---------
    npCorMat : 2D np.array. A correlation matrix.
    
    structure : char. Specify the vine structure that should be generated.
                Default is 'R' for Regular vine structure. Alternative is 'C' 
                for C-vine structure.
                
    Return
    ------
    x : list of networkx.Graph. Vine structure.
    """
    num_vars = corr_mat.shape[0]
    
    nodes = [str(i) for i in range(1, num_vars + 1)]
    node_pairs = combinations(nodes, 2)

    vine_trees  = []
    vine_graphs = []

    ## initialization of the first tree
    current_graph = nx.Graph()

    for edge in node_pairs:
        current_graph.add_edge( *edge )
        
    for edge in current_graph.edges():
        n0, n1 = edge
        rho    = corr_mat[int(n0) - 1, int(n1) - 1]
        current_graph[n0][n1]['rho'   ] = rho
        current_graph[n0][n1]['weight'] = 1 - np.abs( rho )

    vine_graphs.append(current_graph)
    
    if structure == 'R':
        current_tree = nx.minimum_spanning_tree(current_graph)
    elif structure == 'C':
        current_tree = current_graph.copy()
        node_weight_sum = {}
        for node in current_tree.nodes():
            neighbor_nodes = current_tree.neighbors(node)
            node_weight_sum[node] = sum([current_tree[node][one_node]['weight'] for one_node in neighbor_nodes])
         
        star_node = min(node_weight_sum, key = node_weight_sum.get)
        star_node_neighbors = current_tree.neighbors(star_node)
        paired_nodes = combinations(star_node_neighbors, 2)
 
        for e in paired_nodes:
            current_tree.remove_edge(*e)

    for edge in current_tree.edges():
        n0, n1 = edge
        # 'par' is length 2 array and family set to 1 for
        # extensibility in the future.
        current_tree[n0][n1]['par'   ] = np.zeros(2, dtype = np.float)
        current_tree[n0][n1]['family'] = family_0

    vine_trees.append(current_tree)
    
    while( len(current_tree.nodes()) >= 3 ):
        next_tree, next_graph = gen_next_vine_tree(current_tree, 
                                                   corr_mat,
                                                   structure = structure,
                                                   family = family_1
                                                   )
        vine_trees.append(next_tree)
        vine_graphs.append(next_graph)
        current_tree = next_tree

    return vine_trees



def rvine_sim(vine_trees, size):
    """
    Sample from a regular vine object 'RVine'.

    Parameter
    ---------
    vine_trees : list of networkx.Graph(). Each element is a vine tree.

    size : int. Sample size.

    Return
    ------
    x : pandas DataFrame like.
    """
    tree_num = len(vine_trees) - 1
    
    # firstly sample for the edge of the last tree
    current_tree = vine_trees[tree_num]
    n0, n1       = current_tree.edges()[0]
    edge_info    = current_tree[n0][n1]
    
    u_n0 = np.random.rand( size )
    u_n1 = np.random.rand( size )
    
    edge_par    = edge_info['par'   ]
    edge_family = edge_info['family']
    
    u_n1 = bvcop.bv_cop_inv_hfunc(u_n1,
                                  u_n0,
                                  edge_par,
                                  edge_family
                                  )
    
    edge_sample = {n0:u_n0, n1:u_n1}
    current_tree[n0][n1]['sample'] = edge_sample
    
    if tree_num == 0:       # vine has only one tree
        return edge_sample
    
    def sample_edge(n0, n1, next_tree_n0, next_tree_n1):
        """
        Need doc here
        """
        ## determine the current tree number from node name
        tree_num = len(n0.replace('|', ',').split(',')) - 1
        
        current_tree = vine_trees[tree_num]
        next_tree    = vine_trees[tree_num + 1]
        edge_info    = current_tree[n0][n1]

        ## if marginal samples both exists on this edge (n0, n1), just
        ## return
        if edge_info.has_key('sample') and \
                len(edge_info['sample']) == 2:
            return

        ## if u_n0 and u_n1 both don't exist, or only u_n0 exists
        if not edge_info.has_key('sample') or not \
                edge_info['sample'].has_key(n1):
            ## if current tree is the first tree, just sample u_n1
            ## from uniform distribution
            if tree_num == 0:
                u_n1 = np.random.rand( size )
            ## if not the first tree, consider whether u_n1 could be
            ## figured out via H-function from marginal samples on the
            ## edge corresponding to its one-fold triple in the
            ## previous tree. if the two marginal samples doesn't both
            ## exist, just sample u_n1 from uniform distribution
            else:
                prev_n0, prev_n1, prev_n2 = edge_info['one_fold']
                prev_tree = vine_trees[tree_num - 1]
                if not gen_node(prev_n0, prev_n2) == n1:
                    prev_n0 = prev_n1
                prev_edge_info = prev_tree[prev_n0][prev_n2]
                if prev_edge_info.has_key('sample') and \
                        len(prev_edge_info['sample']) == 2:
                    u_prev_n0 = prev_edge_info['sample'][prev_n0]
                    u_prev_n2 = prev_edge_info['sample'][prev_n2]
                    u_n1 = bvcop.bv_cop_hfunc(u_prev_n0,u_prev_n2,
                                              prev_edge_info['par'],                        
                                              prev_edge_info['family']
                                              )
                else:
                    u_n1 = np.random.rand( size )

        else:
            u_n1 = edge_info['sample'][n1]

        ## figure out u_n0 via the inverse H-function via marginal
        ## sample on edge (old_n0,old_n1)
        next_tree_info = next_tree[next_tree_n0][next_tree_n1]
        u_n0 = bvcop.bv_cop_inv_hfunc(next_tree_info['sample'][gen_node(n0, n1)],
                                  u_n1,
                                  edge_info['par'],
                                  edge_info['family']
                                  )

        ## put the sampled dict of edge_sample on edge (n0,n1)
        edge_sample = {n0:u_n0, n1:u_n1}
        current_tree[n0][n1]['sample'] = edge_sample

        ## if the current tree is the first one, copy the marginal
        ## sample to the neighbor edge as soon as it is generated.
        if tree_num == 0:
            for one_node in current_tree.neighbors(n0):
                if not current_tree[n0][one_node].has_key('sample'):
                    edge_sample = {n0:u_n0}
                    current_tree[n0][one_node]['sample'] = edge_sample
                else:
                    if not current_tree[n0][one_node]['sample'].has_key(n0):
                        current_tree[n0][one_node]['sample'][n0] = u_n0
            for one_node in current_tree.neighbors(n1):
                if not current_tree[n1][one_node].has_key('sample'):
                    edge_sample = {n1:u_n1}
                    current_tree[n1][one_node]['sample'] = edge_sample
                else:
                    if not current_tree[n1][one_node]['sample'].has_key(n1):
                        current_tree[n1][one_node]['sample'][n1] = u_n1
            return

        ## recover the three node of one-fold triple of current edge
        prev_n0, prev_n1, prev_n2 = edge_info['one_fold']

        ## call 'sample_edge' itself recursively
        sample_edge(prev_n0, prev_n2, n0, n1)
        sample_edge(prev_n1, prev_n2, n0, n1)
        return 
    
    prev_n0, prev_n1, prev_n2 = edge_info['one_fold']

    # recursive sampling entrance
    sample_edge(prev_n0, prev_n2, n0, n1)
    sample_edge(prev_n1, prev_n2, n0, n1)
    
    sample_result = {}
    tree_1 = vine_trees[0]
    
    for edge in tree_1.edges():
        n0, n1 = edge
        edge_info = tree_1[n0][n1]
        if not sample_result.has_key(n0):
            sample_result[n0] = edge_info['sample'][n0]
        if not sample_result.has_key(n1):
            sample_result[n1] = edge_info['sample'][n1]

    for tree in vine_trees:
        for edge in tree.edges():
            n0, n1 = edge
            tree[n0][n1].pop('sample')
            
    return sample_result





def iscorrmat(corr_mat):
    """
    Check the input matrix meets:

        1. square matrix
        2. diagonal are one's
        2. symmetric matrix 
        3. eigen values are positive

    Parameter
    ---------
    corr_matrix : 2-D numpy array.
    """
    nrow, ncol = corr_mat.shape[0 : 2]
    if nrow != ncol:
        return False
    if np.any(np.diag(corr_mat) != 1):
        return False
    if np.any(corr_mat != corr_mat.transpose()):
        return False
    if np.any(np.linalg.eigvals(corr_mat) <= 0):
        return False
    return True
    
    

def marginal_vine(vine_trees, edge):
    """
    Generate marginal vine structure of vine_trees from one edge of one tree.
    
    Parameter
    ---------
    vine_trees : list of networkx.Graph().
    
    edge : tuple of two nodes.
    
    Return
    ------
    x : list of networkx.Graph().
    """
    n0, n1 = edge
    num_tree = len(node_labels(n0))
    print "num of tree = %d " % num_tree
    # argument check.
    if num_tree != len(node_labels(n1)):
        raise ValueError("nodes are from different trees.")
    if edge not in vine_trees[num_tree-1].edges():
        raise ValueError("specified edge isn't an edge in the vine structure.")
    
    marginal_label_set = set(node_labels(gen_node(n0, n1)))
    marginal_vine_trees = copy.deepcopy(vine_trees[0 : num_tree])
    
    for i in range(num_tree):
        nodes_for_delete = []
        for one_node in marginal_vine_trees[i].nodes():
            node_label_set = set(node_labels(one_node))
            if not node_label_set.issubset(marginal_label_set):
                nodes_for_delete.append(one_node)
        marginal_vine_trees[i].remove_nodes_from(nodes_for_delete)
    
    return marginal_vine_trees


def vine_plot(vine_trees, ntrees = 0, filename = ""):
    """
    Plot the regular vine structure generated through routine
    'cor2vine'.

    Parameter
    ---------

    ntrees : int, optional. The first ntrees of all the vine trees
             will be plotted. Default is `0', meaning plotting all
             the vine trees.
             
    filename : string, optional. Default is an empty string
               indicating direct output to screen. The plot will
               output to the specified directory if a file name
               with extension is given.
    """
    num_vars = len(vine_trees) + 1
    if ntrees == 0:
        ntrees = num_vars - 1
    elif ntrees > num_vars - 1:
        ntrees = num_vars - 1

    if ntrees == 1:
        plt.title("Tree_1")
        nx.draw(vine_trees[0], with_labels=True)
        if filename:
            plt.savefig(filename)                
        else:
            plt.show()
    else:
        mfrow = (ntrees+1) /2
        mfcol = 2

        for i in range(ntrees):
            plt.subplot(mfrow, mfcol, i+1)
            plt.title("Tree_"+ str(i+1) ) 
            nx.draw(vine_trees[i], with_labels=True)
        if filename:
            plt.savefig(filename)                
        else:
            plt.show()

    plt.clf()


# def approx_edge_par(edge, vine_trees, corr_mat, discrete_vars, size = 100000):
#     """
#     Approximate the parameter of specified edge.
#     
#     Parameter
#     ---------
#     edge : tuple of two strings. Two nodes.
#     
#     marginal_vine_tree : list of networkx.Graph(). Marginal vine structure.
#     
#     corr_mat : 2D numpy array.
#     
#     discrete_vars : list of univariate CountVar objects. 
#     
#     size : int. Sample size.
#     """
#     n0, n1 = edge
#     tree_num = len(node_labels(n0))
#     conditioning_label_set = set(node_labels(n0)) & set(node_labels(n1))
#     # "(&1 | &2) - &3" , not "&1 | &2 - &3" below.
#     conditioned_label_set = ( set(node_labels(n0)) | set(node_labels(n1)) ) \
#                              - conditioning_label_set
#     conditioned_labels = tuple(conditioned_label_set)
#     label_0, label_1 = conditioned_labels
#     discrete_var_0 = discrete_vars[int(label_0) - 1]
#     discrete_var_1 = discrete_vars[int(label_1) - 1]
#     edge_info = vine_trees[tree_num-1].get_edge_data(n0, n1)
#     if edge_info['family'] == 1:
#         def TarFunc(par):
#             """
#             """
#             u_0 = np.random.rand(size)
#             u_1 = bvcop.bv_cop_inv_hfunc(np.random.rand(size), u_0, np.array([np.arctan(par) * 2 / np.pi, 0]), edge_info['family'])
#             u_var_0   = discrete_var_0.sim(u_0)
#             u_var_1   = discrete_var_1.sim(u_1)
#             realized_corr_sigma = np.corrcoef(u_var_0, u_var_1)[0, 1]
#             return np.abs(realized_corr_sigma - edge_info['rho'])
#         par_hat = np.array([np.arctan(fmin(TarFunc, x0=edge_info['rho'])) * 2.0 / np.pi, 0], dtype=np.float)
#     elif edge_info['family'] == 4:
#         def TarFunc(par):
#             """
#             """
#             u_0 = np.random.rand(size)
#             u_1 = bvcop.bv_cop_inv_hfunc(np.random.rand(size), u_0, np.array([np.exp(par) + 1.0, 0]), edge_info['family'])
#             u_var_0   = discrete_var_0.sim(u_0)
#             u_var_1   = discrete_var_1.sim(u_1)
#             realized_corr_sigma = np.corrcoef(u_var_0, u_var_1)[0, 1]
#             return np.abs(realized_corr_sigma - edge_info['rho'])
#         par_hat = np.array([np.exp(fmin(TarFunc, x0=edge_info['rho'])) + 1.0, 0], dtype=np.float)            
#     return par_hat
        
    
    
    

# def approx_vine_par(vine_trees, corr_mat, discrete_vars, size):
#     """
#     approx parameters on each edge of vine trees.
#     
#     Parameter
#     ---------
#     vine_trees : list of networkx.Graph(). 
#     
#     corr_mat : 2D numpy.array.
#     
#     discrete_vars :
#     
#     size : int. Sample size 
#     
#     Return
#     ------
#     x : list of networkx.Graph(). vine structure with approxed parameters.
#     """
#     for one_tree in vine_trees:
#         for edge in one_tree.edges():
#             print "approximating edge (%s, %s) .." % edge
#             # marginal_vine_trees = marginal_vine(vine_trees, edge)
#             edge_par = approx_edge_par(edge, 
#                                        vine_trees,
#                                        corr_mat,
#                                        discrete_vars,
#                                        size
#                                        )
#             n0, n1 = edge
#             one_tree[n0][n1]['par'] = edge_par
#     return vine_trees



##########################################
# code below approximate edge parameter by
# a method of marginal vine copulas.
##########################################


def approx_edge_par(edge, marginal_vine_trees, corr_mat, discrete_vars, size = 100000, opt_count = 5):
    """
    Approximate the parameter of specified edge.
     
    Parameter
    ---------
    edge : tuple of two strings. Two nodes.
     
    marginal_vine_tree : list of networkx.Graph(). Marginal vine structure.
     
    corr_mat : 2D numpy array.
     
    discrete_vars : list of univariate CountVar objects. 
     
    size : int. Sample size.
    
    opt_count : int. The optimization will stop till opt_count times or optimization successfully returned.
                Default is 5.
    """
    n0, n1 = edge
    tree_num = len(node_labels(n0))
    conditioning_label_set = set(node_labels(n0)) & set(node_labels(n1))
    # "(&1 | &2) - &3" , not "&1 | &2 - &3" below.
    conditioned_label_set = ( set(node_labels(n0)) | set(node_labels(n1)) ) \
                             - conditioning_label_set
    conditioned_labels = tuple(conditioned_label_set)
    print conditioned_labels
    label_0, label_1 = conditioned_labels
    discrete_var_0 = discrete_vars[int(label_0) - 1]
    discrete_var_1 = discrete_vars[int(label_1) - 1]
    corr_sigma = corr_mat[int(label_0)-1, int(label_1)-1]
    edge_info = marginal_vine_trees[tree_num-1].get_edge_data(n0, n1)
    if edge_info['family'] == 1:
        def TarFunc(par):
            """
            """
            marginal_vine_trees[tree_num-1][n0][n1]['par'] = np.array([np.arctan(par) * 2 / np.pi, 0], dtype=np.float)
            sim_dat = rvine_sim(marginal_vine_trees, size)
            u_label_0 = sim_dat[label_0]
            u_label_1 = sim_dat[label_1]
            u_var_0   = discrete_var_0.sim(u_label_0)
            u_var_1   = discrete_var_1.sim(u_label_1)
            realized_corr_sigma = np.corrcoef(u_var_0, u_var_1)[0, 1]
            return abs(corr_sigma - realized_corr_sigma)
        
        opt_flag = False
        n_count = 0
        while ( not opt_flag and n_count < opt_count ):
            optim_res = fmin(TarFunc, x0=edge_info['rho'], full_output = True)
            if optim_res[4] == 0:
                opt_flag = True
            n_count += 1
            
        par_hat = np.array([np.arctan(optim_res[0]) * 2.0 / np.pi, 0], dtype=np.float)
        
    elif edge_info['family'] == 4:
        def TarFunc(par):
            """
            """
            marginal_vine_trees[tree_num-1][n0][n1]['par'] = np.array([np.exp(par) + 1.0, 0], dtype=np.float)
            sim_dat = rvine_sim(marginal_vine_trees, size)
            u_label_0 = sim_dat[label_0]
            u_label_1 = sim_dat[label_1]
            u_var_0   = discrete_var_0.sim(u_label_0)
            u_var_1   = discrete_var_1.sim(u_label_1)
            realized_corr_sigma = np.corrcoef(u_var_0, u_var_1)[0, 1]
            return abs(corr_sigma - realized_corr_sigma)
        
        opt_flag = False
        n_count = 0
        while ( not opt_flag and n_count < opt_count ):
            optim_res = fmin(TarFunc, x0=edge_info['rho'], full_output = True)
            if optim_res[4] == 0:
                opt_flag = True
            n_count += 1
        
        par_hat = np.array([np.exp(optim_res[0]) + 1.0, 0], dtype=np.float) 
                   
    return par_hat
         
     
     
     
 
def approx_vine_par(vine_trees, corr_mat, discrete_vars, size):
    """
    approx parameters on each edge of vine trees.
     
    Parameter
    ---------
    vine_trees : list of networkx.Graph(). 
     
    corr_mat : 2D numpy.array.
     
    discrete_vars :
     
    size : int. Sample size 
     
    Return
    ------
    x : list of networkx.Graph(). vine structure with approxed parameters.
    """
    for one_tree in vine_trees:
        for edge in one_tree.edges():
            print "approximating edge (%s, %s) .." % edge
            marginal_vine_trees = marginal_vine(vine_trees, edge)
            edge_par = approx_edge_par(edge, 
                                       marginal_vine_trees,
                                       corr_mat,
                                       discrete_vars,
                                       size
                                       )
            n0, n1 = edge
            one_tree[n0][n1]['par'] = edge_par
    return vine_trees
             
            

def multi_count_sim(vine_trees, discrete_vars, size):
    """
    Sample multi count variables using regular vine copula structure.
    
    Parameter
    ---------
    
    vine_trees : list of networkx.Graph(). Vine trees list.
    
    discrete_vars : list of CountRV objs.
    
    size : int. Sample size.
    
    Return
    ------
    x : dict of 1D numpy.array.
    """            
    multi_seeds = rvine_sim(vine_trees, size)
    sim_dat = {}
    for key, seeds in multi_seeds.iteritems():
        rv = discrete_vars[int(key) - 1]
        rv_samples = rv.sim(seeds)
        sim_dat[key] = rv_samples
    return sim_dat


def realized_corr_mat_replications(vine_trees, discrete_vars, corr_mat, R, size):
    """
    Realized correlation matrix replications of multi count variables with a
    prespecified correlation matrix sampled using regular vine copulas method.
    
    Parameter
    ---------
    vine_trees : list of networkx.Graph().
    
    discrete_vars : list of CountRV objs.
    
    corr_mat : 2D numpy.array.
    
    R : int. Number of replications.
    
    size : int. Sample size.
    
    Return
    ------
    x : list of 2D numpy.array.
    """
    def one_replication():
        """
        """
        sim_dat = multi_count_sim(vine_trees, discrete_vars, size)
        return ps.DataFrame(sim_dat).corr().values
    
    return [one_replication() for r in range(R)]


def realized_naive_corr_mat_replications(discrete_vars, corr_mat, R, size):
    """
    Realized correlation matrix replications of multi count variables with a
    prespecified correlation matrix sampled by naive method.
    
    Parameter
    ---------
    discrete_vars : list of CountRV objs.
    
    corr_mat : 2D numpy.array.
    
    R : int. Number of replications.
    
    size : int. Sample size.
    
    Return
    ------
    x : list of 2D numpy.array.    
    """
    def one_replication():
        """
        """
        sim_dat = naive_sim(corr_mat, discrete_vars, size)
        return ps.DataFrame(sim_dat).corr().values
    
    return [one_replication() for r in range(R)]


def max_relative_bias(vine_trees, discrete_vars, corr_mat, R, size):
    """
    Performance test routine of sampling multi-discrete variables using regular
    vine copula method. See "A method for approximately sampling high-
    dimensional count variables with prespecified Pearson Correlation" for
    detailed definition.
    
    Parameter
    ---------
    vine_trees : list of networkx.Graph().
    
    corr_mat : 2D numpy array
    
    R : int. Replications.
    
    size : int. Sample size.
    
    Return
    ------
    x : float. Maximum of relative bias.
    """
    realized_corr_mats = realized_corr_mat_replications(vine_trees,
                                                        discrete_vars,
                                                        corr_mat,
                                                        R,
                                                        size)
    corr_mat_hat = sum(realized_corr_mats) / R
    return np.max(np.abs(corr_mat_hat / corr_mat - 1.0))
    

def max_relative_bias_naive_method(discrete_vars, corr_mat, R, size):
    """
    Performance test routine of sampling multi-discrete variables by naive
    method. See "A method for approximately sampling high-dimensional count
    variables with prespecified Pearson Correlation" for detailed definition.
    
    Parameter
    ---------
    vine_trees : list of networkx.Graph().
    
    corr_mat : 2D numpy array
    
    R : int. Replications.
    
    size : int. Sample size.
    
    Return
    ------
    x : float. Maximum of relative bias.
    """
    realized_naive_corr_mats = realized_naive_corr_mat_replications(discrete_vars,
                                                                    corr_mat,
                                                                    R,
                                                                    size)
    corr_mat_hat = sum(realized_naive_corr_mats) / R
    return np.max(np.abs(corr_mat_hat / corr_mat - 1.0))
    
    
def average_acceptance_number(vine_trees, discrete_vars, corr_mat, R, size, alpha):
    """
    Performance test routine of sampling multi-discrete variables. See "A method
    for approximately sampling high-dimensional count variables with
    prespecified Pearson Correlation" for detailed definition.
    
    Parameter
    ---------
    vine_trees : list of networkx.Graph().
    
    corr_mat : 2D numpy array
    
    R : int. Replications.
    
    size : int. Sample size.
    
    Return
    ------
    x : float. Average number of acceptance.
    """
    if size <= 10:
        raise ValueError("Sample size too small!")
    T = len(discrete_vars)
    realized_corr_mats = realized_corr_mat_replications(vine_trees,
                                                        discrete_vars,
                                                        corr_mat,
                                                        R,
                                                        size)
    realized_z_mats = [np.arctanh(np.tril(corr_mat_hat, -1)) for corr_mat_hat in realized_corr_mats]
    z_mat = np.arctanh(np.tril(corr_mat, -1))
    z_stats = [np.sqrt(size-3) * np.abs(z_mat_hat - z_mat) for z_mat_hat in realized_z_mats]
    critical_value = norm.ppf(1 - alpha / T / (T - 1))
    acceptance_results = [np.all(one_z_stat <= critical_value) for one_z_stat in z_stats]
    return np.array(acceptance_results).mean()
    
    
def average_acceptance_number_naive_method(discrete_vars, corr_mat, R, size, alpha):
    """
    """
    if size <= 10:
        raise ValueError("Sample size too small!")
    T = len(discrete_vars)
    realized_corr_mats = realized_naive_corr_mat_replications(discrete_vars,
                                                              corr_mat,
                                                              R,
                                                              size)
    realized_z_mats = [np.arctanh(np.tril(corr_mat_hat, -1)) for corr_mat_hat in realized_corr_mats]
    z_mat = np.arctanh(np.tril(corr_mat, -1))
    z_stats = [np.sqrt(size-3) * np.abs(z_mat_hat - z_mat) for z_mat_hat in realized_z_mats]
    critical_value = norm.ppf(1 - alpha / T / (T - 1))
    acceptance_results = [np.all(one_z_stat <= critical_value) for one_z_stat in z_stats]
    return np.array(acceptance_results).mean()


def naive_sim(corr_mat, discrete_vars, size):
    """
    Naive method for sampling from multi counts variables with prespecified
    correlation matrix.
    
    Parameter
    ---------
    corr_mat : 2D numpy.array. Correlation matrix.
    
    discrete_vars : list of CountRV.
    
    size : int. Sample size.
    
    Return
    ------
    x : dict of 1D numpy.array.
    """
    T = len(discrete_vars)
    if T != corr_mat.shape[0]:
        raise ValueError("correlation matrix dim not equal to number of univariate discrete variables.")
    
    A = np.linalg.cholesky(corr_mat)
    Z = norm.rvs(size = (T, size))
    naive_seeds = norm.cdf(np.dot(A, Z).transpose())
    sim_dat = {}
    
    for i in range(T):
        sim_dat[str(i + 1)] = discrete_vars[i].sim(naive_seeds[:, i])
        
    return sim_dat
    
    
    
# class MultiCounts:
#     def __init__(self, npCorMat, rvs):
#         """
#         Parameter
#         ---------
# 
#         npCorMat : 2-D square matrix. The correlation matrix of
#                       discrete variables.
# 
#         rvs         : list of `Counts` class instances.
#         """
#         if type(npCorMat) != np.ndarray:
#             raise TypeError("corr_matrix should be numpy.ndarray type.")
#         if not iscorrmat(npCorMat):
#             raise ValueError("The input matrix isn't a correlation matrix.")
# 
#         self.npCorMat = npCorMat
#         self.numVars = npCorMat.shape[0]
# 
#         if len(rvs) != self.numVars:
#             raise ValueError("'rvs' length doesn't conform with correlation matrix.")
# 
#         self.rvs = rvs
#         self.VarLabels = range(1, self.numVars + 1)
# 
#     def _GenVine(self, structure = 'r'):
#         """
#         Generate regular vine copula via discrete variable correlation
#         matrix. Regular vine structure are determined by Pearson
#         correlation parameter or partial correlation parameter;
#         bivariate copula on each edges are specified as normal.
#         
#         Parameter
#         ---------
# 
#         structure : flag specifying the structure of vine. 'r',
#                     'c' and 'd' and there capital letters are
#                     acceptable. 'r' stands for generalized regular
#                     vine; 'c' stands for C-vine, with star like trees;
#                     'd' stands for D-vine, with linear structure
#                     trees.
#         """
#         if structure.upper() not in ['C', 'R']:
#             raise ValueError('Unknown structure!')
#         self.Rvine = GenVine(self.npCorMat)
#         
# 
#     def sim(self, size, seed = 'gaussian'):
#         """
#         Simulate multivariate count samples from either gaussian dependence
#         structure or from regular vine structure.
#         
#         Parameter
#         ---------
#         
#         size : int. Sample size.
#         
#         seed : str. 'gaussian' means the seeds for sampling is generated from
#                multivariate gaussian. 'vine' means the seeds is generated from
#                vine copula.
#         """
#         if seed == 'gaussian':
#             A = np.linalg.cholesky(self.GaussianMat)
#             Z = norm.rvs(size = (self.numVars, size))
#             npMultiSeeds = norm.cdf(np.dot(A, Z).transpose())
#             npMultiCountSamples = np.zeros((size, self.numVars), dtype = np.int)
# 
#             for i in range(self.numVars):
#                 npMultiCountSamples[:, i] = self.rvs[i].sim(npMultiSeeds[:, i])
# 
#             return npMultiCountSamples
# 
#         elif seed == 'vine':
#             npMultiSeeds = np.array(RvineSim(self.Rvine, size).values()).transpose()
#             npMultiCountSamples = np.ndarray((size, self.numVars), dtype = np.int)
#         
#             for i in range(self.numVars):
#                 npMultiCountSamples[:, i] = self.rvs[i].sim(npMultiSeeds[:, i])
#             
#             return npMultiCountSamples
# 
# 
#     def _distance(self, size, seed = 'gaussian'):
#         """
#         Figure out the distance between specified correlation matrix and
#         realized correlation matrix from simulation.
#         
#         Parameter
#         ---------
#         
#         size : int. sample size.
#         
#         seed : str. 'gaussian' or 'vine' are acceptable.
#         
#         Return
#         ------
#         
#         x : float. max |C - C_0|.
#         """
#         npRealizedCorMat = np.corrcoef(self.sim(size, seed), rowvar = 0)
#         return np.max(np.abs(npRealizedCorMat - self.npCorMat))
# 
# 
#     def _approx_par_edge(self, edge, size, disp = False):
#         """
#         Find the initial guess for the edges of the first vine tree using the
#         simulation method.
#         
#         Parameter
#         ---------
#         
#         edge : list of two char.
#         
#         size : int. The sample size.
#         """
#         n0, n1 = edge
#         i, j = int(n0) - 1, int(n1) - 1
#         
#         def obj_fun(par):
#             bv_seeds = bvcop.bv_cop_sim(np.array([par, 0]), 1, size)
#             bv_sim_0 = self.rvs[i].sim(bv_seeds[:, 0])
#             bv_sim_1 = self.rvs[j].sim(bv_seeds[:, 1])
#             return np.abs(np.corrcoef(bv_sim_0, bv_sim_1)[0, 1]\
#                               - self.npCorMat[i,j])
#         
#         x0 = self.npCorMat[i, j]
#         cons = [lambda x : 0.999 - np.abs(x)]
#         par = fmin_cobyla(obj_fun, x0, cons, disp = disp, rhobeg = 0.05, rhoend = 1e-5)
#         return np.array([par, 0])
#             
# 
#     def _approx_par_tree_0(self, size, disp = False):
#         """
#         Find the initial parameter guesses of edges of the first vine tree.
#         
#         Parameter
#         ---------
#         size : int. sample size.
#         
#         disp : bool. Flag for displaying the optimization result. 
#         """
#         for edge in self.Rvine[0].edges():
#             n0, n1 = edge
#             self.Rvine[0][n0][n1]['par'] = self._approx_par_edge(edge, size, disp = disp)
#             
# 
#     def approx_par(self, size, seed = 'gaussian', structure = 'r', disp = False):
#         """
#         
#         """
#         if seed == 'gaussian':
#             self.GaussianMat = self.npCorMat
#             ## object function , par length (d - 1) * d / 2
#             def object_fun(par):
#                 """
#                 """
#                 k = 0
#                 for i in range(self.var_num - 1):
#                     for j in range(i + 1, self.var_num):
#                         self.GaussianMat[i, j] = tanh(par[k])
#                         self.GaussianMat[j, i] = tanh(par[k])
#                         k += 1
# 
#                 print self.GaussianMat
# 
#                 return self._distance(size, seed)
# 
#             ## optimization
#             par_num = (self.var_num - 1) * self.var_num / 2
# 
#             x0 = np.zeros(par_num, dtype = np.float)
# 
#             k = 0
#             for i in range(self.var_num - 1):
#                 for j in range(i + 1, self.var_num):
#                     x0[k] = arctanh(self.cormat[i, j])
#                     k += 1
# 
#             print x0
# 
#             par = fmin_powell(object_fun, x0, disp = disp)
# 
#             if len(par.shape) == 0:
#                 par = np.array([par.item()])
# 
#             k = 0
#             for i in range(self.var_num - 1):
#                 for j in range(i + 1, self.var_num):
#                     self.GaussianMat[i, j] = tanh(par[k])
#                     self.GaussianMat[j, i] = tanh(par[k])
#                     k += 1
# 
#             return
#                     
#             
#         elif seed == 'vine':
# 
#             self._mc_to_vine(structure = structure)
# 
#             ## find parameters on edges of the first tree 
#             self._approx_par_tree_0(size)
# 
#             ## find parameters on edges of the rest trees
#             par_num = (self.var_num - 1) * (self.var_num - 2) / 2
# 
#             def object_fun(par):
#                 """
#                 """
#                 i = 0
#     
#                 for tree in self.Rvine[1:]:
#                     for edge in tree.edges():
#                         n0, n1 = edge
#                         # edge_par = np.array([par[i], 0], np.float)
#                         edge_par = np.array([tanh(par[i]), 0], np.float)                    
#                         tree[n0][n1]['par'] = edge_par
#                         i += 1
# 
#                 return self._distance(size, seed)
# 
#             x0 = np.zeros(par_num, dtype = np.float)
# 
#             ## initial value is set to `rho`
# 
#             i = 0
# 
#             for tree in self.Rvine[1:]:
#                 for edge in tree.edges():
#                     n0, n1 = edge
#                     x0[i] = arctanh(tree[n0][n1]['rho'])
#                     i += 1
#                 
#             # def gen_cons(i):
#             #     return lambda x : 0.99 - np.abs(x[i])
# 
#             # cons = [gen_cons(i) for i in range(par_num)]
# 
#             # par = fmin_cobyla(object_fun, x0, cons, disp = disp, rhobeg = 0.05, rhoend = 1e-5)
#             par = fmin_powell(object_fun, x0,  disp = disp)
# 
#             ## below sentence is because different return type of
#             ## `fmin_powell` for 1-D and multi-D optimization.
# 
#             if len(par.shape) == 0:
#                 par = np.array([par.item()])
# 
#             i = 0
# 
#             for tree in self.Rvine[1:]:
#                 for edge in tree.edges():
#                     n0, n1 = edge
#                     # edge_par = np.array([par[i], 0],dtype = np.float)
#                     edge_par = np.array([tanh(par[i]), 0],dtype = np.float)                
#                     tree[n0][n1]['par'] = edge_par
#                     i += 1
# 
#             return 
# 
#         
# 
# 
# 
#     def res(self, ndigits = 2):
#         """
#         Return the parameters of bivariate normal copula on each edge
#         of regular vine.
# 
#         Parameter
#         ---------
# 
#         ndigits : int. Control the number of decimal digits of result
#                   that will be printed.
#         """
#         BVCOPULA_FAMILY = {
#             1:"Normal",
#             2:"Student",
#             3:"Clayton",
#             4:"Gumbel",
#             5:"Frank",
#             6:"Joe",
#             }
#         
#         if not self.Rvine:
#             raise Exception(
#                 "Routine 'cor2vine' isn't taken."
#                 )
#         
#         res_columns = pandas.MultiIndex.from_tuples([('Edge', 'Node1'),
#                                                      ('Edge', 'Node2'),
#                                                      ('Par1', ''),
#                                                      ('Par2', ''),
#                                                      ('Family', '')
#                                                      ])
#         
#         node_1_list   = []
#         node_2_list   = []
#         par_1_list    = []
#         par_2_list    = []
#         family_list   = []
#         
#         for tree in self.Rvine:
#             for edge in tree.edges():
#                 n0, n1      = edge
#                 edge_family = tree[n0][n1]['family' ]
#                 edge_par    = tree[n0][n1]['par_sqe']
#                 node_1_list.append(n0)
#                 node_2_list.append(n1)
#                 family_list.append(BVCOPULA_FAMILY[edge_family])                    
#                 par_1_list.append(round(edge_par[0],ndigits))
#                 par_2_list.append(round(edge_par[1],ndigits))
#         self.res_df = pandas.DataFrame(zip(*[node_1_list,
#                                              node_2_list,
#                                              par_1_list,
#                                              par_2_list,
#                                              family_list]),
#                                        columns = res_columns)
#         return self.res_df
#     
#     def max_bias(self, N, R, seed = 'gaussian'):
#         """
#         """
#         sim_cormat = np.zeros_like(self.cormat, dtype = np.float)
#         for i in range(R):
#             sim_cormat += np.corrcoef(self.sim(N, seed), rowvar = 0)
# 
#         return np.max(np.abs(sim_cormat / R -  self.cormat)) 
# 
# 
#     def _test(self, alpha, N, seed = 'gaussian'):
# 
#         test_num = self.var_num * (self.var_num - 1) / 2
#         alpha_c = 1 - (1 - alpha) ** (1.0 / test_num)
#         critical_value = norm.ppf(1 - alpha_c / 2.0)
#         sim_cormat = np.corrcoef(self.sim(N, seed), rowvar = 0)
#         z_stat = np.abs(arctanh(sim_cormat) - arctanh(self.cormat)) \
#             * np.sqrt(N - 3)
#         # BUG FIXED for diagonal of `z_stat` being singular
#         for i in range(self.var_num):
#             z_stat[i, i] = 0.0
#         Rej = z_stat > critical_value
# 
#         if np.any(Rej):
#             return 0
#         else:
#             return 1
# 
#     def ACC(self, alpha, N, R, seed = 'gaussian'):
#         """
#         """
#         acc_num = 0.0
# 
#         for i in range(R):
# 
#             acc_num += self._test(alpha, N, seed)
# 
#         return acc_num / R


