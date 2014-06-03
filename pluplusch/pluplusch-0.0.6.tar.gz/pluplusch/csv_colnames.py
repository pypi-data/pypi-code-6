import csv
def colnames(fp, *args, **kwargs):
    pos = fp.tell()
    result = next(csv.reader(fp, *args, **kwargs))
    fp.seek(pos)
    return result
