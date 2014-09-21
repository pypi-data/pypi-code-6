
import numpy as np

def wordtoarray(words, nstr):
    """
    """
    nwords = len(words)
    result = np.empty((nwords, nstr), dtype="S1")
    for iw, word in enumerate(words):
        result[iw, :] = list(word.ljust(nstr)[:nstr])
    return result

def arraytoword(data, strip=False):
    """
    """
    nw, ns = data.shape
    result = [data[iw,:].tostring() for iw in xrange(nw)]
    if strip:
        result = [word.strip() for word in result]
    return result


