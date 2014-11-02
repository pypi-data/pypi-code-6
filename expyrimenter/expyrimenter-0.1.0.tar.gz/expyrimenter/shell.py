import logging
import subprocess
from subprocess import CalledProcessError
from .runnable import Runnable


class Shell(Runnable):
    """
    :param str cmd: Command with arguments to be run.
    :param str title: A title to be displayed in log outputs.
                      If None, :attr:`cmd` will be shown.
    :param bool stdout: Whether or not to display standard output.
                        Default is *False*.
    :param bool stderr: Whether or not to display standard error.
                        Default is *True*.
    """

    def __init__(self, cmd, title=None, stdout=False, stderr=True):
        self._cmd = self._redirect_outputs(cmd, stdout, stderr)
        self._title, self._stdout, self._stderr = title, stdout, stderr

    def _redirect_outputs(self, cmd, stdout, stderr):
        """
        Avoid transfering unnecessary output through the network.
        If local, keeps the output clean.
        """
        suffix = ''
        if not stdout:
            suffix += ' 1>/dev/null'
        if not stderr:
            suffix += ' 2>/dev/null'

        return cmd + suffix

    @property
    def command(self):
        """
        The command to be run in shell.

        :rtype: str
        """
        return self._cmd

    @property
    def title(self):
        """
        If the title is not set, returns :func:`command`.

        :rtype: str
        """
        if self._title is None:
            return self._cmd
        return self._title

    def run_pre(self):
        logger = logging.getLogger('shell')
        logger.debug('beginning:' + self.title)

    def run(self):
        """If the command exits 0, returns 0 or the stdout/stderr output.
        Otherwise, raises CalledProcessError.

        :return: shell return code (0) or output.
        :rtype: int or str
        :raises CalledProcessError: if return code is not 0.
        """
        self.run_pre()

        kwargs = {'shell': True, 'universal_newlines': True}
        if self._stderr:
            kwargs['stderr'] = subprocess.STDOUT

        if not (self._stdout or self._stderr):
            output = subprocess.check_call(self._cmd, **kwargs)
        else:
            output = subprocess.check_output(self._cmd, **kwargs).strip()

        self.run_pos()
        return output

    def was_successful(self):
        """Runs the command and returns whether the return code is 0.

        :return: whether the command was successful.
        :rtype: bool
        """
        try:
            self.run()
            return True
        except CalledProcessError:
            return False

    def has_failed(self):
        """Runs the command and returns whether the return code differs from 0.

        :return: whether the command has failed.
        :rtype: bool
        """
        return not self.was_successful()

    def run_pos(self):
        logger = logging.getLogger('shell')
        logger.debug('finished:' + self.title)
