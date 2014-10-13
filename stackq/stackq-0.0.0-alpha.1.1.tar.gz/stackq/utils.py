import io
# handle python 2 and 3 module import diffs
import urllib

def saveToFile(filepath):
  '''Returns a function that can be called with
  text that is going to be written to the file
  pointed by `filepath`
  @param {str} filepath
  @return {def} a function'''
  def write(string):
    words = "saving to file '{0}'".format(filepath)
    writeProgress = io.log(words)
    try:
      with open(filepath, "a") as saveFile:
        saveFile.write(string)
        writeProgress.ok()
    except Exception as e:
      writeProgress.error(err=e)
  return write


def ping():
  '''Pings google.com. Returns True if its a hist.
  Otherwise return an Error object
  @return {bool or Error}- True for success. Error for
  failure'''
  networkConn = io.log("Checking network connectivity")
  try:
    urllib.urlopen("http://google.com")
    networkConn.ok()
    return True
  except Exception as e:
    networkConn.error(err=e)
    return e
