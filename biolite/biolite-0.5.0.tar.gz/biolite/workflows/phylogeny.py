#!/usr/bin/env python
#
# BioLite - Tools for processing gene sequence data and automating workflows
# Copyright (c) 2012-2014 Brown University. All rights reserved.
#
# This file is part of BioLite.
#
# BioLite is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BioLite is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BioLite.  If not, see <http://www.gnu.org/licenses/>.

import dendropy
import numpy as np
import os
from Bio import SeqIO
from collections import OrderedDict, namedtuple
from biolite import diagnostics
from biolite import utils


def get_species(taxon):
	"""
	Parses the species from a taxon name in the format 'species@sequence_id'.
	"""
	return str(taxon).partition('@')[0]


def get_taxa(nodes):
	"""
	Returns a list of taxa names given a list of nodes.
	"""
	return [node.get_node_str() for node in nodes]


def count_orthologs(taxa):
	"""
	Returns the count of orthologs given a list of taxon names. If there are as
	many species as there are taxon names, then the count is the number of
	taxon names. If there are less species than taxon names, then the count is
	0 since there must be some paralogs.
	"""
	species = map(get_species, taxa)
	return len(species) * int(len(species) == len(set(species)))


def monophyly_masking(tree):
	"""
	Takes a tree and identifies clades that have more than one sequence per
	taxon and prunes tip at random leaving a single representative sequence per
	taxon.
	"""
	for node in tree.internal_nodes():
		if node.parent_node:
			tree.reroot_at_node(node)
			for leaf in tree.leaf_nodes():
				sister = leaf.sister_nodes()[0]
				if get_species(leaf.taxon) == get_species(sister.taxon):
					tree.prune_taxa([leaf.taxon], update_splits=False)
	return tree


def split_tree(tree, nodes):
	"""
	Takes a rooted tree and a non-root internal node, and returns the two
	subtrees on either side of that node.
	"""
	assert tree.is_rooted
	root = tree.seed_node

	out = [tree]

	for node in nodes:
		assert node != root
		if node.parent_node:

			# Prune the child subtree from the original tree and reroot it.
			tree.prune_subtree(node, update_splits=False)
			#tree.reroot_at_node(root, update_splits=False)

			# Move the node to a new subtree.
			subtree = dendropy.Tree()
			subtree.seed_node = node
			if node.is_internal():
				subtree.reroot_at_node(node, update_splits=False)

			out.append(subtree)

	# Return both the modified tree and the subtree.
	return out


def paralogy_prune(tree, pruned_trees):
	"""
	Takes a tree and loops through the internal nodes (except root) and gets
	the maximum number of orthologs on either side of each node.
	"""
	# A dictionary will keep track of node (key) and maximum number of
	# orthologs at this node (value). Internal nodes are reported by dendropy
	# in prefix order, so by using an OrderedDict, we will split the tree as
	# close to the root as possible.
	counts = OrderedDict()
	all_leaves = set(get_taxa(tree.leaf_nodes()))

	# Stop at any trees that only have two leaves.
	if len(all_leaves) <= 2:
		pruned_trees.append(tree)
		#print tree.as_newick_string()
		return

	for node in tree.postorder_node_iter():
		child_leaves = set(get_taxa(node.leaf_nodes()))
		other_leaves = all_leaves - child_leaves
		counts[node] = max(
						count_orthologs(child_leaves),
						count_orthologs(other_leaves))
		node.label = str(counts[node])

	#print tree.as_ascii_plot(show_internal_node_labels=True)

	# Calculate the maximum number of orthologs across all nodes.
	all_max = max(counts.itervalues())

	# Create a list of the nodes that have this max value, where we might split
	# the tree.
	splits = filter(lambda node : counts[node] == all_max, counts)
	assert splits

	if splits[0] == tree.seed_node:
		assert len(splits) == 1
		# The tree is pruned and only contains orthologs.
		pruned_trees.append(tree)
	else:
		assert not tree.seed_node in splits
		# Split the tree at the first non-root split node. Because the nodes
		# are in prefix order, this should be close to the root.
		subtrees = split_tree(tree, splits)
		for subtree in subtrees:
			paralogy_prune(subtree, pruned_trees)


def supermatrix(clusters, outdir, partition_prefix='DNA', proportion=None):
	"""
	Build a supermatrix from a list of clusters (as FASTA file names).
	"""

	Gene = namedtuple("Gene", "name seqs")

	taxa = {}
	genes = []

	for cluster in clusters:
		# Build a dictionary of taxa/sequences in this cluster
		gene = Gene(utils.basename(cluster), {})
		for record in SeqIO.parse(cluster, 'fasta'):
			gene.seqs[record.id.partition('@')[0]] = str(record.seq)
		for taxon in gene.seqs:
			taxa[taxon] = taxa.get(taxon, 0) + 1
		genes.append(gene)

	# Sort from best to worst sampled genes.
	genes = sorted(genes, key=(lambda gene: len(gene.seqs)), reverse=True)

	# Sort from best to worst sampled taxa.
	taxa = sorted(taxa, key=taxa.get, reverse=True)
	diagnostics.log("taxa", taxa)

	superseq = dict([(x, []) for x in taxa])
	occupancy = np.zeros((len(genes), len(taxa)), dtype=np.bool)
	cells = np.zeros(len(genes), dtype=np.uint32)
	sites = np.zeros(len(genes), dtype=np.uint32)

	for i, gene in enumerate(genes):

		# Find the maximum sequence length
		maxlen = max(map(len, gene.seqs.itervalues()))
		sites[i] = maxlen

		# Append sequences to the super-sequence, padding out any that
		# are shorter than the longest sequence
		for j, taxon in enumerate(taxa):
			seq = gene.seqs.get(taxon, '')
			if seq:
				superseq[taxon].append(seq)
				occupancy[i,j] = True
				cells[i] += sum(1 for c in seq if c != '-')
			if len(seq) < maxlen:
				superseq[taxon].append('-' * (maxlen - len(seq)))

	cum_occupancy = np.cumsum(np.sum(occupancy, axis=1), dtype=np.float64)
	cum_occupancy /= np.cumsum(len(taxa) * np.ones(len(clusters)))

	nsites = np.sum(sites)
	cell_occupancy = float(np.sum(cells)) / (nsites * len(taxa))

	utils.info("total genes:", len(genes))
	utils.info("total sites:", nsites)
	utils.info("total occupancy: %.2f" % cum_occupancy[-1])
	utils.info("total cell occupancy: %.2f" % cell_occupancy)

	# Use argument 'proportion' to trim supermatrix: find index in
	# cum_occupancy to trim superseq per taxon
	index = len(genes)
	if proportion:
		for i, val in enumerate(cum_occupancy):
			if val < proportion:
				index = i
				break
		if index <= 0:
			utils.die("supermatrix is empty")
		nsites = np.sum(sites[:index])
		cell_occupancy = float(np.sum(cells[:index])) / (nsites * len(taxa))
		utils.info("trimmed genes:", index)
		utils.info("trimmed sites:", nsites)
		utils.info("trimmed occupancy: %.2f" % cum_occupancy[index-1])
		utils.info("trimmed cell occupancy: %.2f" % cell_occupancy)

	diagnostics.log("nsites", nsites)
	diagnostics.log("cell_occupancy", cell_occupancy)

	# Write out supersequence for each taxon

	fasta = os.path.join(outdir, 'supermatrix.fa')
	with open(fasta, 'w') as f:
		for taxon in taxa:
			print >>f, ">%s" % taxon
			print >>f, ''.join(superseq[taxon][:index])

	partition = os.path.join(outdir, 'supermatrix.partition.txt')
	with open(partition, 'w') as f:
		cum_index = 0
		for i in xrange(0, index):
			print >>f, '%s, %s = %d-%d' % (
				partition_prefix, genes[i].name, cum_index+1, cum_index+sites[i])
			cum_index += sites[i]

	occupancy_txt = os.path.join(outdir, 'supermatrix.occupancy.txt')
	with open(occupancy_txt, 'w') as f:
		print >>f, '\t'.join(taxa)
		for row in occupancy[:index]:
			print >>f, '\t'.join(map(str, map(int, row)))

	cum_occupancy_txt = os.path.join(outdir, 'supermatrix.cum_occupancy.txt')
	with open(cum_occupancy_txt, 'w') as f:
		print >>f, '\n'.join(map(str, cum_occupancy[:index]))

	diagnostics.log('fasta', fasta)
	diagnostics.log('partition', partition)
	diagnostics.log('occupancy', occupancy_txt)
	diagnostics.log('cum_occupancy', cum_occupancy_txt)

# vim: noexpandtab ts=4 sw=4
