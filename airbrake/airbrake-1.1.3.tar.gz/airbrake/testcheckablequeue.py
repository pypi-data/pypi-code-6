#import eventlet
#eventlet.monkey_patch()

from concurrent import futures

from airbrake.utils import CheckableQueue

QQ = CheckableQueue(maxsize=30)

def putter(thing):

    return QQ.put(thing)

def isin(another):

    return another in QQ


def main():
    tpool = futures.ThreadPoolExecutor(4)

    import pprint
    pprint.pprint([x for x in tpool.map(putter, xrange(300))])
    pprint.pprint([x for x in tpool.map(isin, xrange(300))])
    pprint.pprint([x for x in tpool.map(putter, xrange(600, 900))])

if __name__ == '__main__':
    main()

