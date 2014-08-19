import os

class TaskCount:
    """ Counts the number of tasks running on this machine """

    def getVariableTuple(self):

        pids = [p for p in os.listdir('/proc') if p.isdigit()]

        return [('TASK_COUNT', len(pids))]