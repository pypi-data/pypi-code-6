from multiprocessing import pool
import Queue


class CheckableQueue(Queue.Queue):

    def __contains__(self, item):
        with self.mutex:
            boo = item in self.queue
            print "%s in CheckableQueue: [%s]" % (item, boo)
            return boo

    def put(self, item, block=False, timeout=1):
        print "Putting [%s]" % item
        try:
            Queue.Queue.put(self, item, block=block, timeout=timeout)
        except Queue.Full:
            try:
                print "Queue Full! Removing one item."
                self.get_nowait()
            except Queue.Empty:
                print "Queue Empty?"
                pass
            self.put(item)


QQ = CheckableQueue(maxsize=30)

def putter(thing):

    return QQ.put(thing)

def isin(another):

    return another in QQ


def main():
    tpool = pool.ThreadPool()
    ppool = pool.Pool()

    tpool.map(putter, xrange(300))
    tpool.map(isin, xrange(300))
    ppool.map(putter, xrange(600, 900))

if __name__ == '__main__':
    main()

