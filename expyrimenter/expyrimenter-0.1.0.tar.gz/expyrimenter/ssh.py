from expyrimenter import Shell
from time import sleep
import logging
import random


class SSH(Shell):
    """
    :param str params: shell SSH params (at least the hostname).
    :param str remote_cmd: Command to be run in remote host through SSH.
    :param str title: A title to be displayed in log outputs.
                      If None, the shell command will be shown.
    :param bool stdout: Whether or not to display standard output.
                        Default is *False*.
    :param bool stderr: Whether or not to display standard error.
                        Default is *True*.
    """

    def __init__(self, params, remote_cmd, title=None,
                 stdout=False, stderr=True):
        remote_cmd = self._redirect_outputs(remote_cmd, stdout, stderr)
        cmd = "ssh %s '%s'" % (params, remote_cmd)
        super().__init__(cmd, title, stdout, stderr)

    @staticmethod
    def await_availability(params, interval=5, max_rand=1):
        """Periodically tries SSH until it is successful.
        This function is very useful in cloud environmentes, because
        there can be a considerable amount of time after a VM is running
        and before SSH connections are available.

        :param str params: shell SSH params (at least the hostname).
        :param num interval: Time in seconds to wait before new trial.
        :param num max_rand: A float random number between 0 and ``max_rand``
                             will be added to ``interval``.
        """
        ssh = SSH(params, 'exit')
        log = logging.getLogger('ssh')
        while ssh.has_failed():
            sleep(random.uniform(0, max_rand))
            log.debug('Trying "ssh %s" again in %d + [0, %.2f) sec' %
                      (params, interval, max_rand))
            sleep(interval)
