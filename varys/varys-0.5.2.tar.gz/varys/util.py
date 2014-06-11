def ensure_dir(dir_path, overwrite=False):
    from shutil import rmtree
    from os.path import isdir, exists
    from os import makedirs
    if exists(dir_path):
        if not isdir(dir_path):
            raise ValueError("%s is a file..." % dir_path)
        if overwrite:
            rmtree(dir_path)
    if not exists(dir_path):
        makedirs(dir_path)

def detect_encoding(file_path):
    from chardet.universaldetector import UniversalDetector
    u = UniversalDetector()
    with open(file_path, 'rb') as f:
        for line in f:
            u.feed(line)
        u.close()
    result = u.result
    if result['encoding']:
        return result['encoding']
    return None

def numberfy(s):
    n = s
    try:
        n = float(n)
        return n
    except Exception:
        return s

def intify(s):
    n = s
    try:
        n = int(n)
        return n
    except Exception:
        return s

def read_df(file_path, delimiter='\t'):
    # maybe use sniffer to unify this and csv reader... would be better
    import io
    enc = detect_encoding(file_path)
    f = io.open(file_path, encoding=enc)
    lines = [line.split(delimiter) for line in f]
    f.close()
    lines = [line for line in lines if len(line) != 0]
    length = len(lines[0])
    if not all([len(line) == length for line in lines]):
        raise ValueError("tdf error, not all rows had the same length in %s" % file_path)
    fieldnames = [c.encode('utf-8').strip() for c in lines[0]]
    bad_chars = "".join([c for f in fieldnames for c in f if not c.isalnum()])
    fieldnames = [f.strip(bad_chars) for f in fieldnames]
    dict_lines = []
    for line in lines[1:]:
        d = {}
        for i in xrange(length):
            d[fieldnames[i]] = numberfy(line[i].encode('utf-8').strip())
        dict_lines.append(d)
    return dict_lines

def read_tdf(file_path):
    return read_df(file_path, delimiter='\t')

def read_csv(file_path):
    return read_df(file_path, delimiter=',')

def round_to(x, base=2.5):
    return base * round(float(x)/base)
