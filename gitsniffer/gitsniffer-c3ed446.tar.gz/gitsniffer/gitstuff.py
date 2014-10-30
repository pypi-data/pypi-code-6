from collections import namedtuple


GitObj = namedtuple("GitObj", "fname prefix hash")


metadata = [
    'refs/heads/master', 'refs/remotes/origin/HEAD',
    'COMMIT_EDITMSG',
    'config',
    'description',
    'FETCH_HEAD',
    'HEAD',
    'index',
    'ORIG_HEAD',
    'packed-refs',
    'logs/HEAD',
    "logs/refs/remotes/origin/HEAD",
    "logs/refs/heads/master",
]


def generate_objects(index):
    """
    Take the index file and extract the paths to all the object files
    The object paths are in the format of <aa>/<biglonghashthing>
    """
    for entry in index:
        fullhex = entry.hex
        fname = entry.path
        prefix, h = fullhex[0:2], fullhex[2:]
        yield GitObj(fname, prefix, h)
