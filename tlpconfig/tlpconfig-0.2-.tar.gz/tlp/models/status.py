from subprocess import Popen, PIPE


def get_status(command):
    p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    out, error = p.communicate()

    if error:
        return error.decode('UTF-8')

    return out.decode('UTF-8')
