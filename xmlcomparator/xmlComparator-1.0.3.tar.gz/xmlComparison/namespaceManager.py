#######################  NamespaceManager ##########################
from .util import Stack 

class NsEntry:
  def __init__(self):
    self.defaultNsPrefix = ''
    self.namespaceMap = {}

class NamespaceManager:
  def __init__(self):
    self.__autoIndex = 0;
    self.__nsStack = Stack()

  def elementStart(self, tagName, attributes):
    nsEntry = NsEntry()
    self.__fillNsEntry(nsEntry, attributes)
    self.__nsStack.push(nsEntry)

  def __fillNsEntry(self, nsEntry, attributes):
    defaultNsAttribute = 'xmlns'
     
    for key in attributes.keys():
      if key == defaultNsAttribute:
        nsValue = attributes[key]
        defaultNsPrefix = self.__getNewNsPrefix()
        nsEntry.defaultNsPrefix = defaultNsPrefix
        nsEntry.namespaceMap[defaultNsPrefix] = nsValue
      elif key.startswith(defaultNsAttribute + ':'):
        nsPrefix = key[key.index(':') + 1 : ]
        nsEntry.namespaceMap[nsPrefix] = attributes[key] 
 
  def __getNewNsPrefix(self):
    nsPrefix = "n" + str(self.__autoIndex)
    self.__autoIndex += 1
    return nsPrefix 

  def onText(self, data):
    pass

  def elementEnd(self, name):
    self.__nsStack.pop()

  def getDefaultNsPrefix(self):
    
    for nsEntry in self.__nsStack[::-1]:
      if nsEntry.defaultNsPrefix:
        return nsEntry.defaultNsPrefix

    return ''

  def getNsMap(self):
    nsMap = {'xml' : 'http://www.w3.org/XML/1998/namespace'}

    for nsEntry in self.__nsStack[::-1]:
      for key in nsEntry.namespaceMap.keys():
        if not key in nsMap:
          nsMap[key] = nsEntry.namespaceMap[key]

    return nsMap


