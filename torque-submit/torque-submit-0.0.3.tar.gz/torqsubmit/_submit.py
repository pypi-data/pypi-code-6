# -*- coding: utf-8 -*-

import os
import sys
from subprocess import Popen, STDOUT, PIPE, CalledProcessError
from time import sleep

from torqsubmit.store import FileBasedStore, StoreProperty, Mode


try:
    import dill as pickle
except ImportError:
    import pickle
import base64

ROOT_DIR = os.path.dirname(__file__)
EXECUTOR = os.path.join(ROOT_DIR, 'torque_wrapper.py')


class Submitter(object):
    def __init__(self):
        super(Submitter, self).__init__()
        self.StoreClass = FileBasedStore
        self.tasks = []
        self.store = {}
        self.enviorment = "true"
        self.dirname = ROOT_DIR
        self.qsub_args = tuple()
        self.processes = None
        self.memory_gb = None
        self.queue = "i3d"
        self.use_pbs_array = False
        self.array_tasks_to_run_in_paralel = None

    def guess_virtualenv(self):
        """
        Sets enviorment in such way that current virtual enviorment is used
        :return:
        """
        import sys
        py_dir = os.path.dirname(sys.executable)
        activate = os.path.join(py_dir, 'activate')
        if not os.path.exists(activate):
            raise ValueError("Couldn't guess virtualenv")
        self.enviorment = """
            source {}
        """.format(activate)


    @property
    def __launch_array_task(self):
        return self.use_pbs_array and len(self.tasks) > 1

    def __update_qsub_ags(self):
        result = []
        if self.processes is not None:
            result.extend(["-l", "nodes=1:ppn={}".format(self.processes)])
        if self.memory_gb is not None:
            result.extend(["-l", "mem={}GB".format(self.memory_gb)])
        if self.queue is not None:
            result.extend(["-q", self.queue])
        return result

    def __update_tasks(self):
        if len(self.tasks) == 1:
            self.store[StoreProperty.MODE] = Mode.SINGLE_TASK
            self.store[StoreProperty.TASK] = self.StoreClass.pickle_task(self.tasks[0])
        else:
            if self.use_pbs_array is False:
                self.store[StoreProperty.MODE] = Mode.MANY_TASKS
            else:
                self.store[StoreProperty.MODE] = Mode.PBS_ARRAY
            self.store[StoreProperty.TASK_COUNT] = len(self.tasks)
            for ii, task in enumerate(self.tasks):
                self.store[StoreProperty.TASK_NO(ii)] = self.StoreClass.pickle_task(task)

    def __update_environ(self):
        return {
            "__PY_T_SUBMIT_ENV": self.enviorment,
            "__PY_T_SUBMIT_DIRNAME": self.dirname
        }

    def __format_pbs_array_argument(self):
        array_spec = "{}-{}".format(0, len(self.tasks) - 1)
        if self.array_tasks_to_run_in_paralel is not None:
            array_spec += '%{}'.format(self.array_tasks_to_run_in_paralel)
        return [
            '-t',
            array_spec
        ]


    def __submit(self, call, env):
        output_chunks = []
        process = Popen(call, env=env, stderr=STDOUT, stdout=PIPE)
        while process.returncode is None:
            output_chunks.append(process.communicate())
            sleep(0.1)
        stdout = "".join([c[0].decode('utf-8') for c in output_chunks if c[0] is not None])
        stderr = "".join([c[1].decode('utf-8') for c in output_chunks if c[1] is not None])

        if process.returncode == 0:
            return stdout, stderr

        exc = CalledProcessError(process.returncode, call)
        exc.stdout = stdout
        exc.stderr = stderr

        print(stdout)
        print(stderr)

        raise exc


    def submit(self):
        self.__update_tasks()
        env = dict(os.environ)
        env.update(self.__update_environ())
        env.update(self.StoreClass.save_store(self.store))
        call = ['qsub']
        call.append('-V')
        if self.__launch_array_task:
            call.extend(self.__format_pbs_array_argument())
        call.extend(self.qsub_args)
        call.extend(self.__update_qsub_ags())
        call.append(EXECUTOR)

        return self.__submit(call, env=env)
