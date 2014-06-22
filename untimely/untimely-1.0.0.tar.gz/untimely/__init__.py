
from time       import time


class IllegalOperationError(StandardError):
  pass


class TimeMeasurement(object):
  def __init__(self, purpose = None):
    self.purpose    = purpose
    self.start_time = None
    self.stop_time  = None

  @property
  def has_started(self):
    return self.start_time is not None

  def start(self):
    if self.has_started:
      raise IllegalOperationError("TimeMeasurement has already been started")
    else:
      self.start_time = time()


  @property
  def has_stopped(self):
    return self.stop_time is not None

  def stop(self):
    if self.has_stopped:
      raise IllegalOperationError("TimeMeasurement has already been stopped")
    else:
      self.stop_time = time()

  @property
  def has_completed(self):
    return self.has_started and self.has_stopped

  @property
  def length(self):
    if self.has_completed:
      return self.stop_time - self.start_time
    else:
      return IllegalOperationError("TimeMeasurement.length cannot be measured in the current state")



  def __enter__(self):
    self.start()
    return self

  def __exit__(self, type, value, tb):
    self.stop()


