import os
import pwd
import re
import datetime
import uuid
import cPickle as pickle
import threading

from hdpenv import HadoopEnv

ZHDUTILS_PACKAGE = 'hdpmanager'
EGG_NAME = 'zemanta_hadoop_job'
EGG_VERSION = '1.0'

DEFAUT_NUM_REDUCERS = 1

HADOOP_STREAMING_JAR_RE = re.compile(r'^hadoop.*streaming.*\.jar$')

CONF_PICKE_FILE_PATH = 'streamer_conf.pickle'
SERIALIZATION_CONF_PICKE_FILE_PATH = 'serialization_conf.pickle'

DEFAULT_MAPPER = 'hdpmanager.mapper.EmptyMapper'

HDFS_TMP_DIR_PREFIX = '/tmp/hdpmanager'


class HadoopJob(object):
    """
    HadoopJob object for managing mapreduce jobs
    Create it with the HadoopManager.create_job methos
    """

    def __init__(self, hdp_manager,
                    input_paths=None, input_jobs=None, output_path=None, mapper=None, reducer=None,
                    combiner=None, num_reducers=None, serialization=None, conf=None,
                    job_env=None, root_package=None, skip_missing_input_paths=False):

        if not input_jobs and not input_paths:
            raise AttributeError('Both input_jobs and input_paths cannot be None')

        self._hdpm = hdp_manager

        self._root_package = root_package

        self._mapper = mapper
        self._combiner = combiner
        self._reducer = reducer
        self._num_reducers = num_reducers or DEFAUT_NUM_REDUCERS

        self._job_name = self._make_job_name()

        self._output_path = output_path or self._get_hdfs_tmp_dir()
        self._input_paths = input_paths
        self._input_jobs = input_jobs
        self._skip_missing_input_paths = skip_missing_input_paths

        self._serialization_conf = serialization
        self._serialization_conf_file = self._create_conf_file(serialization, SERIALIZATION_CONF_PICKE_FILE_PATH)

        self._conf = conf
        self._conf_file = self._create_conf_file(conf, CONF_PICKE_FILE_PATH)

        self._hadoop_env = HadoopEnv(hdp_manager, root_package=self._root_package, **(job_env or {}))

    def _make_job_name(self):
        now = datetime.datetime.utcnow().strftime('%H-%M-%S')

        user = pwd.getpwuid(os.getuid())[0]
        scripts = '-'.join(set([p.split('.')[0] for p in [self._mapper, self._reducer, self._combiner] if p]))

        random = uuid.uuid4().hex[:5]

        return '.'.join([user, scripts, now, random])

    def _get_hdfs_tmp_dir(self):
        today = datetime.date.today().isoformat()
        return os.path.join(HDFS_TMP_DIR_PREFIX, today, self._job_name)

    def _create_conf_file(self, conf, fp):
        if not conf:
            return

        conf_file = os.path.join(self._hdpm._get_tmp_dir('conf'), fp)
        pickle.dump(conf, open(conf_file, 'w'))
        return conf_file

    def _get_streamer_command(self, module_path, encoded):
        path = module_path.split('.')
        module = '.'.join(path[:-1])
        class_name = path[-1]

        if encoded:
            return 'python -c "from %s import %s; %s()._run()"' % (module, class_name, class_name)
        else:
            return 'python', '-c', 'from %s import %s; %s()._run()' % (module, class_name, class_name)

    def _get_mapper_command(self, encoded=True):
        return self._get_streamer_command(self._mapper or DEFAULT_MAPPER, encoded)

    def _get_reducer_command(self, encoded=True):
        if not self._reducer:
            return
        return self._get_streamer_command(self._reducer, encoded)

    def _get_combiner_command(self, encoded=True):
        if not self._combiner:
            return
        return self._get_streamer_command(self._combiner, encoded)

    def rm_output(self):
        """
        Remove output dir
        """

        try:
            self._hdpm.fs.rm(self._output_path)
        except self._hdpm.HadoopRunException:
            pass

    def cat_output(self):
        """
        Returns a generator over mapreduce output
        """

        from streamer import DEFAULT_OUTPUT_SERIALIZED
        output_serializer = (self._serialization_conf or {}).get('output', DEFAULT_OUTPUT_SERIALIZED)
        return self._hdpm.fs.cat(os.path.join(self._output_path, 'part-*'), serializer=output_serializer, tab_separated=True)

    def get_output_path(self):
        """
        Returns path to the output file. Usefull when temporary dir is used
        """
        return self._output_path

    def _get_all_input_paths(self):
        inputs = []

        if self._input_jobs:
            inputs += [ij.get_output_path() for ij in self._input_jobs]

        if self._input_paths:
            inputs += self._input_paths

        if self._skip_missing_input_paths:
            clean_inputs = [inf for inf in inputs if self._hdpm.fs.exists(inf)]
        else:
            clean_inputs = inputs

        if not clean_inputs:
            raise self._hdpm.HadoopRunException('No input files for job.')

        return clean_inputs

    def _run_dependent_jobs(self):
        if not self._input_jobs:
            return

        promises = []
        for ij in self._input_jobs:
            ij.rm_output()
            promises.append(ij.run_async())

        for promise in promises:
            promise.join()

    def _stdout_print_async(self, promise):
        t = threading.Thread(target=promise.print_stdout)
        t.daemon = True
        t.start()

    def run_async(self):
        """
        Run a mapreduce job in background
        Returns a HadoopCmdPromise object
        """
        self._run_dependent_jobs()

        env_files = self._hadoop_env.env_files

        cmd = ('jar', self._hdpm._hadoop_stream_jar)

        attrs = [
                ('-mapper', self._get_mapper_command()),

                ('-input', self._get_all_input_paths()),
                ('-output', self._output_path),

                ('-cmdenv', 'PYTHONPATH=:%s' % (os.pathsep.join([e[0] for e in env_files]))),
                ('-file', [efile[1] for efile in env_files]),

                ('-reducer', self._get_reducer_command()),
                ('-numReduceTasks', self._num_reducers),

                ('-combiner', self._get_combiner_command()),

                ('-file', self._conf_file),
                ('-file', self._serialization_conf_file),
        ]

        job_promise = self._hdpm._run_hadoop_cmd(cmd, attrs, self._job_name)

        self._stdout_print_async(job_promise)

        return job_promise


    def run(self):
        """
        Run a mapreduce job
        """

        job_promise = self.run_async()
        job_promise.join()
