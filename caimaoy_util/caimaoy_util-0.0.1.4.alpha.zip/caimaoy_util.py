# -*- coding: UTF-8 -*-

'''
caimaoy's util


Last modified time: 2014-10-14 19:36:09
Edit time: 2014-10-14 19:36:33
File name: process_exist.py
Edit by caimaoy
'''


def is_process_exist(p):
    '''判断windows系统下是否存在进程p
    '''

    try:
        import win32com.client
    except Exception as e:
        print e
    ret = 0
    try:
        WMI = win32com.client.GetObject('winmgmts:')
        processCodeCov = WMI.ExecQuery('select * from Win32_Process where Name="%s"' % p)
    except Exception as e:
        print p + "error : ", e;
    if len(processCodeCov) > 0:
        ret = True
    else:
        ret = False
    return ret


#tail.py
#Usage: python tail.py FILENAME LINES
#similar to linux command: tail -n LINES FILENAME
def last_lines(filename, lines = 1):
    #print the last several line(s) of a text file
    """
    Argument filename is the name of the file to print.
    Argument lines is the number of lines to print from last.
    """
    lines = int(lines)
    block_size = 1024
    block = ''
    nl_count = 0
    start = 0
    fsock = file(filename, 'rU')
    try:
        #seek to end
        fsock.seek(0, 2)
        #get seek position
        curpos = fsock.tell()
        while(curpos > 0): #while not BOF
            #seek ahead block_size+the length of last read block
            curpos -= (block_size + len(block));
            if curpos < 0: curpos = 0
            fsock.seek(curpos)
            #read to end
            block = fsock.read()
            nl_count = block.count('\n')
            #if read enough(more)
            if nl_count >= lines: break
        #get the exact start position
        for n in range(nl_count-lines+1):
            start = block.find('\n', start)+1
    finally:
        fsock.close()
    #print it out
    # print block[start:]
    return block[start:]

    '''
    import sys
    last_lines(sys.argv[1], sys.argv[2]) #print the last several lines of THIS file
    '''

if __name__ == '__main__':
    '''
    f = r'E:\test-pc-av\baidu_security\pc_av\Src\daily_build\result\Result\SystemScanPerf.txt'
    for i in last_lines(f, 5).split('\n'):
        print i
    '''
    pass
