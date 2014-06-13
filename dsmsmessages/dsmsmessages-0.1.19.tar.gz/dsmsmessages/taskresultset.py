# -*- coding: utf-8 -*-

from .taskresult import TaskResult
from .fields import MsgFields as MSGF


class TaskResultSet(dict):
    """
    JobResult is a dict for storing TaskResults with convenience functions.
    """
    def __init__(self, target_id, job_id):
        self.setdefault(MSGF.TRS_META, {})

        try:
            int(target_id)
        except TypeError:
            raise ValueError("Target id must be a number")

        try:
            int(job_id)
        except TypeError:
            raise ValueError("Job id must be a number")

        self[MSGF.TRS_META][MSGF.TRS_META_TARGET_ID] = target_id
        self[MSGF.TRS_META][MSGF.TRS_META_JOB_ID] = job_id

        dict.__init__(self)

    @property
    def target_id(self):
        try:
            return self[MSGF.TRS_META][MSGF.TRS_META_TARGET_ID]
        except KeyError:
            raise ValueError("Target ID not set!")

    @property
    def job_id(self):
        try:
            return self[MSGF.TRS_META][MSGF.TRS_META_JOB_ID]
        except KeyError:
            raise ValueError("Job ID not set!")

    def add(self, task_result):
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
        self.setdefault(task_name, {MSGF.TASKRESULTS: {}, MSGF.META: {}})

        self[task_name][MSGF.META].setdefault(MSGF.META_ERR, [])

        self[task_name][MSGF.META][MSGF.META_ERR].append(err)

    def task_success(self, task_name):
        return self.task_errs(task_name) == []

    def task_errs(self, task_name):
        try:
            self[task_name][MSGF.META]
        except:
            raise ValueError("%s task not found in message" % task_name)

        return self[task_name][MSGF.META].get(MSGF.META_ERR, [])

    def tasks(self):
        return filter(lambda k: k != MSGF.TRS_META, self.iterkeys())

    def task_tmoids(self, task_name):
        try:
            self[task_name][MSGF.TASKRESULTS]
        except KeyError:
            raise ValueError("%s task not found in message" % task_name)

        return self[task_name][MSGF.TASKRESULTS].keys()

    def get_task_tmoid(self, task_name, tmoid, schema=None):
        """
        Get a single TaskResult based on a task name and target monitoring
        ID.
        """
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
