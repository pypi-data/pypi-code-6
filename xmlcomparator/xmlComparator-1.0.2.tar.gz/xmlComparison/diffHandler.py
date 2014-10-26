#######################  DiffHandler     ##########################

class DiffHandler():
  def setTargetFile(self, targetFile):
    self.__targetFile = targetFile

  def setSourceFile(self, sourceFile):
    self.__sourceFile = sourceFile
 
  def nodeNotAvailable(self, entry):
    print('[**node missing**]:')
    print( entry.xpath)
    print('')

  def textNotMatch(self, entry, diffTexts):
    print('[**text not match for node**]:')
    print(entry.xpath + ';')
    print('different texts: ' + str(diffTexts))
    print('')

