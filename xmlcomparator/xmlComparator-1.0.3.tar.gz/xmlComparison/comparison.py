import xml.sax
import xml.sax.handler

from .namespaceManager import NamespaceManager
from .xpathManager import XpathManager
from .entryTree import EntryTreeCreator
from .nodeChecker import NodeChecker
from .diffHandler import DiffHandler

class ComparisonHandler(xml.sax.handler.ContentHandler):
  
  def __init__(self, listenerList):
    self.__listenerList = listenerList

  def startElement(self, name, attributes):
    for handler in self.__listenerList:
      #try:
        handler.elementStart(name, attributes)
      #except:
      #  pass
      
  def characters(self, data):
    for handler in self.__listenerList:
      #try:
        handler.onText(data)
      #except:
      #  pass

  def endElement(self, name):
    for handler in self.__listenerList[::-1]:
      #try:
        handler.elementEnd(name)
      #except:
      #  pass

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

