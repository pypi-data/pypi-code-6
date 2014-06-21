# -*- coding: utf-8 -*-

from .taskresult import TaskResult
from .fields import MsgFields as MSGF


class TaskResultSet(dict):
    """
    JobResult is a dict for storing TaskResults with convenience functions.
    """
    def __init__(self, target_id, job_id, data=None):
        self.setdefault(MSGF.TRS_META, {})

        # target_id and job_id are stored internally as strs, since this
        # is how they get json encoded. To API user, they're converted to
        # ints when using .target_id, .job_id, get_task_tmoid() etc.
        try:
            target_id = str(int(target_id))
        except TypeError:
            raise ValueError("Target id must be a number")

        try:
            job_id = str(int(job_id))
        except TypeError:
            raise ValueError("Job id must be a number")

        self[MSGF.TRS_META][MSGF.TRS_META_TARGET_ID] = target_id
        self[MSGF.TRS_META][MSGF.TRS_META_JOB_ID] = job_id

        dict.__init__(self)

        if data and not isinstance(data, dict):
            raise ValueError("data must be a dictionary to import")
        elif data:
            self.update(data)

    @classmethod
    def init_from_dict(cls, data):
        """
        Init a TaskResult set from a a (likely JSON deserialized) dict.
        """
        target_id = data[MSGF.TRS_META][MSGF.TRS_META_TARGET_ID]
        job_id = data[MSGF.TRS_META][MSGF.TRS_META_JOB_ID]

        return cls(target_id, job_id, data=data)

    @property
    def target_id(self):
        """
        Return an int representing target_id of Job.
        """
        try:
            return int(self[MSGF.TRS_META][MSGF.TRS_META_TARGET_ID])
        except KeyError:
            raise ValueError("Target ID not set!")
        except TypeError:
            raise ValueError("Target ID muse be an int")

    @property
    def job_id(self):
        """
        Return an int representing job_id of Job.
        """
        try:
            return int(self[MSGF.TRS_META][MSGF.TRS_META_JOB_ID])
        except KeyError:
            raise ValueError("Job ID not set!")
        except TypeError:
            raise ValueError("Job ID must be an int")

    def add(self, task_result):
        """
        Add a TaskResult to this TaskResultSet.
        """
        if not task_result.task_name:
            raise ValueError("TaskResult must specify a task")
        if not task_result.tmoid:
            raise ValueError("TaskResult must specify a target monitoring "
                             "object id")

        self.setdefault(task_result.task_name, {
            MSGF.TASKRESULTS: {},
            MSGF.META: {}}
        )
        self[task_result.task_name][MSGF.TASKRESULTS][task_result.tmoid] = \
            dict(task_result)

    def add_task_err(self, task_name, err):
        """
        Add an error indicating that there was a TaskResult-level error
        preventing Task from being run (e.g. insufficient inputs)
        Use TaskResult.err when this problem relates to a particular tmoid,
        and TaskResultSet.add_task_err() when none of the tmoids could be
        tested.
        """
        self.setdefault(task_name, {MSGF.TASKRESULTS: {}, MSGF.META: {}})

        self[task_name][MSGF.META].setdefault(MSGF.META_ERR, [])

        self[task_name][MSGF.META][MSGF.META_ERR].append(err)

    def task_success(self, task_name):
        """
        Return a bool indicating if a TaskResult ran without high-level
        errors i.e. testing was attempted for tmoids.
        """
        return self.task_errs(task_name) == []

    def task_errs(self, task_name):
        """
        Return list of errors returned by task.
        """
        try:
            self[task_name][MSGF.META]
        except:
            raise ValueError("%s task not found in message" % task_name)

        return self[task_name][MSGF.META].get(MSGF.META_ERR, [])

    def tasks(self):
        """
        Return a list of Task result names contained in a message.
        """
        return filter(lambda k: k != MSGF.TRS_META, self.iterkeys())

    def task_tmoids(self, task_name):
        """
        Return a list of tmoid ints related to a Task result name.
        """
        try:
            self[task_name][MSGF.TASKRESULTS]
        except KeyError:
            raise ValueError("%s task not found in message" % task_name)

        # keys here are json encoded as strs, recast to int
        return [int(k) for k in self[task_name][MSGF.TASKRESULTS].keys()]

    def get_task_tmoid(self, task_name, tmoid, schema=None):
        """
        Get a single TaskResult based on a task name and target monitoring
        ID.
        """
        try:
            tmoid = str(int(tmoid))
        except TypeError:
            raise ValueError("Tmoid must be an int")

        try:
            self[task_name][MSGF.TASKRESULTS][tmoid]
        except KeyError:
            raise ValueError("Could not find task {0} with tmoid {1} in "
                             "results".format(task_name, tmoid))

        tr = TaskResult.init_from_dict(
            task_name,
            tmoid,
            self[task_name][MSGF.TASKRESULTS][tmoid],
            schema=schema
        )
        return tr
