#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''make_GitHub_wiki_tree
make GitHub wiki tree
'''

import sys, os

def getConf(conf_file):
  return open(conf_file, 'rb').read().splitlines()

__conf__ = getConf(os.path.join(os.path.dirname(__file__), 'conf/setup.cf'))
__version__ = __conf__[0]
__url__ = 'https://github.com/HatsuneMiku/make_GitHub_wiki_tree/wiki'
__author__ = '999hatsune'
__author_email__ = '999hatsune@gmail.com'

CONFFILE = u'mktree.cf'
OUTFILE = [u'Tree.md', u'_Sidebar.md']

def walk(p, depth, uribase, ofp):
  # must be called os.walk with topdown when handling dirnames.pop(-1)
  for pathname, dirnames, filenames in os.walk(p):
    for f in reversed(filenames):
      if f[-3:] != '.md' or f in OUTFILE: continue
      # print 'f: %s %s' % (pathname, f)
      a = b = f[:-3]
      if depth >= 3 and len(a) == 13 and a[:8].isdigit() and a[9:].isdigit():
        y, m, d, n = int(a[:4]), int(a[4:6]), int(a[6:8]), int(a[9:])
        # a = '%04d/%04d%02d/%s' % (y, y, m, a)
        b = '%04d-%02d-%02d_%04d' % (y, m, d, n)
      ofp.write('%*s- [%s](%s%s)\n' % ((depth * 2), ' ', b, uribase, a))
    while len(dirnames):
      d = dirnames.pop(-1)
      if d == '.git': continue
      # print 'd: %s %s' % (pathname, d)
      ofp.write('%*s+ %s\n' % ((depth * 2), ' ', d))
      walk(os.path.join(pathname, d), depth + 1, uribase, ofp)

def mktree(basedir, act, rep, ofp):
  uribase = '/%s/%s/wiki/' % (act, rep)
  ofp.write('Tree\n====\n')
  ofp.write('created automatically\n')
  ofp.write('\n')
  ofp.write('Contents\n--------\n')
  walk(basedir, 1, uribase, ofp)

def mktree_main(basedir):
  cf = os.path.join(basedir, CONFFILE)
  ifp = open(cf, 'rb')
  if ifp is None:
    print u'cannot open %s' % cf
    return
  act, rep = map(lambda s: s.rstrip(), ifp.readlines())
  ifp.close()
  fname = os.path.join(basedir, OUTFILE[0])
  ofp = open(fname, 'wb')
  if ofp is None:
    print u'cannot open %s' % fname
    return
  mktree(basedir, act, rep, ofp)
  ofp.close()
  ifp = open(fname, 'rb')
  ofp = open(os.path.join(basedir, OUTFILE[1]), 'wb')
  ofp.write(ifp.read())
  ofp.close()
  ifp.close()

if __name__ == '__main__':
  mktree_main(os.path.abspath('.'))
