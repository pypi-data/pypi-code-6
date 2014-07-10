extensions = ['sphinxcontrib.bibtex']


author_full = u'Me'
source_suffix = '.rst'
master_doc = 'index-latex'

exclude_patterns = ['_build']

latex_documents = [
  ('index-latex', 'actingeldynamics.tex', u'Actin Gels dynamics',
   author_full, 'manual', False),
]


