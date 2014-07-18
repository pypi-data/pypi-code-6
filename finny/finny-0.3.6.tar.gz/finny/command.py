from abc import ABCMeta, abstractmethod

class Command(object):
  __metaclass__ = ABCMeta

  @abstractmethod
  def run(self):
    pass
