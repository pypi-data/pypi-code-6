import xml.sax.handler

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

