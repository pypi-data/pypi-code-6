#!/usr/local/bin/python
# -*- coding: utf-8 -*-
'''mktree
'''

import sys, os
import make_GitHub_wiki_tree

if __name__ == '__main__':
  make_GitHub_wiki_tree.mktree_main(os.path.abspath('.'))
