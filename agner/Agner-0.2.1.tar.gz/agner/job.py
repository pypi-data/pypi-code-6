from uuid import uuid4
try:
  import cPickle as pickle
except ImportError:
  import Pickle as pickle

class Job(object):
  def __init__(self, **kwargs):
    self.payload = kwargs
    # TODO: replace with a smart 64bit job id generator that has time and
    # machine info
    if self.payload.get('job_id'):
      self.job_id = self.payload['job_id']
    else:
      self.job_id = uuid4()
      self.payload['job_id'] = self.job_id
    self.__queue_name = None # set when enqueued

  def __repr__(self):
    status = "UNQUEUED"
    if self.__queue_name:
      status = "IN QUEUE: %s" % self.__queue_name
    return u'<agner.Job ID:%s %s>' % (self.job_id, status)

  def queue_name(self):
    return self.__queue_name

  @classmethod
  def from_serialized(self, serialized):
    payload = pickle.loads(serialized)
    return Job(**payload)

  def notify_queued(self, queue):
    """To be called by the queue itself when it inserts this job
    Do not call this yourself
    """
    self.__queue_name = queue.queue_name

  def serialize(self):
    """Returns a suitable string representation of a job
    """
    return pickle.dumps(self.payload)
