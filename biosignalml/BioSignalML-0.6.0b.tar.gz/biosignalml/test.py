class B(object):

  def __init__(self, a, b=1):
    self._a = a
    self._b = b


B.a = lambda self: self._a
B.b = lambda self: self._b
B.c = lambda self: self._c


class C(B):
  def __init__(self, base=2):
    B.__init__(self, 'C', b=base)
    self._c = 'xx'
    self.__class__ = B
