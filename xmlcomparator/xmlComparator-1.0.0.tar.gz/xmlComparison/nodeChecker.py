######################  NodeChecker      ##########################
import xml.etree.ElementTree as ElementTree

class NodeManager():
  def __init__(self):
    self.__targetDocRoot = None

  def setTargetFile(self, targetFile):
    self.__targetDocRoot = ElementTree.parse(targetFile).getroot()

  def findNodes(self, entry):
    if self.isRoot(entry):
        return self.__getRootNode(entry)
    else:
      newXpath = self.__getRelativeXpath(entry)
    
      return self.__targetDocRoot.findall(newXpath, entry.nsMap)

  def getNodeTexts(self, nodeList):
    result = []

    for node in nodeList:
      result.append(self.getNodeText(node))

    return result

  def __modifyText(self, text):
  
    return '' if not text else text.strip()
  
  def getNodeText(self, node):
    #http://effbot.org/zone/element.htm
    return self.__modifyText(node.text) + self.__modifyText(self.__getTailText(node))
   
  def __getTailText(self, node):
    tailText = ''
    for childNode in list(node):
      tailText += self.__modifyText(childNode.tail)

    return tailText

  def isRoot(self, entry):
    return entry.xpath.find('/', 2) == -1

  def __getRelativeXpath(self, entry):
     return entry.xpath[entry.xpath.find('/', 2) + 1 :]#skip root node 

  def __getRootNode(self, rootEntry):
    
    rootExists = self.__rootTagMatch(rootEntry) and self.__rootAttributesMatch(rootEntry)

    if not rootExists:
      return []
    else:
      return [self.__targetDocRoot]

  def __rootTagMatch(self, entry):
    sourceTag = entry.getTag()
    targetTag = self.getTagFromNode(self.__targetDocRoot)
    
    return sourceTag == targetTag

  def getTagFromNode(self, node):
    tag = node.tag
    if tag[0] == '{':
      endInd = tag.index('}')
      tag = tag[endInd + 1 : ]

    return tag

  def __rootAttributesMatch(self, entry):
    sourceAttributes = entry.getAttributes()
    
    return self.checkNodeAttributes(self.__targetDocRoot, sourceAttributes)
 
  def checkNodeAttributes(self, node, srcAttributes):
    for key in srcAttributes.keys():
      if not node.get(key):
        return False
      if not srcAttributes[key] == node.get(key):
        return False

    return True

class NodeChecker():
  def __init__(self, diffHandler):
    self.__diffHandler = diffHandler
    self.__nodeManager = NodeManager()

  def check(self, sourceRootEntry, targetFile):
    self.__nodeManager.setTargetFile(targetFile)
    self.__check(sourceRootEntry)
   
  def __check(self, rootEntry):
    if not rootEntry:
      return
    
    nodeExists = self.__checkEntry(rootEntry)
    
    if nodeExists:
      for childEntry in rootEntry.childXpaths:
        self.__check(childEntry)
  
  def __checkEntry(self, entry):
  
    foundNodes = self.__nodeManager.findNodes(entry)
    
    if foundNodes:
      self.__checkTexts(entry, foundNodes)
      return True
    else:
      self.__notifyNodeNotAvailable(entry)
      return False
  
  def __notifyNodeNotAvailable(self, entry):
    try:
      self.__diffHandler.nodeNotAvailable(entry)
    except: 
      pass

  def __notifyTextNotMatch(self, entry, diffTexts):
    try:
      self.__diffHandler.textNotMatch(entry, diffTexts)
    except:
      pass
  
  def __checkTexts(self, entry, foundNodes):
    targetTexts = self.__nodeManager.getNodeTexts(foundNodes)
  
    #print('source texts:' + str(entry.texts))
    #print('target texts:' + str(targetTexts))
 
    diffTexts = self.__diff(entry.texts, targetTexts)

    if diffTexts:
      self.__notifyTextNotMatch(entry, diffTexts)

  def __diff(self, llist, rlist):
    result = []
    for item in llist:
      if not item in rlist:
        result.append(item)
  
    return result

