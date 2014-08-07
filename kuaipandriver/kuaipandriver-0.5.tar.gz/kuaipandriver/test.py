# -*-:coding:utf8 -*-
import sys
import time
from common import httpget
from threading import Thread


def chunk_task(threadId, block, url):
    start = block * threadId
    end = block * (threadId +1) -1;

    rangeheader = {"Range":"bytes=%d-%d" % (start, end)}
    print("downloading %s" % str(rangeheader))

    response = httpget(url, timeout=360, headers=rangeheader, allow_redirect=True, proxy="socks5://127.0.0.1:1082")
    if response.status_code == 206:
        with open("download/%d" % threadId, "w") as f:
            f.write(response.text)
        print("%s 下载完成" % ("download/%d" % threadId))    
    else:
        print("range %s download failed!" % str(rangeheader))
        print(response.text)

def getcontentlength(url):
    response = httpget(url, nobody=True, proxy="socks5://127.0.0.1:1082")
    print("正在获取文件信息......")
    if response.status_code == 200:
        return int(response.headers["Content-Length"])
    else:
        print response.headers
        raise Exception("文件信息获取失败" + str(response.status_code))

def flush(bar):
    sys.stdout.write("%s\r" % bar)
    sys.stdout.flush()


class Process(Thread):
    def __init__(self):
        super(Process, self).__init__()
        self.setDaemon(True)
        self.runflag = True

    def run(self):
        bar1 = "="
        for x in range(20):
            flush(bar1)
            time.sleep(0.1)
            bar1 = bar1 + "="

        while self.runflag:
           flush(bar1+"-")
           time.sleep(0.1)
           flush(bar1+"|")
           time.sleep(0.1)
           flush(bar1+"~")
           time.sleep(0.1)
           flush(bar1+"!")


def combinefile():
    import os
    os.chdir("download")
    files = os.listdir(".")
    files.sort()
    filelist = " ".join(files)
    cmd = "cat %s > ../files.img" % filelist
    print cmd
    print os.system(cmd)
    os.system("rm -f *")
    os.chdir("..")

def start():
    url = "https://android-apktool.googlecode.com/files/apktool-install-linux-r05-ibot.tar.bz2"
    tasknum = 5 
    totalsize = getcontentlength(url)

    print("开始下载 %s, 文件大小 %d" % (url, totalsize))
    tasks = []
    index = 0
    block = totalsize / tasknum if totalsize % tasknum == 0 else totalsize / tasknum +1

    for threadId in range(tasknum):

        task = Thread(target=chunk_task, args=(threadId, block, url))
        tasks.append(task)
        task.start()
        index += 1
    
    Process().start()
    for task in tasks:
        task.join()

    print("文件下载完成") 
    combinefile()


import pycurl
def gethandler(url):
    def callback(data):
        pass

    handler = pycurl.Curl()
    handler.setopt(pycurl.URL, url)
    handler.setopt(pycurl.WRITEFUNCTION, callback)

    return handler

def pool_handle(m):
    import pdb;pdb.set_trace()
    while 1:
        ret, num_handles = m.perform()
        if ret != pycurl.E_CALL_MULTI_PERFORM: break
        print num_handles
    while num_handles:
        ret = m.select(1.0)
        if ret == -1:  continue
        while 1:
            ret, num_handles = m.perform()
            if ret != pycurl.E_CALL_MULTI_PERFORM: break

if __name__ == '__main__':
    from common import BatchRequest
    mreq = BatchRequest()
    for url in ["http://localhost/phpmyadmin/index.php" for url in range(100)]:
        mreq.get("http://www.163.com")

    mreq.run()
    for rep in mreq.get_result():
        print rep.headers
