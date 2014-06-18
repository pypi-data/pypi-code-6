class chromRange:
    chrom = ''
    start = 0
    end = 0

    def dict(self):
        dict = {
                'chrom': self.chrom,
                'start': self.start,
                'end': self.end}
        return dict

    def __init__(self, chrom, start, end):
        self.start = start
        self.end = end
        self.chrom = chrom

