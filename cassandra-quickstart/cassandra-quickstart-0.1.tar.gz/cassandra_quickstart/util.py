from six.moves import urllib
from six import print_
import os
import errno

class DownloadError(Exception):
    pass

def download(url, target, show_progress=False):
    u = urllib.request.urlopen(url)
    f = open(target, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    if show_progress:
        print_("Downloading %s to %s (%.3fMB)" % (url, target, float(file_size) / (1024 * 1024)))

    file_size_dl = 0
    block_sz = 8192
    status = None
    attempts = 0
    while file_size_dl < file_size:
        buffer = u.read(block_sz)
        if not buffer:
            attempts = attempts + 1
            if attempts >= 5:
                raise DownloadError("Error downloading file (nothing read after %i attempts, downloded only %i of %i bytes)" % (attempts, file_size_dl, file_size))
            time.sleep(0.5 * attempts)
            continue;
        else:
            attempts = 0

        file_size_dl += len(buffer)
        f.write(buffer)
        if show_progress:
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = chr(8)*(len(status)+1) + status
            print_(status, end='')

    if show_progress:
        print_("")
    f.close()
    u.close()


def makedirs(path):
    """mkdir -p"""
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise


