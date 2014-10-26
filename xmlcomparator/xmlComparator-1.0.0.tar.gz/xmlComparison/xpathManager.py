#######################  XpathManager     ##########################
class XpathManager():
  def __init__(self, nsManager):
    self.__nsManager = nsManager
    self.__xpath = ''

  def elementStart(self, name, attributes):
    self.__appendQualifiedName(name)
    self.__appendAttributes(attributes)

  def __appendQualifiedName(self, name):
    self.__xpath += '/' + self.__getQualifiedName(name)

  def __getQualifiedName(self, name):
    qualifiedName = name
    defaultNsPrefix = self.__nsManager.getDefaultNsPrefix()
    if not ':' in name and defaultNsPrefix:
      qualifiedName = defaultNsPrefix + ':' + name
    
    return qualifiedName

  def onText(self, data): pass

  def __appendAttributes(self, attributes):
    # http://www.xmlplease.com/attributexmlns
    # An attribute without a prefix is never in a namespace. 
    # This has implications when we want to navigate XML with code. 
    # If the elements are in a namespace we must declare it also in the code.
    # But in the code we must not declare namespaces for the attributes unless they actually are in a namespace.

    # An attribute is only in a namespace if it has a proper prefix declared as an alias for an XML namespace.
    attrKeys = sorted(attributes.keys())
    attributesList =  ["[@" + key + "='" + attributes[key] + "']" for key in attrKeys if not key.startswith('xmlns')]
    attributesXpath = ''.join(attributesList)

    self.__xpath += attributesXpath

  def elementEnd(self, name):
    ind = self.__xpath.rindex('/' + self.__getQualifiedName(name))
    self.__xpath = self.__xpath[0:ind]

  def getNsMap(self):
    return self.__nsManager.getNsMap()

  def getXpath(self):
    return self.__xpath

  def getTagFromXpath(self, xpath):
    beginInd = xpath.rindex('/')
    endInd = xpath.find('[@', beginInd)

    if endInd == -1:
      lastPart = xpath[beginInd + 1 : ]
    else:
      lastPart = xpath[beginInd + 1 : endInd]

    nsIndex = lastPart.find(':')

    if nsIndex == -1:
      return lastPart
    else:
      return lastPart[nsIndex + 1 : ]

  def getAttributesFromXpath(self, xpath):
    attributesMap = {}
    for attrPiece in self.__getAttrPieces(xpath):
      key, value = self.__extractAttr(attrPiece)
      attributesMap[key] = value
    return attributesMap

  def __extractAttr(self, attrPiece):
    keyBeginIndex = attrPiece.index('[@') + 2;
    keyEndIndex = attrPiece.index('=', keyBeginIndex)

    valueBeginIndex = attrPiece.index("'", keyEndIndex) + 1
    valueEndIndex = attrPiece.index("'", valueBeginIndex) 
    
    key = attrPiece[keyBeginIndex : keyEndIndex].strip()
    value = attrPiece[valueBeginIndex : valueEndIndex]

    return (key, value)

  def __getAttrPieces(self, xpath):
    beginIndex = xpath.find('[@', xpath.rindex('/'))

    while not beginIndex == -1:
      endIndex = xpath.index(']', beginIndex) + 1
      yield xpath[beginIndex : endIndex]
      beginIndex = xpath.find('[@', endIndex)


