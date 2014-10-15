import hashlib
from .iterx import SepIter

class FastaReader (SepIter):

    RECORD_SEP = '>'
    
    def __init__ (self, iterable):
        self.super = super(FastaReader, self) # set this for fast access by next()
        self.super.__init__(iterable, self.RECORD_SEP)
        
    def sequences (self):
        header, seq_iter = self.super.__next__()
        return (header, "".join(s.strip() for s in seq_iter))

    def md5sums (self):
        for header, seq_iter in self:
            md5 = hashlib.md5()
            for seqline in seq_iter:
                md5.update(seqline.strip().upper().encode())
            yield (header, md5.hexdigest())
