""" goulash.util
"""
import time, uuid

def uniq(use_time=False):
    """ """
    result = str(uuid.uuid1())
    if use_time: result+=str(time.time())[:-3]
    return result
