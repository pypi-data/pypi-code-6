import os
import platform

UBUNTU_UPSTART_JOB_FILE = \
"""# {tty} - getty
#
# This service maintains a getty on {tty} from the point the system is
# started until it is shut down again.

start on stopped rc RUNLEVEL=[2345]
stop on runlevel [!2345]

respawn
exec /sbin/getty -8 38400 -n -i -l {path} {tty}
"""


def install(tty_dev, greeter_path):
    dist, version, nick = platform.dist()
    if dist == 'Ubuntu':
        major, minor = (int(i) for i in version.split('.'))
        if major >= 10:
            install_on_ubuntu(tty_dev, greeter_path)
            return
    raise NotImplementedError("{} {} not supported".format(dist, version))


def move_to_backup(path):
    backup_path = path + ".before_greeter"
    if not os.path.exists(backup_path):
        os.rename(path, backup_path)


def install_on_ubuntu(tty_dev, greeter_path):
    template = UBUNTU_UPSTART_JOB_FILE.format(tty=tty_dev, path=greeter_path)
    job_path = "/etc/init/{tty_dev}.conf".format(tty_dev=tty_dev)
    move_to_backup(job_path)
    with open(job_path, "w") as f:
        f.write(template)
