from multiprocessing import Pool
from time import sleep


def f(x):
    print str(x) + ' - start'
    sleep(x)
    print str(x) + ' - stop'
    return x * x


if __name__ == '__main__':
    pool = Pool(processes=2)  # start 4 worker processes
    result = pool.apply_async(f, [1])  # evaluate "f(10)" asynchronously
    print pool.map(f, range(2))  # prints "[0, 1, 4,..., 81]"