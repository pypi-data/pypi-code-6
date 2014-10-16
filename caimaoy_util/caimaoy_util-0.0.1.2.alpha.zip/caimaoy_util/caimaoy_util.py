# -*- coding: UTF-8 -*-

'''
caimaoy's util


Last modified time: 2014-10-14 19:36:09
Edit time: 2014-10-14 19:36:33
File name: process_exist.py
Edit by caimaoy
'''

import win32com.client

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

if __name__ == '__main__':
    pass

