import subprocess as sp

def play(filename):
    mplayer = sp.Popen(['mplayer', filename],
                    stdout = sp.PIPE, stderr = sp.PIPE)
    mplayer.wait()
    stdout, stderr = mplayer.communicate()
    lines = stdout.decode('utf-8').split('\r')
    try:
        return lines[-2]
    except IndexError:
        return None
