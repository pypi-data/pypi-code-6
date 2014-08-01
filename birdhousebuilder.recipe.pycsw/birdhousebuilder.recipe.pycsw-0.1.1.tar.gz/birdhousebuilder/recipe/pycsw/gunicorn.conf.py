import multiprocessing

bind = 'unix://${prefix}/var/run/${sites}.socket'
workers = multiprocessing.cpu_count() * 2 + 1

# environment
raw_env = ["HOME=${prefix}/var/lib/pycsw", 
           "PYCSW_CONFIG=${prefix}/etc/pycsw/${sites}.cfg", 
           "PATH=${prefix}/bin:/usr/bin:/bin", 
           ]                                                                                                               

# logging

debug = True
errorlog = '-'
loglevel = 'debug'
accesslog = '-'
