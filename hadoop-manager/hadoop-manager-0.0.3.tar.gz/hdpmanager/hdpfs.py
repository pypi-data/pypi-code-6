import datetime
import shlex
from collections import namedtuple

from protocol import get_protocol_from_name


class HadoopFileNotFoundError(IOError):
    pass


_HadoopLsLine = namedtuple('File', ['permissions', 'replicas', 'user', 'group', 'size', 'modified', 'path'])


class HadoopFs(object):

    HadoopFileNotFoundError = HadoopFileNotFoundError

    def __init__(self, hadoop_manager):
        self._hdpm = hadoop_manager

    def cat(self, path, serializer='raw', tab_separated=False):
        """
        Returns a generator over files defined by path

        :param path: path to the files
        :param serializer: input serializer. Options are json, pickle and raw(default)
        :param tab_seperated: boolean if input is tab separated
        """
        job = self._hdpm._run_hadoop_cmd('fs', ('-cat', path))
        output = job.yield_stdout()
        output_serializer = get_protocol_from_name(serializer)

        for line in output:
            line = line.rstrip()

            if tab_separated:
                ls = line.split('\t')
                if len(ls) > 1:
                    yield tuple(output_serializer.decode(part) for part in line.split('\t'))
                else:
                    yield output_serializer.decode(line)
            else:
                yield output_serializer.decode(line)

        job.join()

    def rm(self, path):
        """
        Recursively remove all files on the path

        :param path: path to the files
        """
        job = self._hdpm._run_hadoop_cmd('fs', ('-rm', '-r', path))
        job.print_stdout()
        job.join()

    def _parse_ls_line(self, line):
        split_line = shlex.split(line)
        if len(split_line) != 8:
            return

        modified = datetime.datetime.strptime('%sT%s' % (split_line[5], split_line[6]), '%Y-%m-%dT%H:%M')

        return _HadoopLsLine(
            permissions=split_line[0],
            replicas=int(split_line[1].replace('-', '0')),
            user=split_line[2],
            group=split_line[3],
            size=int(split_line[4]),
            modified=modified,
            path=split_line[7],
        )

    def ls(self, path, recursive=False):
        """
        Lists files on the path

        :param path: path to the file
        :param recursive: list subdirectories recursively
        """

        if recursive:
            cmd = '-lsr'
        else:
            cmd = '-ls'

        try:
            job = self._hdpm._run_hadoop_cmd('fs', (cmd, path))
            for line in job.yield_stdout():
                parsed_line = self._parse_ls_line(line)
                if parsed_line:
                    yield parsed_line
            job.join()
        except self._hdpm.HadoopRunException:
            raise self.HadoopFileNotFoundError("ls: '%s': No such file or directory" % path)

    def exists(self, path):
        """
        Check if file on the path exists

        :param path: path to the file
        """
        try:
            for _ in self.ls(path):
                pass
        except self.HadoopFileNotFoundError:
            return False
        return True
