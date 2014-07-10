#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from akatsuki.exporter import export_wordpress
from akatsuki.parser import load_bibtex_file
from akatsuki.utils import pmid_to_url, sort_by_date


def main(bibtex_file, html_file):
    """Load BibTeX file and export to WordPress HTML file"""
    entries = load_bibtex_file(bibtex_file)
    entries = pmid_to_url(entries)
    entries = sort_by_date(entries, reverse=True)
    export_wordpress(html_file, entries)
