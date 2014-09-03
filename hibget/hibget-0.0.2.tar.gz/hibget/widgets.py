__author__ = "Joel Pedraza"
__copyright__ = "Copyright 2014, Joel Pedraza"
__license__ = "MIT"

from progressbar import Widget, ProgressBar, Percentage, Bar, FileTransferSpeed
import datetime

UNITS = (
    {'suffix': 'YiB', 'divider': 1024 ** 8},
    {'suffix': 'ZiB', 'divider': 1024 ** 7},
    {'suffix': 'EiB', 'divider': 1024 ** 6},
    {'suffix': 'PiB', 'divider': 1024 ** 5},
    {'suffix': 'TiB', 'divider': 1024 ** 4},
    {'suffix': 'GiB', 'divider': 1024 ** 3},
    {'suffix': 'MiB', 'divider': 1024 ** 2},
    {'suffix': 'KiB', 'divider': 1024 ** 1},
)


class FileSize(Widget):
    """Displays the current count."""

    FORMAT = '%7.2f %s'

    def update(self, pbar):
        for unit in UNITS:
            if pbar.currval >= unit['divider']:
                return self.FORMAT % (pbar.currval / unit['divider'], unit['suffix'])
        return self.FORMAT % (pbar.currval, '  B')


class CompactETA(Widget):
    """Widget which attempts to estimate the time of arrival."""

    __slots__ = ('eta_format', 'complete_format')
    TIME_SENSITIVE = True

    def __init__(self, eta_format=' ETA: %s', complete_format='Time: %s'):
        self.eta_format = eta_format
        self.complete_format = complete_format

    @staticmethod
    def format_time(seconds):
        """Formats time as the string "HH:MM:SS"."""

        timedelta = datetime.timedelta(seconds=int(seconds))

        mm, ss = divmod(timedelta.seconds, 60)
        if mm < 60:
            return "%02d:%02d" % (mm, ss)
        hh, mm = divmod(mm, 60)
        if hh < 24:
            return "%02d:%02d:%02d" % (hh, mm, ss)
        dd, hh = divmod(mm, 24)
        return "%d days %02d:%02d:%02d" % (dd, hh, mm, ss)

    def update(self, pbar):
        """Updates the widget to show the ETA or total time when finished."""

        if pbar.currval == 0:
            return self.eta_format % '--:--'
        elif pbar.finished:
            return self.complete_format % self.format_time(pbar.seconds_elapsed)
        else:
            elapsed = pbar.seconds_elapsed
            eta = elapsed * pbar.maxval / pbar.currval - elapsed
            return self.eta_format % self.format_time(eta)


def pacman_progress_bar(*args, title='', **kwargs):
    title = '%s: ' % title if title else title
    return ProgressBar(
        widgets=[title, FileSize(), ' ', FileTransferSpeed(), ' ', CompactETA(eta_format="%s", complete_format="%s"),
                 ' ', Bar(left="[", right="]", fill='-'), ' ', Percentage()], *args, **kwargs)