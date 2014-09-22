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

"""
Provides a framework for generating HTML reports from BioLite diagnostics.
The typical usage is to extend the `BaseReport` class for each pipeline, and
override the `init` method to specify **lookups** and **generators**.

**Lookups** are called with `self.lookup` and specify entities or attributes
that should be loaded from the diagnotics into the `self.data` AttributeDict.
For example::

  self.lookup('args', diagnostics.INIT)

will load the initialization entity, which includes all of the command-line
arguments passed to the pipeline for a given run.

**Generators** are functions that return lists of HTML lines, which are
concatenated together to form the final HTML report, in the order that the
generators are attached. A generator function will typically start by checking
if a diagnostics value was successfully loaded into `self.data`, e.g.::

  def report_arguments(self):
  	if 'args' in self.data:
		html = [self.header('Arguments')]
		html += ['<p>%s</[>' % a for a in self.data.args]
		return html

The generator is attached to the report in the `init` method with the line::

  self.generator(self.report_arguments)

"""

import argparse
import codecs
import os
import re
import shlex
import shutil
import textwrap

from collections import namedtuple, defaultdict, OrderedDict
from docutils.core import publish_parts
from itertools import chain
from operator import attrgetter, itemgetter

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as pyplot
from matplotlib import cm
import numpy as np

import catalog
import database
import diagnostics
import utils
from config import datadir

# From ColorBrewer2, Qualitative, Set3
palette10 = (
	'#8DD3C7',
	'#FFED6F',
	'#BEBADA',
	'#FB8072',
	'#80B1D3',
	'#FDB462',
	'#B3DE69',
	'#FCCDE5',
	'#BC80BD',
	'#CCEBC5')

catalog_schema = [
	('id', "Catalog ID"),
	('species', "Species"),
	('itis_id', "ITIS ID"),
	('library_id', "Library ID"),
	('note', "Note"),
	('sample_prep', "Sample Prep")]

runs_schema = [
	('run_id', 'Run ID'),
	('name', 'Pipelines')]

Field = namedtuple('Field', 'key title type format')

filter_schema = (
	Field('pairs', "Read pairs examined", int, '{:,d}'),
	Field('pairs_kept', "Read pairs kept", int, '{:,d}'),
	Field('percent_kept', "Percent kept", float, '{:.1f}%'),
	Field('quality', "Illumina quality threshold", int, '{:,d}'),
	Field('reject_adapters', "Adapter fails", int, '{:,d}'),
	Field('reject_quality', "Quality fails", int, '{:,d}'),
	Field('reject_content', "Base composition fails", int, '{:,d}'))

insert_schema = (
	Field('mean', "Mean insert size (bp)", float, '{:.2f}'),
	Field('stddev', "Standard deviation (bp)", float, '{:.2f}'))

exclude_schema = (
	Field('pairs', "Read pairs examined", int, '{:,d}'),
	Field('pairs_kept', "Read pairs kept", int, '{:,d}'),
	Field('percent_kept', "Percent kept", float, '{:.1f}%'))

coverage_schema = (
	Field('mean_cov', "Mean coverage", float, '{:.1f}'),
	Field('median_cov', "Median coverage", int, '{:,d}'),
	Field('min_cov', "Min coverage", int, '{:,d}'),
	Field('max_cov', "Max coverage", int, '{:,d}'))

profile_schema = (
	Field('name', 'Command', str, '{}'),
	Field('entity', 'Stage', str, '{}'),
	Field('walltime', 'Wall Time (s)', float, '{:.2f}'),
	Field('usertime', 'User Time (s)', float, '{:.2f}'),
	Field('systime', 'System Time (s)', float, '{:.2f}'),
	Field('maxrss', 'Max Memory (KB)', int, '{:,d}'))

rusage_schema = (
	Field('walltime', 'Wall Time (s)', float, '{:.2f}'),
	Field('usertime', 'User Time (s)', float, '{:.2f}'),
	Field('systime', 'System Time (s)', float, '{:.2f}'),
	Field('maxrss', 'Max Memory (KB)', int, '{:,d}'))

rsem_schema = (
	Field('nreads', "Reads examined", int, '{:,d}'),
	Field('naligned', "Reads aligned", int, '{:,d}'),
	Field('nfailed', "Reads unaligned", int, '{:,d}'))

profile_aggregators = {
	'walltime': sum,
	'usertime': sum,
	'systime': sum,
	'maxrss': max}

def profile_aggregate(profiles):
	"""
	Applies aggregators (sum or max) to fields in the input profiles list.

	Returns a dict of aggregated values.
	"""
	schema = profile_schema[2:]
	values = defaultdict(list)
	aggregates = dict()
	# Collect all the profile entries into lists for each field
	# (e.g. 'walltime', 'mem', etc.)
	for profile in profiles:
		for field in schema:
			if field.key in profile_aggregators:
				try:
					values[field.key].append(field.type(profile[field.key]))
				except KeyError:
					pass
	# Run the aggregators on each of these lists to produce a final
	# list where each entry is the formatted, aggregated value, or
	# '-' if the value list was empty.
	for field in schema:
		if values[field.key]:
			op = profile_aggregators.get(field.key, sum)
			aggregates[field.key] =	op(values[field.key])
	return aggregates

def copy_css(outdir):
	"""
	Copy CSS files and images needed for report templates.
	"""
	css = utils.safe_mkdir(os.path.join(outdir, 'css'))
	shutil.copy(os.path.join(datadir, 'bootstrap.min.css'), css)
	img = utils.safe_mkdir(os.path.join(outdir, 'img'))
	shutil.copy(os.path.join(datadir, 'glyphicons-halflings.png'), img)
	shutil.copy(os.path.join(datadir, 'glyphicons-halflings-white.png'), img)

def copy_js(outdir):
	"""
	Copy Javascript files used for some report features.
	"""
	js = utils.safe_mkdir(os.path.join(outdir, 'js'))
	files = ('d3.min.js', 'jquery.min.js', 'jsphylosvg-min.js', 'raphael-min.js')
	for f in files:
		shutil.copy(os.path.join(datadir, f), js)

def _figure_props(axes, props):
	if 'title' in props:
		axes.set_title(props['title'])
	if 'xlabel' in props:
		axes.set_xlabel(props['xlabel'], fontsize=12)
	if 'ylabel' in props:
		axes.set_ylabel(props['ylabel'], fontsize=12)
	if 'xlim' in props:
		pyplot.xlim(props['xlim'])
	if 'ylim' in props:
		pyplot.ylim(props['ylim'])
	if 'xscale' in props:
		axes.set_xscale(props['xscale'])
	if 'yscale' in props:
		axes.set_yscale(props['yscale'])
	if 'xticks' in props:
		axes.set_xticks(props['xticks'])
	if 'yticks' in props:
		axes.set_yticks(props['yticks'])
	if 'xticklabels' in props:
		axes.set_xticklabels(props['xticklabels'])
	if 'yticklabels' in props:
		axes.set_yticklabels(props['yticklabels'])
	if 'yline' in props:
		for y in props['yline']:
			pyplot.axhline(y=y)
	if 'box' in props:
		pyplot.box(props['box'])

def _figure_create(props={}):
	figure = pyplot.figure(
		figsize=props.get('figsize'),
		dpi=props.get('dpi', 72))
	axes = figure.add_subplot('111')
	_figure_props(axes, props)
	return figure, axes

def _figure_save(figure, outdir, imgname):
	pyplot.tight_layout()
	imgname = utils.safe_str(imgname)
	figure.savefig(os.path.join(outdir, imgname))
	return "<img src=\"{}\"/>".format(imgname)

class BaseReport:
	"""
	A base class that provides basic infrastructure for reporting
	diagnostics via HTML for a given run.

	This is intended to be sub-classed within an BioLite pipeline script,
	to define how the diagnostics for that pipeline should be summarized
	and plotted.
	"""

	def __init__(self, id, run_id, outdir=None, verbose=False, hlevel=1):
		"""
		Override init() instead of this function.
		"""
		self.id = id
		self.run_id = run_id
		self.outdir = outdir
		self.verbose = verbose
		self.hlevel = hlevel
		self.name = ''
		self.data = utils.AttributeDict()
		self.js = []
		self.generators = []
		self.init()
		self.lookup('profile', "%s.*.profile" % self.name,
												func=diagnostics.lookup_like)
		self.generator(self.profile_table)

	def __repr__(self):
		if self.data:
			return True
		return False

	def __str__(self):
		if self.data:
			html = []
			for func in self.generators:
				func_html = func()
				if func_html:
					html += func_html
					if func.__doc__:
						doc = publish_parts(
								textwrap.dedent(func.__doc__),
								writer_name='html')
						html.append('<blockquote>%s</blockquote>' % doc['body'])
			# Join lines, collapse tabs and ignore empty lines in output.
			return '\n'.join([line.replace('\t','') for line in html if line])
		else:
			return ''

	def init(self):
		"""
		Override this function with a series of lookup() and generator()
		calls that specify the diagnostics lookups needed by your report, and
		the sub-class functions that generate the HTML output.
		"""
		pass

	def lookup(self, name, entity, attribute=None, func=diagnostics.lookup):
		"""
		Lookup data from the diagnotics table for `entity` and store
		it in the `self.data` dict.

		Optionally, specify the lookup `func` to use from the `diagnotics`
        module.
		"""
		values = func(self.run_id, entity)
		if values:
			if attribute:
				try:
					self.data[name] = values[attribute]
				except KeyError:
					pass
			else:
				self.data[name] = values

	def lookup_attribute(self, entity, attribute, func=diagnostics.lookup):
		"""
		Lookup a single `attribute` from `entity` in the diagnostics table
		and store it in the `self.data` dict with name `attribute`.

		Optionally, specify the lookup `func` to use from the `diagnotics`
        module.
		"""
		values = func(self.run_id, entity)
		try:
			self.data[attribute] = values[attribute]
		except KeyError:
			pass

	def lookup_unpack(self, entity, func=diagnostics.lookup):
		"""
		Lookup data from the diagnotics table for `entity` and store
		it in the `self.data` dict, unpacking each attribute in the `entity`
		as a name in `self.data`.

		Optionally, specify the lookup `func` to use from the `diagnotics`
        module.
		"""
		values = func(self.run_id, entity)
		for attribute in values:
			self.data[attribute] = values[attribute]

	def extract_arg(self, entity, arg):
		"""
		Parse the 'command' attrbute of 'entity' to find the value for the
		argument 'arg'.
		"""
		command = diagnostics.lookup(self.run_id, entity).get('command')
		if command:
			args = shlex.split(str(command))
			for i, a in enumerate(args):
				if a == arg and (i+1) < len(args):
					return args[i+1]
			utils.info("no argument '%s' for command in '%s' for run %d" % (arg, entity, int(self.run_id)))
		else:
			utils.info("could not find 'commmand' in entity '%s' for run %d" % (entity, int(self.run_id)))
		return None

	def add_js(self, name):
		"""
		Copy a Javascript file from the BioLite share directory, and include
		a reference to it in the HTML output. Current options are:

		* d3.min.js
		* jsphylosvg-min.js
		* raphael-min.js

		"""
		if not name in ('d3.min.js', 'jsphylosvg-min.js', 'raphael-min.js'):
			utils.info("warning: javascript name '%s' unrecognized" % name)
		self.js.append(name)
		shutil.copy(
			os.path.join(datadir, name),
			utils.safe_mkdir(os.path.join(self.outdir, 'js')))

	def get_js(self):
		return map('<script type="text/javascript" src="js/{}"></script>'.format, self.js)

	def generator(self, func):
		"""
		Add functions in your sub-class to the 'generators' list, and their
		list-of-strings output will be appended in order to the output of the
		object's __repr__ function.
		"""
		self.generators.append(func)

	def check(self, *args):
		"""
		Check if multiple keys are in the report's data dictionary. Return
		true if all exists, otherwise false.
		"""
		for name in args:
			if name not in self.data:
				return False
		return True

	def zip(self, *args):
		"""
		Zip together multiple items from the report's data dictionary.
		"""
		return zip(*[self.data[arg] for arg in args])

	def header(self, html, level=0):
		return "<h{0}>{1}</h{0}>".format(self.hlevel + level, html)

	def percent(self, data_name, field_name, num, div):
		try:
			data = self.data[data_name]
			data[field_name] = 100.0 * float(data[num]) / float(data[div])
		except KeyError:
			pass

	def str2list(self, name):
		"""
		Converts a diagnostics string with key `name` in `self.data` into a
		list, by parsing it as a typical Python list representation
		:samp:`[item1, item2, ... ]`.
		"""
		if name in self.data:
			self.data[name] = diagnostics.str2list(self.data[name])

	def summarize(self, schema, name, attr=None):
		"""
		Returns a 2-column summary table of a pipeline's key statistics.
		"""
		if name in self.data:
			html = ['<table class="table table-striped table-condensed table-mini">']
			if attr is not None:
				data = self.data[name][attr]
			else:
				data = self.data[name]
			for field in schema:
				row = "<tr><td><b>%s</b></td><td class=\"right\">%s</td></tr>"
				value = data.get(field.key)
				if not value is None:
					html.append(row % (
							field.title,
							field.format.format(field.type(data[field.key]))))
				else:
					html.append(row % (field.title, '-'))
			html.append("</table>")
			return html

	def table(self, rows, headers=None, style=None):
		"""
		Returns an HTML table with a row for each tuple in `rows`, and an
		option header row for the tuple `headers`. The `style` string
		indicates justification for a column as either l (left) or r (right).
		For example, 'lr' prints a table with the first column left-justified
		and the second column right-justified.
		"""
		styles = {'c': " style=\"text-align:center\"", 'r': " style=\"text-align:right\""}
		html = ['<table class="table table-striped table-condensed table-mini">']
		if style:
			style = [styles.get(s, '') for s in style]
		else:
			style = [''] * max(map(len, rows))
		if headers:
			html.append("<tr>")
			html += map("<td{0[0]}>{0[1]}</td>".format, zip(style, headers))
			html.append("</tr>")
		for row in rows:
			html.append("<tr>")
			html += map("<td{0[0]}>{0[1]}</td>".format, zip(style, row))
			html.append("</tr>")
		html.append("</table>")
		return html

	def histogram(self, imgname, data, bins=100, props={}):
		"""
		Plots a histogram in dict `data` with the given number of `bins`
		to the file `imgname`. The keys of the dict should correspond to
		bins with width 1, and the values to frequencies.
		"""
		props['figsize'] = props.get('figsize', (9,3))

		xmax = max(data.iterkeys())
		bins = min(xmax + 1, bins)
		binsize = ((xmax - 1) / bins) + 1

		# Rebin.
		old_data = data
		data = np.zeros(bins)
		for i, count in old_data.iteritems():
			data[i / binsize] += count

		# Create an x range with the bin size.
		halfbin = 0.45 * float(binsize)
		xlim = (-halfbin, binsize * data.size - halfbin)
		x = np.arange(xlim[0], xlim[1], binsize)

		# Create the figure.
		props['xlim'] = props.get('xlim', xlim)
		props['yticks'] = props.get('yticks', [0, max(data)])
		figure, axes = _figure_create(props)
		axes.bar(x, data,
			width=props.get('width', 0.9 * binsize),
			color=props.get('color', 'r'))
		return _figure_save(figure, self.outdir, imgname)

	def histogram_categorical(self, imgname, data, props={}):
		"""
		Plots a histogram in dict `data` to the file `imgname`, using the keys
		as categories and values as frequencies.
		"""
		props['figsize'] = props.get('figsize', (9,3))

		categories = sorted(data)
		frequencies = map(data.get, categories)

		# Create the figure.
		props['xlim'] = props.get('xlim', [-1.0, len(data)])
		props['xticks'] = props.get('xticks', np.arange(len(data)))
		props['xticklabels'] = props.get('xticklabels', map(str, categories))
		props['yticks'] = props.get('yticks', [0, max(frequencies)])
		figure, axes = _figure_create(props)
		axes.bar(np.arange(len(data)) - 0.45, frequencies,
			width=props.get('width', 0.9),
			color=props.get('color', 'r'))
		return _figure_save(figure, self.outdir, imgname)

	def histogram_overlay(self, imgname, hists, labels=None, bins=100, props={}):
		"""
		Plots up to 3 histograms over each other. Histograms are plotted in the
		order of the hists list, so that the last histogram is the topmost.
		The histograms are plotted with alpha=0.5 and colors red, blue, green.
		"""

		colors = ('r', 'b', 'g')
		props['figsize'] = props.get('figsize', (9,3))

		xmax = max([hist[:,0].max() for hist in hists])

		# Rebin.
		binsize = ((xmax - 1) / bins) + 1
		rebin = list()
		for hist in hists:
			rebin.append(np.zeros(bins))
			for i in xrange(hist.shape[0]):
				rebin[-1][int(hist[i][0] / binsize)] += hist[i][1]

		ymax = max([hist.max() for hist in rebin])
		padding = 0.04 * ymax

		# Add padding to non-zero bins.
		for hist in rebin:
			hist[hist.nonzero()] += padding

		# Create an x range with the bin size.
		x = np.arange(0, binsize * bins, binsize)

		figure, axes = _figure_create(props)

		if not labels:
			labels = [None] * len(hists)
		for y, label, c in zip(rebin, labels, colors):
			axes.bar(x, y, label=label, color=c, width=binsize, alpha=0.5, bottom=-padding)
		axes.set_xlim([0, binsize * bins])
		axes.set_xticks([i * binsize * bins / 10 for i in range(0,11)])
		axes.set_xticks([i * binsize  for i in range(0,bins+1)], minor=True)
		axes.set_ylim([-padding, ymax])
		if ymax > 1:
			axes.set_yticks([1, ymax])
			pyplot.axhline(y=0, color='k')
		else:
			axes.set_yticks([ymax])
		font = matplotlib.font_manager.FontProperties()
		font.set_size('small')
		axes.legend(loc=props.get('loc'), prop=font)
		return _figure_save(figure, self.outdir, imgname)

	def barplot(self, imgname, data, props={}):
		"""
		Plots bars for a dict `data` to the file `imgname`, using the keys
		as categories and values as heights.
		"""
		props['figsize'] = props.get('figsize', (9,3))

		categories = sorted(data)
		frequencies = map(data.get, categories)

		# Create the figure.
		props['xlim'] = props.get('xlim', [-1.0, len(data)])
		props['xticks'] = props.get('xticks', np.arange(len(data)))
		props['xticklabels'] = props.get('xticklabels', map(str, categories))
		figure, axes = _figure_create(props)
		axes.bar(np.arange(len(data)) - 0.45, frequencies,
			width=props.get('width', 0.9),
			color=props.get('color', 'r'))
		return _figure_save(figure, self.outdir, imgname)

	def scatterplot(self, imgname, plot, props={}):
		"""
		Plots the (X,Y) points given in `plot` to the file `imgname`.

		`plot` should be a tuple of the form `(x, y, ...)` where x and y
		are list or nparray objects and any additional fields are parameters
		to the matplotlib `plot` function (such as color or label).
		"""
		# Create the figure.
		figure, axes = _figure_create(props)
		axes.plot(*plot)
		return _figure_save(figure, self.outdir, imgname)

	def multiscatterplot(self, imgname, plots, props={}):
		"""
		Plots multiple sets of (X,Y) points given in `plots` to the file
		`imgname`.

		`plots` should be a list of tuples of the form `(x, y, color, label)`
		where x and y are list or nparray objects, color is a matplotlib color
		specification (for instance, 'r' for red) and label is a string.
		"""
		# Create the figure.
		figure, axes = _figure_create(props)
		for x, y, c, label in plots:
			axes.plot(x, y, c, label=label, mfc='none', mec=c[0])
		font = matplotlib.font_manager.FontProperties()
		font.set_size('small')
		axes.legend(loc=props.get('loc'), prop=font)
		return _figure_save(figure, self.outdir, imgname)

	def lineplot(self, imgname, data, props={}):
		"""
		Plots a single line for the values in `data` to the file `imgname`.
		"""
		# Create the figure.
		figure, axes = _figure_create(props)
		axes.plot(data, color=props.get('color', 'r'))
		return _figure_save(figure, self.outdir, imgname)

	def multilineplot(self, imgname, plots, props={}):
		"""
		Plots multiple lines, one for each `(x, y, label)` tuple in the
		`plots` list, to the file `imgname`.
		"""
		# Create the figure.
		figure, axes = _figure_create(props)
		for x, y, label in plots:
			axes.plot(x, y, label=label,
				marker=props.get('marker'), mfc=props.get('mfc'))
		font = matplotlib.font_manager.FontProperties()
		font.set_size('small')
		axes.legend(loc=props.get('loc', 'lower right'), prop=font)
		return _figure_save(figure, self.outdir, imgname)

	def imageplot(self, imgname, matrix, props={}, vmin=0.0, vmax=1.0):
		"""
		Plots a 2D `matrix` as an image to the filename `imgname`.
		"""
		# Create the figure.
		figure, axes = _figure_create(props)
		axes.set_rasterization_zorder(1)
		axes.imshow(matrix, cmap=cm.gray, interpolation='none', aspect='auto', vmin=vmin, vmax=vmax, zorder=0)
		return _figure_save(figure, self.outdir, imgname)

	def profile_table(self):
		# CPU and memory usage for each command called by this pipeline.
		if 'profile' in self.data:
			html = [self.header("Resourse Usage")]
			# The aggregate row always gets written.
			agg = profile_aggregate(self.data.profile.values())
			html += ["<table class=\"table\">", "<tr>"]
			for field in profile_schema:
				if field.key in profile_aggregators:
					html.append('<th>%s</th>' % field.title)
			html.append('</tr>')
			for field in profile_schema:
				if field.key in profile_aggregators:
					try:
						s = field.format.format(field.type(agg[field.key]))
					except:
						s = '-'
					op = profile_aggregators.get(field.key, sum).__name__
					html.append('<td class="right">%s [%s]</td>' % (s, op))
			html += [ '</tr>', '</table>' ]
			# The detailed rows are hidden by default.
			html += [
				'<a class="btn btn-info" onclick="togglestats(this)"><i class="icon-list-alt icon-white"></i> Show/hide details</a>',
				'<table class="stats table table-striped table-condensed">']
			headers = [field.title for field in profile_schema]
			# Write the column headers.
			html.append("<tr><th>")
			html.append("</th><th>".join(headers))
			html.append("</th></tr>")
			# Write the values.
			for entity in self.data.profile:
				profile = self.data.profile[entity]
				tokens = entity.split('.')
				profile['entity'] = '.'.join(tokens[1:-2])
				html.append("<tr>")
				# First two columns are strings and don't use "right" <td>
				for field in profile_schema[:2]:
					try:
						html += [
							"<td>",
							field.format.format(field.type(profile[field.key])),
							"</td>"]
					except KeyError:
						html.append("<td class=\"center\">&ndash;</td>")
				for field in profile_schema[2:]:
					try:
						html += [
							"<td class=\"right\">",
							field.format.format(field.type(profile[field.key])),
							"</td>"]
					except KeyError:
						html.append("<td class=\"center\">&ndash;</td>")
				html.append("</tr>")
			html += ["</tr>", "</table>"]
			return html


class Tag:
	"""
	Utility class for representing an HTML tag, with an option to export as a
	CSV value.
	"""

	def __init__(self, tag, value, *attributes):
		self.value = value
		self.string = '<%s>%s</%s>' % (' '.join(chain((tag,), attributes)), value, tag)

	def __str__(self):
		return self.string

	def csv(self):
		"""Reformat CSV output for easy import into R."""
		s = unicode(self.value)
		if s == u'-' or s == u'None' or s == u'':
			# Change blank values to the special string 'NA'.
			return u'NA'
		else:
			# Remove percent signs and commas from all values.
			return s.replace('%', '').replace(',','')

Column = namedtuple("Column", "name fmt")
Lookup = namedtuple("Lookup", "name key type")

class TabularReport:
	"""
	"""

	ITIS_URL = "http://www.itis.gov/servlet/SingleRpt/SingleRpt?search_topic=TSN&search_value="

	def __init__(self, title="Biolite Tabular Report"):
		"""
		"""
		parser = argparse.ArgumentParser(description="""
			Generates an HTML report comparing in tabular format all runs in the
			diagnostics database (by default), or of only the specified list
			of RUN_IDs.""")
		parser.add_argument('--outdir', '-o', default='.', help="""
			write HTML and CSV output to OUTDIR [default: .]""")
		parser.add_argument('--multiline', '-m', action='store_true', help="""
			one line per run, including multiple runs of the same pipeline for
			a catalog ID [default: only the most recent runs]""")
		parser.add_argument('--hidden', action='store_true', help="""
			include runs that are marked as hidden [default: False]""")
		parser.add_argument('run_ids', metavar='RUN_ID', nargs='*', help="""
			include only the specified list of run IDs""")
		self.parser = parser

		self.title = title
		self.default_format = '{}'
		self.lookups = {}
		self.transforms = OrderedDict()
		self.groups = OrderedDict()
		self.headers = [('Run', len(runs_schema)), ('Catalog', len(catalog_schema))]

	def set_default_format(self, fmt):
		"""
		Set the default format to use the `type` function and the `fmt`
		format string. This is (str, '{}') by default.
		"""
		self.default_format = fmt

	def add_lookup(self, entity, *attributes):
		"""
		"""
		lookups = []
		for attr in attributes:
			if isinstance(attr, basestring):
				lookups.append(Lookup(attr, attr, str))
			elif len(attr) == 1:
				lookups.append(Lookup(attr[0], attr[0], str))
			elif len(attr) == 2:
				lookups.append(Lookup(attr[0], attr[1], str))
			elif len(attr) == 3:
				lookups.append(Lookup(*attr))
		self.lookups[entity] = lookups

	def add_transform(self, key, f):
		"""
		"""
		self.transforms[key] = f

	def add_group(self, title, *columns):
		"""
		"""
		group = []
		for column in columns:
			if isinstance(column, basestring):
				group.append(Column(column, self.default_format))
			elif len(column) == 1:
				group.append(Column(column[0], self.default_format))
			elif len(column) == 2:
				group.append(Column(*column))
		self.groups[title] = group
		self.headers.append((title, len(group)))

	def run(self):
		"""
		"""
		# Parse args
		args = self.parser.parse_args()
		outdir = utils.safe_mkdir(args.outdir)
		if args.run_ids:
			runs = map(diagnostics.lookup_run, args.run_ids)
		else:
			runs = diagnostics.lookup_runs()

		rows = defaultdict(list)
		for run in runs:
			if not run.done:
				utils.info("skipping incomplete run", run.run_id)
				continue
			if (not args.hidden) and run.hidden:
				utils.info("skipping hidden run", run.run_id)
				continue
			rows[run.id].append(run)
		if args.multiline:
			pass

		# Build subheaders from schema
		subheaders = map(itemgetter(1), runs_schema + catalog_schema)
		csv_subheaders = list(subheaders)
		for group in self.groups.itervalues():
			subheaders += [column.name.partition('$')[0] for column in group]
			csv_subheaders += [column.name for column in group]
		ncolumns = len(subheaders)

		# Build table through diagnostics lookups
		table = []
		for id in sorted(rows):
			runs = rows[id]
			data = {}
			for run in runs:
				for entity, lookups in self.lookups.iteritems():
					values = diagnostics.lookup(run.run_id, entity)
					for lookup in lookups:
						val = values.get(lookup.key)
						if val is not None:
							data[lookup.name] = lookup.type(val)
			for key in self.transforms:
				try:
					data[key] = self.transforms[key](data)
				except KeyError as e:
					utils.info("bad key", e, "in transform for id", id)
			row = [Tag('td', '-')] * ncolumns
			row[0] = Tag('td', ','.join(utils.number_range(map(attrgetter('run_id'), runs))), 'class="right"')
			row[1] = Tag('td', ('/'.join(map(attrgetter('name'), runs))))
			record = catalog.select(id)
			if not record:
				record = catalog.make_record(id=id)
			record = record._asdict()
			if record['itis_id']:
				record['itis_id'] = "<a href=\"{0}{1}\">{1}</a>".format(self.ITIS_URL, record['itis_id'])
			for i, field in enumerate(map(itemgetter(0), catalog_schema), start=2):
				if record[field]:
					row[i] = Tag('td', str(record[field]))
			for run in runs:
				j = i + 1
				for columns in self.groups.itervalues():
					for column in columns:
						val = data.get(column.name)
						if val is not None:
							row[j] = Tag('td', column.fmt.format(val), 'class="right"')
						j += 1
			table.append(row)

		# Write HTML
		html = [
			'<table class="table table-striped sortable">',
			'<thead>',
			'<tr>',
			'\n'.join(['<th colspan="%d"><h4>%s</h4></th>' % (d,s) for s,d in self.headers]),
			'</tr>',
			'<tr>',
			'\n'.join(['<th><h6>%s</h6></th>' % s for s in subheaders]),
			'</tr>',
			'</thead>',
			'<tbody>']
		for row in table:
			html.append('<tr>%s</tr>' % ''.join(map(str, row)))
		html += ['</tbody>', '</table>']

		with codecs.open(os.path.join(outdir, 'index.html'), 'w', 'utf-8') as f:
			for line in codecs.open(os.path.join(datadir, 'tabular_report.html'), 'r', 'utf-8'):
				if line == '%%CONTENT%%\n':
					for line in html:
						print >>f, line
				elif '%%TITLE%%' in line:
					print >>f, line.replace('%%TITLE%%', self.title),
				else:
					f.write(line)

		# Write CSV
		with codecs.open(os.path.join(outdir, 'index.csv'), 'w', 'utf-8') as f:
			print >>f, ','.join(csv_subheaders)
			for row in table:
				print >>f, ','.join(cell.csv() for cell in row)

# vim: noexpandtab ts=4 sw=4
