version = VERSION = __version__ = "0.0.2"

def gcovparse(combined):
    # clean and strip lines
    assert ':Source:' in combined, 'gcov file is missing ":Source:" line(s)'
    files = filter(lambda f: f!='', combined.strip().split("0:Source:"))
    reports = map(_part, files[1:])
    return reports

def _part(chunk):
    report = {
        "file": chunk.split('\n',1)[0],
        "stats": {},
        "lines": []
    }
    map(lambda l: _line(l, report), chunk.strip().split('\n')[1:])

    return report

def _line(l, report):
    line = l.split(':', 2)
    if len(line)==3:
        hit, line, data = tuple(line)
        if data.startswith("Runs"):
            report["stats"]["runs"] = data[5:]
        elif data.startswith("Programs"):
            report["stats"]["programs"] = data[9:]
        elif int(line) > 0:
            report['lines'].append(dict(line=int(line.strip()), hit=None if '-' in hit else 0 if '#' in hit else int(hit.strip())))
