'''Handles IO operations such as printing to console'''

import colorama
import os
import sys


PY2 = sys.version_info.major == 2
PY3 = sys.version_info.major == 3
DISABLE_COLORS = False
COLORS = {
  "error": colorama.Fore.RED,
  "priority": colorama.Fore.CYAN,
  "reset": colorama.Style.RESET_ALL,
  "success": colorama.Fore.GREEN,
  "warning": colorama.Fore.YELLOW
}


# handling Python 2 & 3 porting issues
if PY2:
  input = raw_input


def disableColors():
  'disables colors using os environment'
  os.environ.update({"STACKQ_DISABLE_COLORS_TEMP": "yes"})


def beVerbose():
  'enable verbose logging of errors'
  os.environ.update({"STACKQ_VERBOSE_TEMP": "yes"})


def getColor(status=""):
  '''returns ansi color codes when colored output is
  enabled.
  @param {str} status - status class / color name
  @return {str} ansi-codes'''
  if os.environ.get("STACKQ_DISABLE_COLORS") or os.environ.get("STACKQ_DISABLE_COLORS_TEMP"):
    return ""
  return COLORS.get(status, "")


def getInput(question, default=""):
  'Simply gets input from user'
  userInput = input(question + "> ") 
  userInput = default if userInput is "" else userInput
  return userInput


def multilineInput(endMark="?"):
  '''gets multiline input across lines
  @param {str} endMark - a line with this stops input
  @return {str}'''
  lines = []
  while 1:
    try:
      line = input("> ")
      lines.append(line)
      if line.find(endMark) is not -1: break
    except KeyboardInterrupt:
      break
    except EOFError:
      exit(1)
  sys.stdout.write("\n")
  return "".join(lines)


def fastWrite(chars):
  '''Writes to sys.stdout and flushes it immediately.This
  ensures the characters are outputted asap
  @param {str} chars - characters/text to write out'''
  sys.stdout.write(chars)
  sys.stdout.flush()


def println(text, status="", append="\n"):
  '''prints `text`to stdout, applying colors for `status`
  and appending `append`
  @param {str} text - text to write out
  @param {str} status - color class
  @param {str} append - characters to append at end of text
  '''
  line = "{0}{1}{2}{3}"
  line = line.format(getColor(status), text, getColor("reset"),append)
  sys.stdout.write(line)


class ProgressPrint():
  '''Class for progress report/print, usually for logging'''
  def __init__(self):
    self.string = "{0}{1}" + getColor("reset") + "\n"

  def ok(self, label="ok"):
    'for successful completion'
    string = self.string.format(getColor("success"), label)
    fastWrite(string)
      
  def error(self, label="error", err=""):
    'for progress hurdled with error(s) that it can not handle'
    string = self.string.format(getColor("error"), label)
    fastWrite(string)
    if err is not "" and (os.environ.get("STACKQ_VERBOSE") or os.environ.get("STACKQ_VERBOSE_TEMP")):
      println(err, status="priority")

  def warning(self, label="warning"):
    'for progress facing an issue that it can handle'
    string = self.string.format(getColor("warning"), label)
    fastWrite(string)


def log(event):
  '''Logs an event to stdout.
  @param {str} event - string to write out
  @return {ProgressPrint} a ProgressPrint instance'''
  statement = "".join([event.capitalize(), "... "])
  fastWrite(statement)
  return ProgressPrint()
