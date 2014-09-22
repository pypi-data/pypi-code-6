# Agalma - an automated phylogenomics workflow
# Copyright (c) 2012-2014 Brown University. All rights reserved.
#
# This file is part of Agalma.
#
# Agalma is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Agalma is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Agalma.  If not, see <http://www.gnu.org/licenses/>.

"""
For each gene tree generated in genetree, prune the tree to include only one
representative sequence per taxon when sequences form a monophyletic group
(here called 'monophyly masking'). Then prune the monophyly-masked tree into
maximally inclusive subtrees with no more than one sequence per taxon (here
called 'paralogy pruning').

Use either TREE_DIR or --previous for a specific set of trees, otherwise
this pipeline will search for the output from the most recent run of genetree
for the given catalog ID.
"""

import os
import numpy as np
from dendropy import Tree
from glob import glob
from agalma import config
from agalma import database
from biolite import diagnostics
from biolite import report
from biolite import utils
from biolite import workflows
from biolite.pipeline import Pipeline

pipe = Pipeline('treeprune', __doc__)

### ARGUMENTS ###

pipe.add_path_arg('tree_dir', nargs='?', metavar='TREE_DIR', default=None, help="""
	An explicit path to a directory containing a 'RAxML_bestTree.*'
	file for each cluster.""")

pipe.add_arg('--previous', '-p', metavar='RUN_ID', default=None, help="""
	Use the trees from a previous run of genetree.""")

### STAGES ###

@pipe.stage
def init(id, previous, tree_dir):
	"""Determine path to input trees"""
	tree_dir = diagnostics.lookup_prev_val(
				id, previous, tree_dir, 'raxml_dir', 'genetree')
	if not tree_dir:
		utils.die("could not determine tree directory")
	ingest('tree_dir')


@pipe.stage
def prune_trees(tree_dir, outdir):
	"""Prune each tree using monophyly masking and paralogy pruning"""

	prune_dir = os.path.join(outdir, 'pruned-trees')
	pruned_tree_list = []
	utils.safe_mkdir(prune_dir)

	# RAxML generates by default 4 files for each alignment; here we only need
	# the best trees
	for tree_path in glob(os.path.join(tree_dir, 'RAxML_bestTree.*')):
		basename = os.path.basename(tree_path)
		tree = Tree(stream=open(tree_path), schema='newick')
		masked_tree = workflows.phylogeny.monophyly_masking(tree)
		masked_tree.write_to_path(
							os.path.join(prune_dir, basename + '.mm'),
							'newick', as_unrooted=True)
		pruned_trees = []
		workflows.phylogeny.paralogy_prune(masked_tree, pruned_trees)
		for i, tree in enumerate(pruned_trees):
			tree_name = '%s.pp.%d' % (basename, i)
			pruned_tree_list.append(tree_name)
			tree.write_to_path(
							os.path.join(prune_dir, tree_name),
							'newick', as_unrooted=True)

	diagnostics.log('prune_dir', prune_dir)
	diagnostics.log('pruned_tree_list', pruned_tree_list)
	ingest('prune_dir', 'pruned_tree_list')


@pipe.stage
def parse_trees(prune_dir, pruned_tree_list, _run_id):
	"""Parse the tips of each tree to create a cluster in the database"""

	hist = {}
	rows = []
	nseqs = 0

	# Parse each paralogy pruned tree, and create a cluster from the tips
	cluster_id = 0
	for tree_path in glob(os.path.join(prune_dir, '*.pp.*')):
		tree = Tree(stream=open(tree_path), schema='newick', as_unrooted=True)
		nodes = tree.leaf_nodes()
		size = len(nodes)
		# Only keep trees with 3 or more tips
		if size >= 3:
			hist[size] = hist.get(size, 0) + 1
			for node in nodes:
				seq_id = node.get_node_str().partition('@')[-1]
				rows.append((_run_id, cluster_id, seq_id))
			cluster_id += 1
			nseqs += size

	# Write clusters to the database
	database.execute("BEGIN")
	database.execute("DELETE FROM homology WHERE run_id=?;", (_run_id,))
	homology_sql = """
		INSERT INTO homology (run_id, component_id, sequence_id)
		VALUES (?,?,?);"""
	for row in rows:
		database.execute(homology_sql, row)
	database.execute("COMMIT")

	utils.info("histogram of gene cluster sizes:")
	for k in sorted(hist):
		print "%d\t:\t%d" % (k, hist[k])

	diagnostics.log('histogram', hist)
	diagnostics.log('nseqs', nseqs)

	finish('prune_dir', 'pruned_tree_list')


### RUN ###

if __name__ == "__main__":
	# Run the pipeline.
	pipe.run()
	# Push the local diagnostics to the global database.
	diagnostics.merge()

### REPORT ###

class Report(report.BaseReport):
	def init(self):
		self.name = pipe.name
		# Lookups
		self.lookup('histogram', 'treeprune.parse_trees', 'histogram')
		self.str2list('histogram')
		# Gener`ators
		self.generator(self.cluster_histogram)
		self.generator(self.threshold_table)

	def cluster_histogram(self):
		"""
		Distribution of the number of orthologs in each gene cluster.
		"""
		if self.check('histogram'):
			hist = self.data.histogram
			hist = [(k,hist[k]) for k in sorted(hist)]
			if len(hist) > 10:
				# Use a histogram
				imgname = "%d.cluster.hist.png" % self.run_id
				props = {
					'title': "Distribution of Cluster Sizes",
					'xlabel': "# Orthologs in Cluster",
					'ylabel': "Frequency"}
				return [self.histogram_overlay(imgname, [np.array(hist)], props=props)]
			else:
				# Use a table
				return self.table(hist, ('Cluster Size', 'Frequency'))


	def threshold_table(self):
		"""

		"""
		sql = """
			SELECT COUNT(component_id)
			FROM homology
			WHERE run_id=?
			GROUP BY component_id;"""
		genes = {}
		clusters = {}
		for row in database.execute(sql, (self.run_id,)):
			count = row[0]
			for i in xrange(3, count+1):
				genes[i] = genes.get(i, 0) + count
				clusters[i] = clusters.get(i, 0) + 1
		if genes:
			headers = ('Threshold', '# Clusters', '% Missing Genes')
			rows = []
			ntaxa = max(genes.iterkeys())
			for i in sorted(genes.iterkeys()):
				full = clusters[i] * ntaxa
				missing = 100.0 * (full - genes[i]) / full
				rows.append((str(i), str(clusters[i]), '%.1f%%' % missing))
			return self.table(rows, headers)

# vim: noexpandtab ts=4 sw=4
