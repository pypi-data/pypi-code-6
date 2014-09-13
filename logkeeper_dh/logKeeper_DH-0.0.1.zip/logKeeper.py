#-*-coding:encoding=utf-8 -*-

"""
logKeeper
	Description:
		该模块主要实现log保存，通过输入特定的字符串，使其保存在文件或数据库中。
		This module mainly for log keep. Information will be saved to document or database. 
	Author：	Daine Huang
	Date：		2014/09/12
	Version：	1.0.5
"""

def logKeeperAPI(filename, keyword, oriPayload, comment = '', type = 0):
    """
	logKeeperAPI:
		function for other application call.
		parameter:(keyword, oriPayload, comment = '')
	"""
    handle = connectedToLogfile(filename)
    payload = payloadAssemble(keyword, oriPayload, comment)
    writeLog(handle, payload, type)
    disConnectedFromLogfile(handle, type)

def creatLogfile(path, filename, type = 0, db_ip = 0, db_name = 0, userid = 'logkeeper', password = 'logkeeper' ):
    """
	creatLogfile:
		function to create log file.
		parameter:(path, filename, type = 0, db_ip = 0, db_name = 0, userid = 'logkeeper', password = 'logkeeper' )
			type 0 is create a file, type 1 is try to connect a database and create a log table.
	"""
    import os
    import time
    path=path.strip()
    path=path.rstrip("\\")
    if type == 0:
        isPathExist = os.path.exists(path)
        currentDate = time.strftime('%Y-%m-%d',time.localtime(time.time()))     
        if not isPathExist:
            os.makedirs(path)				#绝对路径创建
            #os.makedirs('.\\test\\test2')	#当前路径下创建
            #os.makedirs('..\\test\\test2')	#前一级路径下创建
            currentTime = time.strftime('%Y-%m-%d_%H:%M',time.localtime(time.time()))
            file = path + '\\' + filename + '-' + currentDate + '.log'
            fileHandle = open(file, 'w' )
            fileHandle.write('# -*-coding:encoding=utf-8 -*-\n# Logfile\n# Date:'+currentTime + '\n\n')
            fileHandle.close()
            print('\nCreate:  \'' + file + '\' successful!!\n')
        if isPathExist:
            currentTime = time.strftime('%Y-%m-%d_%H:%M',time.localtime(time.time()))
            file = path + '\\' + filename + '-' + currentDate + '.log'
            fileHandle = open(file, 'w' )
            fileHandle.write('# -*-coding:encoding=utf-8 -*-\n# Logfile\n# Date:'+currentTime + '\n\n')
            fileHandle.close()
            print('\nCreate:  \'' + file + '\' successful!!\n')
    return file

def connectedToLogfile(file, type = 0, db_ip = 0, db_name = 0, userid = 'logkeeper', password = 'logkeeper' ):
    """
	connectedToLogfile:
		function to open a log file or connect to database.
		parameter same like 'creatLogfile()'
	"""
    if type == 0:
        handle = open(file, 'a')
    return handle
	
def disConnectedFromLogfile(handle, type = 0):
    """
	disConnectedFromLogfile:
		function to close a log file or disconnect from database.
		parameter:(type, handle)
	"""
    if type == 0:
        handle.close()
        #print('\nLog file (closed & saved) .')
    return 0

def writeLog(handle, payload, type = 0):
    """
	writeLog:
		function to write payload to log file.
		parameter:(type, handle, payload)
	"""
    if type == 0:
        ret = handle.write(payload)
    return ret

def payloadAssemble(keyword, oriPayload, comment = '', date_time = 1):
    """
	paloadAssemble:
		function to assemble payload, add keyword highlight and current time, make it easy to bug shooting.
		parameter:(oriPayload, keyword, date_time = 1)
	"""
    import time
    if date_time == 1:
        currentTime = time.strftime('%Y-%m-%d_%H:%M',time.localtime(time.time()))
        payload = '\n' + currentTime + '||' + keyword + '||' + oriPayload + '||' + comment
    else:
        payload = '\n' + keyword + '||' + oriPayload + '||' + comment
    return payload



# This is demo
# build version：0.1
# Author: Daine Huang
# Date: 2014/09/12

if __name__ == '__main__':
    print('logKeeper testing!\nlogKeeper 测试!\n')
    import os
    path = os.getcwd()
    tfile = input('\nInput file name for tests:')
    filename = creatLogfile(path,tfile)
    testpool = ['FFAABBCCDD12','FFAABBCCDD13','FFAABBCCDD14','FFAABBCCDD15','FFAABBCCDD16','FFAABBCCDD17']
    for oripayload in testpool:
        logKeeperAPI(filename, 'Only for tests', oripayload, 'This is comment!' )
