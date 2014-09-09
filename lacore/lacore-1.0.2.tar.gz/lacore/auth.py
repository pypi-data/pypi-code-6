import hashlib
import io

from lacore.adf.elements import Auth


class HashingMixin(object):
    def __init__(self, hashf='md5', *args, **kwargs):
        self.hashf = hashf
        self.hashobj = getattr(hashlib, hashf)()
        super(HashingMixin, self).__init__(*args, **kwargs)

    def update(self, data):
        self.hashobj.update(data)

    def digest(self):
        return self.hashobj.digest()

    @property
    def hashobj(self):
        return getattr(self, "_hash_" + self.hashf)

    @hashobj.setter
    def hashobj(self, hobj):
        setattr(self, "_hash_" + self.hashf, hobj)


class HashFile(HashingMixin, io.FileIO):
    def read(self, n):
        d = super(HashFile, self).read(n)
        if d is not None:
            self.hashobj.update(d)
        return d


class MyHashObj(HashingMixin):

    def __init__(self, hashf='sha512', *args, **kwargs):
        super(MyHashObj, self).__init__(hashf=hashf, *args, **kwargs)
        self.md5 = hashlib.md5()

    def update(self, data):
        self.md5.update(data)
        super(MyHashObj, self).update(data)

    def auth(self):
        args = {'md5': self.md5.digest()}
        args[self.hashf] = self.digest()
        return Auth(**args)

    def verify(self, auth):
        ret = (auth.md5 == self.md5.digest())
        if ret and hasattr(auth, self.hashf):
            h = getattr(auth, self.hashf)
            ret = (self.digest() == h)
        return ret
