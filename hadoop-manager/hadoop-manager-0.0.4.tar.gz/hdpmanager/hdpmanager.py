import os
import re
import shutil
import subprocess
import uuid

from hdpjob import HadoopJob
from hdpfs import HadoopFs

HADOOP_STREAMING_JAR_RE = re.compile(r'^hadoop.*streaming.*\.jar$')

# temporary dir are created in HDP_TMP_DIR
HDP_TMP_DIR = "/tmp/hadoop-manager"
# each temporary dir gets a randomly generated uuid suffix
# example: /tmp/hadoop-manager/job-02e0d565-5924-419b-ae61-4ce3b56fd28b
HDP_DIR_PREFIX = "job"


class HadoopRunException(Exception):

    def __init__(self, msg, stderr=None):
        super(HadoopRunException, self).__init__(msg)
        self.stderr = stderr

    def __str__(self):
        err = super(HadoopRunException, self).__str__()
        if self.stderr:
            err += '\n' + self.stderr.read()
        return err


class HadoopCmdPromise(object):

    def __init__(self, subprocess):
        self._subprocess = subprocess

    def join(self):
        """
        Block until command/job is completed
        """
        self._subprocess.wait()
        if self._subprocess.returncode != 0:
            raise HadoopRunException('Running hadoop command failed with code %s!' % self._subprocess.returncode, stderr=self._subprocess.stderr)

    def yield_stdout(self):
        """
        Yield command's stdout
        """
        while True:
            o = self._subprocess.stdout.readline()
            if not o:
                break
            yield o

    def print_stdout(self):
        """
        Print command's stdout
        """
        for l in self.yield_stdout():
            print l,


class HadoopManager(object):
    """
    HadoopManager is a central object for managing hadoop jobs and hdfs

    In order to perform proper temporary directory cleanup use HadoopManager with 'with' statement.
    with HadoopManager(...) as manager:
            pass

    :param hadoop_home: home folder of hadoop package
    :param hadoop_fs_default_name: default hdfs home used when paths provided are relative
    :param hadoop_job_tracker: hadoop job tracker host:port
    """

    HadoopRunException = HadoopRunException

    def __init__(self, hadoop_home, hadoop_fs_default_name=None, hadoop_job_tracker=None):

        self._tmp_dir_path = self._make_tmp_dir_path()

        self._hadoop_home = hadoop_home
        self._hadoop_fs_default_name = hadoop_fs_default_name
        self._hadoop_job_tracker = hadoop_job_tracker

        self._hadoop_bin = self._find_hadoop_bin()
        self._hadoop_stream_jar = self._find_streaming_jar()

        self._fs = HadoopFs(self)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._rm_tmp_dir()

    @property
    def fs(self):
        """
        HadoopFs object for managing hdfs
        """
        return self._fs

    def create_job(self, **kwargs):
        """
        Create HadoopJob object

        :param input_paths: list of input files for mapper
        :param input_jobs: list of jobs that will be run when this job is run
                their output will be used as input for this job
        :param output_path: path to the output dir, if not provided, tmp dir will be used
        :param mapper: import path to the mapper class
        :param reducer: import path to the reducer class
        :param combiner: import path to the combiner class
        :param root_package: import path to the subpackage in you app where the mapper/reducer/combiner import starts
        :param num_reducers: number of reducers
        :param conf: object that will be send to mapper, reducer and combiner
                it will be accessible as self.conf in job objects.
        :param serialization: dict with configuration for input, output and internal serialization
                valid keys are input, output and inter, valid values are json, pickle and raw
        :param job_env: dict which defines environment
                valid options are packages, package_data and requires
                if packages aren't provided all packages returned by setuptools.find_packages in root_package will be included
        :param skip_missing_input_paths: skip input paths with no matching files
        """
        return HadoopJob(self, **kwargs)

    def _find_hadoop_bin(self):
        return '%s/bin/hadoop' % self._hadoop_home

    def _find_streaming_jar(self):
        paths = [os.path.join(self._hadoop_home, 'lib', 'hadoop-0.20-mapreduce', 'contrib'), # Try 4.0 path first
                self._hadoop_home]

        for path in paths:
            for (dirpath, _, filenames) in os.walk(path):
                for filename in filenames:
                    if HADOOP_STREAMING_JAR_RE.match(filename):
                        return os.path.join(dirpath, filename)
        return None

    def _get_cmd_list(self, t):
        if not t:
            return []

        cmd = None
        if isinstance(t, (tuple, list)):
            if len(t) > 1 and t[-1] is None:
                # Skip command if attr is None
                return []
            cmd = list(t)
        else:
            cmd = [t]

        if len(cmd) == 2 and isinstance(cmd[1], list):
            exploded = []
            for attr in cmd[1]:
                exploded += [cmd[0], attr]
            cmd = exploded

        return [str(c) for c in cmd]

    def _run_hadoop_cmd(self, command, attrs, job_name=None):
        cmd = [self._hadoop_bin]

        cmd += self._get_cmd_list(command)

        if self._hadoop_fs_default_name:
            cmd += ['-D', 'fs.defaultFS=%s' % self._hadoop_fs_default_name,]
        if self._hadoop_job_tracker:
            cmd += ['-D', 'mapred.job.tracker=%s' % self._hadoop_job_tracker,]
        if job_name:
            cmd += ['-D', 'mapred.job.name=%s' % job_name]

        if not isinstance(attrs, list):
            attrs = [attrs]
        for attr in attrs:
            cmd += self._get_cmd_list(attr)

        hdp_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return HadoopCmdPromise(hdp_process)

    def _make_tmp_dir_path(self):
        tmp_directory = '%s_%s/' % (HDP_DIR_PREFIX, uuid.uuid4().hex)
        return os.path.join(HDP_TMP_DIR, tmp_directory)

    def _get_tmp_dir(self, subdir=None):
        path = self._tmp_dir_path
        if subdir:
            path = os.path.join(path, subdir)
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def _rm_tmp_dir(self):
        if os.path.exists(self._tmp_dir_path):
            shutil.rmtree(self._tmp_dir_path, ignore_errors=True)
