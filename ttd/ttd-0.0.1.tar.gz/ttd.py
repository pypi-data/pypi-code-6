import sys


def ttd(iterable, out=sys.stderr):
    total = len(iterable)
    print_ttd(0, total, out)
    for index, obj in enumerate(iterable, 1):
        yield obj
        print_ttd(index, total, out)
    sys.stdout.write('\r')


def print_ttd(index, total, out=sys.stderr):
    segments = 20
    percent = float(index) / total
    complete = "=" * int(percent * segments)
    empty = " " * (segments - len(complete))
    status = '\r[{}>{}] {}/{} {}%'.format(complete, empty, index, total, int(percent * 100))
    out.write(status)
