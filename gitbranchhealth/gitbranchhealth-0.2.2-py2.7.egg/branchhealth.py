# Git Branch-Health Tool
#
# A tool for showing, with colors, the health of branches, both locally and
# on remotes, of a specified git repository. The health of a branch is
# computed using the time since last activity was recorded on the branch. This
# can be specified on the command line.
#
# Inspired by Felipe Kiss' "Show Last Activity On Branch" script, available at:
# https://coderwall.com/p/g-1n9w
#

from nicelog.formatters import ColorLineFormatter
import logging
import sys
import os

from git import *

import argparse
import sys
from datetime import *
import dateutil.parser
from colors import red, yellow, green

from config import BranchHealthConfig
from util import hasGitDir
from util import isGitRepo
from util import isoDateComparator
from manager import BranchManager

# Use to turn on debugging output
DEBUG = False

# Use to turn on verbose output
VERBOSE = False

# Whether or not color formatting should be turned on
COLOR = True

# Constants specifying branch health
HEALTHY = 0
AGED = 1
OLD = 2

gLog = None
gParser = None

class BranchHealthOptions:
  """
  Composition of all possible options for a given run of git branchhealth.
  """

  def __init__(self, aRepoPath, aRemoteName, aNumDays, aBadOnly, aNoColor, aDeleteOldBranches, aIgnoredBranches=['master', 'HEAD'], aLog=None):
    """
    Initialize a new BranchHealthOptions object with parameters that were given
    from the command line.
    """
    self.mRepoPath = aRepoPath
    self.mRemoteName = aRemoteName
    self.mNumDays = aNumDays
    self.mBadOnly = aBadOnly
    self.mNoColor = aNoColor
    self.mRepo = Repo(self.mRepoPath)
    self.mLog = aLog
    self.mDeleteOldBranches = aDeleteOldBranches
    self.__mIgnoredBranches = aIgnoredBranches
    self.__setupConfigOptions()

  def shouldDeleteOldBranches(self):
    return self.mDeleteOldBranches

  def getIgnoredBranches(self):
    return self.__mIgnoredBranches

  def getRepo(self):
    return self.mRepo

  def getRepoPath(self):
    return self.mRepoPath

  def getRemoteName(self):
    return self.mRemoteName

  def getHealthyDays(self):
    return int(self.mNumDays)

  def getBadOnly(self):
    return self.mBadOnly

  def shouldHaveColor(self):
    return not self.mNoColor

  def getLog(self):
    return self.mLog

  def setLog(self, aLog):
    self.mLog = aLog

  def __setupConfigOptions(self):
    log = self.getLog()
    config = BranchHealthConfig(self.getRepo())

    self.mNoColor = not config.shouldUseColor() or self.mNoColor

    if not config.shouldIgnoreBranches():
      self.__mIgnoredBranches = []


def showBranchHealth(aOptions):
  global gLog
  branchMap = []

  log = gLog

  remoteName = aOptions.getRemoteName()
  repoPath = aOptions.getRepoPath()

  if log:
    log.debug('Operating on repository in: ' + repoPath)
    log.debug('Operating on remote named: ' + str(remoteName))


  repo = aOptions.getRepo()

  if remoteName:
    manager = BranchManager(aOptions)
    branchMap = manager.getBranchMapFromRemote(remoteName)

  sortedBranches = sortBranchesByHealth(branchMap, aOptions.getHealthyDays())
  printBranchHealthChart(sortedBranches, aOptions)


# Sort a list of branch tuples by the date the last activity occurred on them.
#
# @param aBranchList A list of tuples, with each tuple having the following:
#        1) The branch name and 2) A date tuple, with each tuple continaing the
#        following: 2a) A human-readable date (e.g. '2 days ago'), and 2b) an
#        iso-standardized date for comparison with other dates. Note that 2a and
#        2b should be equivalent, with 2a being less accurate, but more easily
#        interpretable by humans.
# @param aHealthyDays The number of days that a branch can be untouched and
#        still be considered 'healthy'.
#
# @returns A list of tuples, with each tuple having the following:
#        1) The branch name and 2) A date tuple, with each tuple continaing the
#        following: 2a) A human-readable date (e.g. '2 days ago'), and 2b) an
#        iso-standardized date for comparison with other dates. Note that 2a and
#        2b should be equivalent, with 2a being less accurate, but more easily
#        interpretable by humans. This list is guaranteed to be sorted in non-
#        ascending order, by the iso-standardized date (#2b, above).

def sortBranchesByHealth(aBranchMap, aHealthyDays):
  global gLog

  sortedBranchMap = sorted(aBranchMap, cmp=isoDateComparator)

  return markBranchHealth(sortedBranchMap, aHealthyDays)

# Traverse a list of branch tuples and mark their healthy status.
#
# @param aBranchList A list of tuples, with each tuple having the following:
#        1) The branch name and 2) A date tuple, with each tuple continaing the
#        following: 2a) A human-readable date (e.g. '2 days ago'), and 2b) an
#        iso-standardized date for comparison with other dates. Note that 2a and
#        2b should be equivalent, with 2a being less accurate, but more easily
#        interpretable by humans.
# @param aHealthyDays The number of days that a branch can be untouched and
#        still be considered 'healthy'.
#
# @returns A list of simplified tuples, each containing: 1) the branch name,
#          2) the human-readable date since last activity on the branch (#2a
#          above), and 3) a constant indicating the health status of the branch

def markBranchHealth(aBranchList, aHealthyDays):
  finalBranchList = []
  # Compute our time delta from when a branch is no longer considered
  # absolutely healthy, and when one should be pruned.
  for branchTuple in aBranchList:
    (branchName, dateTuple) = branchTuple
    (humanDate, isoDate) = dateTuple
    branchdate = dateutil.parser.parse(isoDate)
    branchLife = date.today() - branchdate.date()
    if branchLife > timedelta(aHealthyDays * 2):
      branchHealth = OLD
    elif branchLife > timedelta(aHealthyDays):
      branchHealth = AGED
    else:
      branchHealth = HEALTHY

    finalBranchList.append((branchName, humanDate, branchHealth))

  return finalBranchList

# Print out a 'health chart' of different branches, and when they were last
# changed. The health chart will color the given branches such that:
#     - Branches with last activity longer than double the number of 'healthy
#       days' ago will be colored in RED.
#     - Branches with last activity longer than the number of 'healthy days'
#       ago will be colored in YELLOW.
#     - All other branches will be colored in GREEN
#
# @param aBranchMap A list of tuples where each tuple contains 1) the name
#        of a branch, 2) the last activity (in human readable format), and 3)
#        the constant indicating the health of this branch, computed from
#        the original, iso-standardized date.
# @param aOptions Display options specified on the command line.

def printBranchHealthChart(aBranchMap, aOptions):
  global gLog
  badOnly = aOptions.getBadOnly()
  noColor = not aOptions.shouldHaveColor()

  log = gLog

  deleteBucket = []
  for branchTuple in aBranchMap:
    (branchName, lastActivityRel, branchHealth) = branchTuple

    # If this is an unhealthy branch, then let's put it in the "delete"
    # bucket.
    if branchHealth == OLD:
      deleteBucket.append(branchTuple)

    # Skip healthy and aged branches if we're only looking for bad ones
    if badOnly and not branchHealth == OLD:
      continue

    if not noColor:
      if branchHealth == HEALTHY:
        coloredDate = green(lastActivityRel)
      elif branchHealth == AGED:
        coloredDate = yellow(lastActivityRel)
      else:
        coloredDate = red(lastActivityRel)
    else:
        coloredDate = lastActivityRel

    alignedPrintout = '{0:40} {1}'.format(branchName + ":", coloredDate)
    print(alignedPrintout)

  if aOptions.shouldDeleteOldBranches():
    manager = BranchManager(aOptions)
    manager.deleteAllOldBranches(deleteBucket)

def splitBranchName(aBranchName):
  return aBranchName.split('/')

# Construct an argparse parser for use with this program to parse command
# line arguments.
#
# @returns An argparse parser object which can be used to parse command line
#          arguments, specific to git-branchhealth.

def createParser():
  parser = argparse.ArgumentParser(description='''
     Show health (time since creation) of git branches, in order.
  ''', add_help=True)
  parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
                      help='Output as much as possible')
  parser.add_argument('-r', '--remote', metavar=('<remote name>'), action='store',
                      help='Operate on specified remote', default=None,
                      dest='remote')
  parser.add_argument('-b', '--bad-only', action='store_true',
                      help='Only show branches that are ready for pruning (i.e. older than numDays * 2)',
                      dest='badOnly')
  parser.add_argument('-d', '--days', action='store', dest='numDays',
                      help='Specify number of days old where a branch is considered to no longer be \'healthy\'',
                      default=14)
  parser.add_argument('-n', '--nocolor', action='store_true', help="Don't use ANSI colors to display branch health",
                      dest='noColor')
  parser.add_argument('-R', '--repository', action='store',  metavar=('repository'), help='Path to git repository where branches should be listed', nargs='?', default='.', dest='repo')
  parser.add_argument('-D', '--delete', action='store_true', help='Delete old branches that are considered "unhealthy"', dest='deleteOld')
  parser.add_argument('--no-ignore', action='store_true', help='Do not ignore any branches (by default, "master" and "HEAD" from a given remote are ignored)', dest='noIgnore')

  return parser

# Parse arguments given on the command line. Uses the argparse package to
# perform this task.
def parseArguments():
  global gParser, gLog, VERBOSE, DEBUG

  if not gParser:
    gParser = createParser()

    parsed = gParser.parse_args(sys.argv[1:])

  if parsed.verbose:
    VERBOSE=True
    DEBUG=True

  # Retrieve the git repository, if one wasn't given on the command line
  repo = parsed.repo

  ignoredBranches = ['HEAD', 'master']
  if parsed.noIgnore:
    ignoredBranches = []
  return BranchHealthOptions(repo, parsed.remote, parsed.numDays, parsed.badOnly, parsed.noColor, parsed.deleteOld, ignoredBranches)

def setupLog(aOptions):
  global gLog, DEBUG

  gLog = logging.getLogger("git-branchhealth")
  handler = logging.StreamHandler(sys.stderr)
  handler.setFormatter(ColorLineFormatter())
  if DEBUG:
    gLog.setLevel(logging.DEBUG)
    handler.setLevel(logging.DEBUG)
  else:
    gLog.setLevel(logging.ERROR)
    handler.setLevel(logging.ERROR)

  gLog.addHandler(handler)

  aOptions.setLog(gLog)

# Main entry point
def runMain():
  global gParser, gLog, DEBUG, VERBOSE

  options = parseArguments()
  setupLog(options)

  if options.getRepoPath() == None:
    gParser.print_help()
    return

  showBranchHealth(options)

if __name__ == '__main__':
  runMain()
