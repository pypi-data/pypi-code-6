#!/usr/bin/python

# Import stuff:
import argparse 
import itertools
import matplotlib
matplotlib.use('PDF')
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import os
import classes as kiwiC
import functions as kiwiF
import warnings
reload(kiwiC)
reload(kiwiF)

# Handle parsing of arguments:
parser = argparse.ArgumentParser(description='Text')
parser.add_argument('-mn','--metNet', 
    help='Metabolite-metabolite network file name',required=True)
parser.add_argument('-gs','--geneSets',
    help='Gene set statistics file name', required=True)
parser.add_argument('-gm','--geneMet', default="", 
    help='Gene-metabolite association file', required=False)
parser.add_argument('-gl','--geneLevelStats', default="", 
    help='Gene-level statistics file', required=False)
parser.add_argument('-pc','--pCutoff', default=0.01, 
    help='Cutoff p-value for which gene sets to include', required=False)
parser.add_argument('-ad','--pAdjusted', default=True, 
    help='Logical indicating whether to use adjusted p-values or not', required=False)
parser.add_argument('-sc','--splCutoff', default=2, 
    help='Shortest path length cutoff', required=False)
parser.add_argument('-np','--nPerm', default=10000, 
    help='Number of permutations used to generate the gene set p-values', required=False)
parser.add_argument('-sz','--maxGeneSetSize', default=10**6, 
    help='Maximum number of genes in a gene set for it to be kept in the analysis', required=False)
parser.add_argument('-dc','--degreeCutoff', default=10**6, 
    help='Cutoff degree for which gene sets to include', required=False)
parser.add_argument('-ns','--minNodeSize', default=300, 
    help='Minimum node size', required=False)
parser.add_argument('-es','--edgeScaleFactor', default=5, 
    help='Edge width scaling factor', required=False)
parser.add_argument('-ls','--labelSize', default=9, 
    help='Font size for the labels', required=False)
parser.add_argument('-cft','--convertGeneNamesFromType', default="", 
    help='IDs of gene labels to be converted (from mygene.info)', required=False)
parser.add_argument('-ctt','--convertGeneNamesToType', default="", 
    help='IDs of gene labels to convert to (from mygene.info)', required=False)
parser.add_argument('-csp','--convertGeneNamesSpecies', default="", 
    help='Species of gene labels (from mygene.info)', required=False)
parser.add_argument('-on','--networkPlotFile', default="", 
    help='File name to save the output network plot', required=False)
parser.add_argument('-ht','--heatmapType', default="binary", 
    help='Heatmap type, either "binary" or "values"', required=False)
parser.add_argument('-oh','--heatmapPlotFile', default="", 
    help='File name to save the output heatmap plot', required=False)
parser.add_argument('-og','--graphMLFile', default="", 
    help='File name to save the output graph as graphML file', required=False)
args = parser.parse_args()

#Command line arguments are coerced to text:
MNfile      = args.metNet
GSfile      = args.geneSets
GMfile      = args.geneMet
Gfile       = args.geneLevelStats
pcutoff     = float(args.pCutoff)
splcutoff   = int(args.splCutoff)
dcutoff     = int(args.degreeCutoff)
pzero       = 0.1/float(args.nPerm)
minNodeSize = float(args.minNodeSize)
eScaleFac   = float(args.edgeScaleFactor)
labSize     = float(args.labelSize)
nwPlotFile  = args.networkPlotFile
hmType      = args.heatmapType
hmPlotFile  = args.heatmapPlotFile
graphMLFile = args.graphMLFile
adj         = ''
if args.pAdjusted =="True":
    adj = 'adj '
maxGSsize   = float(args.maxGeneSetSize)
cgnFromType = args.convertGeneNamesFromType
cgnToType   = args.convertGeneNamesToType
cgnSpecies  = args.convertGeneNamesSpecies
 
# Check for bad input stuff:
if not os.access(MNfile,os.R_OK): raise IOError("Specified metabolite-metabolite network file cannot be accessed")
if not os.access(GSfile,os.R_OK): raise IOError("Specified gene set statistics file cannot be accessed")
if len(Gfile)==0: warnings.warn('No gene-level statistics files is provided: no heatmap will be generated',RuntimeWarning)
if len(GMfile)==0: warnings.warn('No gene-metabolite association file is provided: no lumping of overlapping gene-sets will be performed\n nor heatmap will be generated',RuntimeWarning)
if not os.access(GMfile,os.R_OK) and len(GMfile) > 0: raise IOError("Specified gene-metabolite association file cannot be accessed")
if not os.access(Gfile,os.R_OK) and len(Gfile) > 0: raise IOError("Specified gene-level statistics file cannot be accessed")
if pcutoff >= 1: raise NameError("pCutoff must be lower than 1")
if pcutoff <= pzero: warnings.warn('pCutoff should be larger than the p-value resolution ('+str(pzero)+')',RuntimeWarning)
if splcutoff < 0: warnings.warn('splCutoff is negative and it has been set to 0','RuntimeWarning')
if pzero >= 1: raise NameError("nPerms is too low")
if minNodeSize <= 0: raise NameError("minNodeSize must be a positive value")
if eScaleFac <= 0: raise NameError("edgeScaleFactor must be a positive value")
if labSize <= 0: raise NameError("minNodeSize must be a positive value")
if minNodeSize <= 0: raise NameError("labelSize must be a positive value")
if not hmType in ["binary","values"]: raise NameError("heatmapType must be either 'binary' or 'values'")
if not args.pAdjusted in ["True","False"]: warnings.warn("pAdjusted not recognised. Argument is ignored (default:'True')")
if maxGSsize <= 0: raise NameError("maxGeneSetSize must be a positive value")

# Make metabolic network MN:
MN = nx.read_edgelist(MNfile,nodetype=str,delimiter='\t')

# Initialize metabolome M:
M = kiwiC.Metabolome()

# Read the metabolites from stats file and add to M:
content = np.genfromtxt(GSfile,dtype=None,delimiter='\t')
header = content[0]
if header[0]!='Name': raise NameError("Gene-set statistic file has invalid header: first column should be named 'Name'.")
if 'p (non-dir.)' in header and 'p (mix.dir.up)' in header and 'p (mix.dir.dn)' in header and 'p (dist.dir.up)' in header and 'p (dist.dir.dn)' in header:
    if len(adj)>0 and 'p adj (non-dir.)' not in header: raise NameError("Gene-set statistics file has invalid header: one column should be named 'p adj (non-dir).' or pAdjusted should be set as 'False'")
    if len(adj)>0 and 'p adj (mix.dir.up)' not in header: raise NameError("Gene-set statistics file has invalid header: one column should be named 'p adj (mix.dir.up).' or pAdjusted should be set as 'False'")
    if len(adj)>0 and 'p adj (mix.dir.dn)' not in header: raise NameError("Gene-set statistics file has invalid header: one column should be named 'p adj (mix.dir.dn).' or pAdjusted should be set as 'False'")
    if len(adj)>0 and 'p adj (dist.dir.up)' not in header: raise NameError("Gene-set statistics file has invalid header: one column should be named 'p adj (dist.dir.up).' or pAdjusted should be set as 'False'")
    if len(adj)>0 and 'p adj (dist.dir.dn)' not in header: raise NameError("Gene-set statistics file has invalid header: one column should be named 'p adj (dist.dir.dn).' or pAdjusted should be set as 'False'")
elif 'p (non-dir.)' in header:
    header[np.where(header=='p (non-dir.)')] = 'p-value'
    if len(adj)>0 and 'p adj (non-dir.)' not in header: raise NameError("Gene-set statistics file has invalid header: one column should be named 'p adj (non-dir).' or pAdjusted should be set as 'False'")
    if 'p adj (non-dir.)' in header:
        header[np.where(header=='p adj (non-dir.)')] = 'p-adj'
elif 'p-value' in header:
    if len(adj)>0 and 'p-adj' not in header: raise NameError("Gene-set statistics file has invalid header: one column should be named 'p-adj' or pAdjusted should be set as 'False'")
else:
    raise NameError("Gene-set statistics file has invalid header.")

for stats in content[1:]:
    stats = tuple(stats)
    m = kiwiC.Metabolite(stats[0])
    m.addGeneSetStats(stats,header,adj)
    M.addMetabolite(m)
if not any([m.pNonDirectional!=np.nan for m in M.metaboliteList]): raise NameError("Invalid data type for gene-set p-value statistic: all values are NaN")
    
# Remove non-significant metabolites and metabolites not in MN and metabolites w high degree:
M.removeNotSignificantMetabolites(pcutoff)    
if len(M.metaboliteList)==0:
    raise NameError('No metabolites passed the pCutoff')
M.removeMetabolitesNotInMetNet(MN)
if len(M.metaboliteList)==0:
    raise NameError('No more metabolites from the gene-set statistics file are present in the metabolite-metabolite network')
if dcutoff < max(nx.degree(MN).values()):
    M.removeHighDegreeMetabolites(MN,dcutoff)
if len(M.metaboliteList)==0:
    raise NameError('No metabolites passed the dCutoff')

# Import the gene-level statistics:
G = kiwiC.Genome()
if len(Gfile)>0:
    content = np.genfromtxt(Gfile,dtype=None,delimiter='\t')
    header = content[0]
    if ('p' not in header) or ('FC' not in header): raise NameError("Gene-level statistics file should contain 'p' and 'FC' as column headers")
    for glstat in content[1:]:
        glstat = tuple(glstat)
        g = kiwiC.Gene(glstat[0])
        p = float(glstat[np.where(header == 'p')[0]])
        FC = float(glstat[np.where(header == 'FC')[0]])
        g.addGeneStats(p,FC)
        G.addGene(g)

if len(GMfile)>0: 
    # Import the gene-metabolite information:
    content      = np.genfromtxt(GMfile,dtype=None,delimiter='\t')
    metList      = np.copy(M.metaboliteList)
    genenameList = []
    for met in metList:
        genenames       = np.unique(np.squeeze(np.asarray((content[np.where(content[:,0]==met.name)[0],1]))))
        genenamesAsList = [g for g in genenames]
        if genenamesAsList in genenameList:
            M.removeMetabolite(met)
            genenameList.append([np.nan])
            metInd = np.where([gl == genenamesAsList for gl in genenameList])[0][0]
            kiwiF.updateLabel(metList[metInd])
        else:
            genenameList.append(genenamesAsList)
            # Check if some genes were excluded by the upstream GSA from a metabolite due to missing stats
            if len(genenames) > maxGSsize:
                M.removeMetabolite(met)
            else:
                for genename in genenames:
                    gene = G.getGene(genename)
                    if isinstance(gene,kiwiC.Gene):
                        met.addGene(gene)
                    else:
                        newGene = kiwiC.Gene(genename)
                        newGene.addGeneStats(p=np.nan,FC=np.nan)
                        G.addGene(newGene)
                        met.addGene(newGene) 

# Construct a dense plot graph:
PG = nx.Graph()
PG.add_nodes_from(M.metaboliteList)
PG.add_edges_from(itertools.combinations(PG.nodes(),2))

# Calculate distance and add to edge property. Add edge weight
for e in PG.edges():
    try:
        PG[e[0]][e[1]]['shortest_path_length'] = nx.shortest_path_length(MN,e[0].name,e[1].name)
    except nx.NetworkXNoPath:
        PG[e[0]][e[1]]['shortest_path_length'] = float('Inf')
    PG[e[0]][e[1]]['weight'] = eScaleFac/PG[e[0]][e[1]]['shortest_path_length']
            
# Remove edges according to shortest path length:
edges_to_remove = [e for e in PG.edges() if PG[e[0]][e[1]]['shortest_path_length']>splcutoff]
PG.remove_edges_from(edges_to_remove)

# Keep only the best edge/s for each node:
all_edges_to_save = []
for met in PG.nodes():
    minspl = float('Inf')
    for e in nx.edges(PG,met):
        minspl = min(minspl,PG[e[0]][e[1]]['shortest_path_length'])
    edges_to_save = [e for e in nx.edges(PG,met) if PG[e[0]][e[1]]['shortest_path_length'] == minspl]
    for e in edges_to_save:
        all_edges_to_save.append(e)
PG.remove_edges_from([e for e in PG.edges() if e not in all_edges_to_save 
    and (e[1],e[0]) not in all_edges_to_save])

# Get edge width for plotting:
edge_width = kiwiF.getEdgeProperty(PG,'weight')

# Get node attribute for plotting:
p          = np.array([[node.pNonDirectional,node.pMixDirUp,node.pDistDirUp,
                        node.pMixDirDn,node.pDistDirDn,node.pValue] for node in PG.nodes()])
p_stable   = p
p_stable[np.isnan(p_stable)] = 1
pzero = min(pzero, pcutoff, p_stable[p_stable!=0].min())
p_stable = p_stable + pzero # Add a small number that is at most 
                              # as high as the smallest non-zero number in p_stable
p_stable   = -np.log10(p_stable)
color_code = (p_stable[:,5] + ((p_stable[:,1]*(p_stable[:,0]+p_stable[:,2]) - 
                p_stable[:,3]*(p_stable[:,0]+p_stable[:,4]))) / 
                (2*p_stable.max()**2))
node_size  = minNodeSize*(p_stable[:,0]+np.log10(pcutoff))+minNodeSize

# Assign plot attributes for a node as node attributes:
k = 0
for node in PG.nodes(): 
    PG.node[node]['directionalityScore'] = float(color_code[k])
    PG.node[node]['-log10p'] = float(p_stable[k,0])
    k = k+1

# Plot network:
fig_nw = plt.figure(figsize=(8,8))
pos=nx.spring_layout(PG,iterations=50,scale=5)
nx.draw(PG, pos, width=edge_width, node_size=node_size, node_color=color_code, cmap=plt.cm.RdBu_r,
        vmin=-abs(color_code).max(), vmax=abs(color_code).max(), with_labels=False)
nx.draw_networkx_labels(PG,pos,dict([[n,n.label] for n in PG.nodes()]), font_size=labSize)
if len(nwPlotFile)>0: 
    plt.savefig(nwPlotFile, bbox_inches='tight')
    plt.close(fig_nw)
else:
    plt.show()
    
# Heatmap:
if len(GMfile)>0 and len(Gfile)>0:
    kiwiF.drawHeatmap(PG,hmType,hmPlotFile,pzero,cgnFromType,cgnToType,cgnSpecies)
        
# Export to graphML:
if len(graphMLFile) > 0:
    nx.write_graphml(PG,graphMLFile)