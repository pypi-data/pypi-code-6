#######################  EntryTreeCreator ##########################
from .util import Stack

class Entry():
  def __init__(self, xpathManager):
    self.xpathManager = xpathManager
    self.xpath = ''
    self.nsMap = {}
    self.texts = ['']
    self.childXpaths = []

  def getTag(self):
    
    return self.xpathManager.getTagFromXpath(self.xpath)
    
  def getAttributes(self):
    return self.xpathManager.getAttributesFromXpath(self.xpath)

class EntryTreeCreator():
  def __init__(self, xpathManager):
    self.__xpathManager = xpathManager
    self.__entryStack = Stack()
    self.rootEntry = None

  def elementStart(self, name, attributes):
    entry = Entry(self.__xpathManager)
    entry.xpath = self.__xpathManager.getXpath()
    entry.nsMap = self.__xpathManager.getNsMap()
    self.__entryStack.push(entry)

  def onText(self, data):
    entry = self.__entryStack.peek()
    entry.texts[0] += data.strip()

  def elementEnd(self, name):
    currentEntry = self.__entryStack.pop()
    self.__mergeEntries(currentEntry.childXpaths)

    parentEntry = self.__entryStack.peek()
    if parentEntry:
      parentEntry.childXpaths.append(currentEntry)
    else:
      self.rootEntry = currentEntry

  def __mergeEntries(self, entryList):
    groups = self.__groupEntries(entryList)
    entryList.clear()

    for group in groups:
      if len(group) == 1:
        entryList.append(group[0])
      else:
        entryList.append(self.__mergeEqualEntries(group))

  def __groupEntries(self, entryList):
    entryMap = {}
    
    for entry in entryList:
      key = entry.xpath
      value = entryMap.get(key, [])
      value.append(entry)
      entryMap[key] = value

    return entryMap.values()

  def __mergeEqualEntries(self, group):
    targetEntry = group[0]
    for entry in group:
      if not entry == targetEntry: 
        self.__mergeEntryPair(targetEntry, entry)

    return targetEntry
 
  def __mergeEntryPair(self, lentry, rentry):
    self.__mergeTexts(lentry, rentry)
    self.__mergeChildXpaths(lentry, rentry)

    self.__mergeEntries(lentry.childXpaths)

  def __mergeTexts(self, lentry, rentry):
    lentry.texts.extend(rentry.texts)

  def __mergeChildXpaths(self, lentry, rentry):
    lentry.childXpaths.extend(rentry.childXpaths)

  def displayEntryTree(self):
    self.__display(self.rootEntry, 0)
    
  def __display(self, entry, numOfPadding):
    if not entry:
      return
     
    padding = '*' * numOfPadding
    print(padding + 'xpath:' + entry.xpath)
    print(padding + 'namespace map:' + str(entry.nsMap))
    print(padding + 'texts:' + str(entry.texts))
    print('')    

    for childEntry in entry.childXpaths:
      self.__display(childEntry, numOfPadding + 3)
  

