import git.config
import ConfigParser
from util import walkUp
import os.path

class BranchHealthConfig:
  def __init__(self, repo):
    self.mParser = git.config.SectionConstraint(repo.config_reader(), 'branchhealth')

  def shouldIgnoreBranches(self):
    try:
      ignoreBranches = not self.mParser.get_value(option='noignore')
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
      return True
    return ignoreBranches

  def shouldUseColor(self):
    try:
      color = not self.mParser.get_value(option='nocolor')
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
      return True
    return color
