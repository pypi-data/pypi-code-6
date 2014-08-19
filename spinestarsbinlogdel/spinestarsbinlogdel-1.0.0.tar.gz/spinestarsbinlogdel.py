#!/usr/bin/env python
# coding=utf-8
# 2014-08-19
# BY Spinestars
# path: [日志存放路径]
# TF: True 定义关键字，False 不定义关键字
# 	log_name: [日志后缀前的关键字,以点号分割]
# m: [定义需要保留的日志文件数]
def log_del(path, TF, log_name, m=5):
    #调用os模块,re模块
    import os 
    import re
    #获取日志文件所在文件夹内的所有文件列表
    libs = os.listdir(path)
    #通过关键字，排除非日志文件,获取只含有日志文件的列表l
    l = []
    for a in libs:
        if TF == "True":
            if a.split('.')[0] == log_name and re.findall(r'\d+',a.split('.')[1]):
                l.append(a)
        else:
            if re.findall(r'\d+',a.split('.')[1]):
                l.append(a)
    print l
    #定义一个临时列表，用来存放日志文件的key（内容是后缀数字）
    L = []
    #定义一个计数，用来记录日志文件列表的当前数
    i = 0
    #循环日志文件后缀数字，用来生成日志文件的字典所需的key列表
    while True:
        lib = l[i]
        s = int(lib.split('.')[1])
        L.append(s)
        i = i + 1
        if i == len(l):
            break
    #构建一个字典，key是日志文件后缀数字，value是对应的日志文件名
    d1 = dict(zip(L, l))
    #逆序排列字典，便于删除早期日志文件
    vd1 = d1.values()[::-1]
    #如果最初获取的日志文件列表小于m个，则不执行删除
    if len(l) <= m:
        print "bin_log files == %d" %(len(l))
    else:
    #执行循环，删除多余的文件
        while True:
    #获取对应key=m之后的对应日志文件
            value = vd1[m]
            print "The %s is del!" %(value)
            del_command = "rm -rf /home/spinestars/test/%s" %(value)
    #调用del_command命令
            os.system(del_command)
            m = m + 1
    #一直删除到m等于日志文件列表的上限
            if m == len(l):
                break
    print "del finish"
