####  features include:
####  1. order of child nodes are irrelevant  
####  2. auto handling of namespace
####  3. promises: not match reported <=> nonmatch exists; match reported <=> match indeed; reported nonmatch is relevant

####  does not support:
####  1. report accurate nonmatched attributes - nonmatched nodes will be reported in this case
####  2. if two nodes have different attributes, their texts will not be compared

import sys
import xml.sax

from xmlComparison.comparisonHandler import ComparisonHandler
from xmlComparison.namespaceManager import NamespaceManager
from xmlComparison.xpathManager import XpathManager
from xmlComparison.entryTree import EntryTreeCreator
from xmlComparison.nodeChecker import NodeChecker
from xmlComparison.diffHandler import DiffHandler

def compare(firstFile, secondFile):
  print('#' * 60)

  parser = xml.sax.make_parser()

  nsManager = NamespaceManager()
  xpathManager = XpathManager(nsManager)
  entryTreeCreator = EntryTreeCreator(xpathManager)

  handlerList = [nsManager, xpathManager, entryTreeCreator]

  parser.setContentHandler(ComparisonHandler(handlerList))

  parser.parse(firstFile)

  #entryTreeCreator.displayEntryTree()

  diffHandler = DiffHandler()
  diffHandler.setSourceFile(firstFile)
  diffHandler.setTargetFile(secondFile)

  nodeChecker = NodeChecker(diffHandler)

  nodeChecker.check(entryTreeCreator.rootEntry, secondFile)

if __name__ == '__main__':
  firstFile = sys.argv[1]
  secondFile  = sys.argv[2]

  compare(firstFile, secondFile)

  ###################################

  compare(secondFile, firstFile) 
