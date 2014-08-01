import os
import shutil
import wrapper
import community

# inputfile name and no of passes
def detect(filename, nop = -1, debug = False):
    comdet_tmppath = 'comdet_tmp'
    fileinput = open(filename, 'r')
    lines = fileinput.readlines()
    p1 = wrapper.Pool()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        split = line.split(' ')
        n1 = p1.get_node(split[0])
        if not n1:
            n1 = p1.add_node(split[0])
        n1.add_elem(split[1])
    if os.path.exists(comdet_tmppath):
        shutil.rmtree(comdet_tmppath)
    os.mkdir(comdet_tmppath)
    os.chdir(comdet_tmppath)
    com_t = community.community()
    result = com_t.start(p1, nop, debug)
    os.chdir('..')
    if os.path.exists(comdet_tmppath):
        shutil.rmtree(comdet_tmppath)
    return result
