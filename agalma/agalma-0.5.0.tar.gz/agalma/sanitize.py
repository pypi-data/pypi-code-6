# Agalma - Tools for processing gene sequence data and automating workflows
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
Filters raw paired-end Illumina data to remove very low quality read pairs,
read pairs with adapter sequences, and read pairs with highly skewed base
composition. It then randomizes the order of reads in the files (applying
the same order of randomization to each file in the pair) to make it simple
to get random subsets of read pairs in later analyses. Finally, fastqc is
run to profile the quality of the reads.
"""

import os
import glob
import shutil
from agalma import config
from biolite import diagnostics
from biolite import report
from biolite import utils
from biolite import wrappers
from biolite.pipeline import IlluminaPipeline

pipe = IlluminaPipeline('sanitize', __doc__)

### ARGUMENTS ###

pipe.add_arg('--quality', '-q', type=int, metavar='MIN', default=28, help="""
	Filter out reads that have a mean quality < MIN.""")

pipe.add_arg('--nreads', '-n', type=int, metavar='NUM', default=None, help="""
	Consider only the first NUM reads that pass filter, others are discarded""")

### STAGES ###

@pipe.stage
def fastqc(id, data, outdir):
	"""Prepare fastqc report for the first 100K reads"""

	for i, fastq in enumerate(data[-1]):
		# Use the first 100k reads for faster runtime.
		subset = "%s.random100k.%d.fq" % (id, i+1)
		# (4 lines per record * 100k records = 400k lines)
		utils.head_to_file(fastq, subset, n=400000, gunzip=fastq.endswith(".gz"))
		wrappers.FastQC(subset, '-o', outdir)


@pipe.stage
def sanitize(id, data, outdir, gzip, quality, nreads):
	"""Filter out low-quality and adapter-contaminated reads"""

	sanitized = os.path.abspath('reads.sanitized')
	sanitized = ['%s.%d.fq' % (sanitized, i) for i,_ in enumerate(data[-1])]
	if gzip:
		sanitized = [f+'.gz' for f in sanitized]

	wrappers.FilterIllumina(
				data[-1], sanitized, '-q', quality, '-s', '/', '-n', nreads)

	data.append(sanitized)
	finish('data')


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
		self.lookup('outdir', diagnostics.INIT, 'outdir')
		self.lookup('filter', 'sanitize.sanitize.filter_illumina')
		self.percent('filter', 'percent_kept', 'pairs_kept', 'pairs')
		self.lookup(
			'hist', 'sanitize.sanitize.filter_illumina', 'quality_histogram')
		self.str2list('hist')
		if 'filter' in self.data:
			# Pull the quality treshold out of the command arguments.
			self.data.filter['quality'] = self.extract_arg(
									'sanitize.sanitize.filter_illumina', '-q')
		# Generators
		self.generator(self.filter_table)
		self.generator(self.fastqc_table)
		self.generator(self.quality_histogram)

	def filter_table(self):
		"""

		"""
		if 'filter' in self.data:
			html = [self.header("Illumina Filtering")]
			html += self.summarize(report.filter_schema, 'filter')
			return html

	def fastqc_table(self):
		"""
		FastQC_ is a tool from Babraham Bioinformatics that generates detailed
		quality diagnostics of NGS sequence data.

		.. _FastQC: http://www.bioinformatics.babraham.ac.uk/projects/fastqc/
		"""
		if 'outdir' in self.data:
			fastqc_dirs = glob.glob(os.path.join(self.data.outdir, '*_fastqc'))
			if fastqc_dirs:
				html = [self.header("FastQC reports")]
				html.append("<table cellpadding=\"5\"><tr>")
				html += self.copy_fastqc(fastqc_dirs)
				html.append("</tr></table>")
				return html

	def copy_fastqc(self, fastqc_dirs):
		"""
		Make local copies of fastqc reports.
		"""
		html = []
		for i in xrange(len(fastqc_dirs)):
			path = fastqc_dirs[i]
			if os.path.isdir(path):
				name = os.path.basename(path)
				newname = "%d.fastqc.%d" % (self.run_id, i+1)
				dest = os.path.join(self.outdir, newname)
				if not os.path.isdir(dest):
					shutil.copytree(path, dest)
				html += [
					"<td>",
					self.header("<a href=\"{0}/fastqc_report.html\">{0}</a>", level=1).format(newname),
					"<pre>"]
				for line in open(os.path.join(path, 'summary.txt')):
					html.append(self.tidy_fastqc_item(line, name))
				html.append("</pre></td>")
		return html

	def tidy_fastqc_item(self, item, fastqc_name):
		# Add colors for pass/fail.
		item = item.replace('PASS', "<span style=\"color: green;\">PASS</span>")
		item = item.replace('FAIL', "<span style=\"color: red;\">FAIL</span>")
		# Tabs to spaces.
		item = item.replace('\t',' ')
		# Remove long name.
		fastqc_name = fastqc_name[:fastqc_name.rfind('_fastqc')]
		item = item[:item.find(fastqc_name)]
		return item

	def quality_histogram(self):
		"""
		Histogram of mean quality scores.
		"""
		if self.check('hist'):
			imgname = '%d.quality_histogram.svg' % self.run_id
			props = {
				'xlabel': "Mean Quality Score",
				'ylabel': "Frequency"}
			return [self.histogram(imgname, self.data.hist, props=props)]

# vim: noexpandtab ts=4 sw=4
