# http://nbviewer.ipython.org/github/herrfz/dataanalysis/blob/master/week3/svd_pca.ipynb
import numpy as np
import pandas as pd
import pandas.rpy.common as com

# a simple function to compute hierarchical cluster on both rows and columns, and plot heatmaps
def heatmap(dm):
    from scipy.cluster.hierarchy import linkage, dendrogram
    from scipy.spatial.distance import pdist, squareform
    
    D1 = squareform(pdist(dm, metric='euclidean'))
    D2 = squareform(pdist(dm.T, metric='euclidean'))
    
    f = figure(figsize=(8, 8))

    # add first dendrogram
    ax1 = f.add_axes([0.09, 0.1, 0.2, 0.6])
    Y = linkage(D1, method='complete')
    Z1 = dendrogram(Y, orientation='right')
    ax1.set_xticks([])
    ax1.set_yticks([])

    # add second dendrogram
    ax2 = f.add_axes([0.3, 0.71, 0.6, 0.2])
    Y = linkage(D2, method='complete')
    Z2 = dendrogram(Y)
    ax2.set_xticks([])
    ax2.set_yticks([])

    # add matrix plot
    axmatrix = f.add_axes([0.3, 0.1, 0.6, 0.6])
    idx1 = Z1['leaves']
    idx2 = Z2['leaves']
    D = dm[idx1, :]
    D = D[:, idx2]
    im = axmatrix.matshow(D, aspect='auto', cmap='hot')
    axmatrix.set_xticks([])
    axmatrix.set_yticks([])
    
    return {'ordered' : D, 'rorder' : Z1['leaves'], 'corder' : Z2['leaves']}



# http://nbviewer.ipython.org/github/herrfz/dataanalysis/blob/master/week2/structure_of_a_data_analysis.ipynb


def hcluster_example()
    # load the data
    spam = com.load_data('spam', package='kernlab')
    np.random.seed(3435)
    trainIndicator = np.random.binomial(1, 0.5, 4601)
    #np.bincount(trainIndicator)
    from pandas.tools.plotting import boxplot

    boxplot(trainSpam, column='capitalAve', by='type');
    # take the log
    #
    # here we use the apply() function to compute the log
    df = trainSpam[['capitalAve', 'type']]
    df['capitalAve'] = df['capitalAve'].apply(lambda x: np.log10(x + 1))

    boxplot(df, column='capitalAve', by='type');


    from hcluster import pdist, linkage, dendrogram
    
    dendrogram(linkage(pdist(trainSpam.ix[:,:56].T)), labels=trainSpam.ix[:,:56].columns);
    
    # take the log
    dendrogram(linkage(pdist(trainSpam.ix[:,:55].T.apply(lambda x: np.log10(x + 1)))), labels=trainSpam.ix[:,:55].columns);
    

