import os

# split path and ext greedily, g for greedy
def gsliptext(path):
    while True:
        path, ext = os.path.splitext(path)
        if not ext:
            print path
            break
        else:
            print ext