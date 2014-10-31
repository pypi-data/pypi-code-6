import libcapdapiRedHom_py as capd_impl

class BettiNumbersOverZ(object):

    def __init__(self, complex):
        self._complex = complex

    def __call__(self):
        complex_impl = self._complex.capd
        betti = capd_impl.BettiNumbersOverZ(complex_impl)()
        return dict(enumerate(betti))
