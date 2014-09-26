# This is c.py
import logging

# Make a global logging object.
x = logging.getLogger("logfun")
x.setLevel(logging.DEBUG)
h = logging.StreamHandler()
f = logging.Formatter("%(levelname)s %(asctime)s %(funcName)s %(lineno)d %(message)s")
h.setFormatter(f)
x.addHandler(h)

def g():

    1/0

def f():

    logfun = logging.getLogger("logfun")

    logfun.debug("Inside f!")

    try:

        g()

    except Exception, ex:

        logfun.exception("Something awful happened!")

    logfun.debug("Finishing f!")

if __name__ == "__main__":
    f()

