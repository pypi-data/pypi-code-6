#-*-coding:encoding=utf-8 -*-
import win32gui
import win32con
import win32api
import win32process
import time
import configparser
import os
import sys
from win32com.shell import shell, shellcon
import shutil
from xml.etree import ElementTree as ET
#from random import randrange as random
import random
import serial

"""
	diagnosis
	这个模块主要是抽象了Yxm工具的操作，模块中有一个DiagnosisClass类，通过这个类可以实现操作Yxm，切换工位，扫描STBID段的功能。
	这个类基于Python 3.4.1 编写，外挂有pywin32,xml.etree.ElementTree,os,sys,shutil 模块
	
	Author：	Daine Huang
	Date：		2014/08/12
	Version：	1.0.5

"""


class DiagnosisClass(object):
    """
	************************************************************************************
	2014/06/10	DiagnosisClass 在版本1.0时完成了基本功能。在V1.0中，可以通过这个类实现：
		1.指定工作路径
		2.指定Yxm目标Title（主要是需要Titile来对win下的Yxm窗口寻址）
		3.实现了启动和关闭Yxm
		4.实现了修改main.xml来切换工位，并且自动重启Yxm进入下一工位测试
	2014/07/16 	DiagnosisClass	autoSendStbid()
	在版本1.03中完成了自动扫描功能。通过这个功能可以实现：
		1.指定扫描DiagnosisCfg.xml中的主板生成序列号或整机生产序列号
		2.指定是否根据区间生成随机数
	2014/07/17	DiagnosisClass	renameYxmLogfile()
	在版本1.04中完成了扫描计数，因为Yxm 的logfile有5000条记录后会在当天无法继续使用，所以在类中增加了：
		1.计数次数，完成5000次为单位的次数self.YxmLogCount = {'scanWidth':5000,'scanCount':0}
		2.在DiagnosisClass	autoSendStbid()添加对YxmLogCount的计算
		3.每当扫描5000个记录后， 会调用DiagnosisClass	renameYxmLogfile()处理YxmLogfile
	2014/08/12	开始针对模块做较大改动，编译成模块发布后，发现初始化必须依赖DiagnosisCfg.xml所以需要改动：
		1.初始化不依赖DiagnosisCfg.xml
		2.新建方法用于读入DiagnosisCfg数据覆盖初始化数据。
		3.增加代码内库版本元组
	2014、08、19
	增加串口操作模块
	************************************************************************************
	"""


    #def __init__(self,title = 0,cfg = 'DiagnosisCfg.xml'):
    def __init__(self,title = 0):
        """2014/06/11	新增了读取xml配置文件完成title的设置，同时会有YxmCfg的节点可以操作"""
        """
        cfgFile = cfg
        self.DiagnosisCfgFileTree = ET.parse(cfgFile)
        self.DiagnosisCfgRoot = self.DiagnosisCfgFileTree.getroot()
        """
        self.index = -1#YxmClient对象的真正进程句柄
        self.execTarget = "YxmClient.exe"#YxmClient的目标名
        self.handle = -1#YxmClient的窗口句柄
        self.netStatus =-1#YxmClient和机顶盒之间网络连接状态
        self.YxmPID = -1
        self.isYxmOpen = 0
        self.editArea = 0
        self.defaultStage = 0
        self.title = 0
        self.ourFactoryStartId = 0
        self.thirdPartFactoryStartId = 0
        self.execPath = os.getcwd()
        self.stageCfgFile = self.execPath + "\\main.xml"
        self.serialport = -1
		
        self.YxmLogCount = {'scanWidth':5000,'scanCount':0}
        """
		2014/07/17	YxmLogCount
			1.因为Yxm程序每天扫描只能扫5023个id，所以需要一个宽度来处理更大宽度的自动化测试
			2.用于处理本次任务扫描5000个号码以后的计数
        """
		
        self.modelVersion = {'Version':'1.0.5','Date':'2014/08/12','Author':'Daine Huang','Email':'daine199@gmail.com'}
        """
		2014/08/15 修改
			模块版本(Version)	：1.0.6
			更新日期(Date)		：2014/08/19
			作　　者(Author)	：Daine Huang
			电子邮件(Email)		：daine199@gmail.com
		"""
		
		
        #self.execPath = "C:\\pc_tool_V35_without_nrc_6_4\\pc_tool_V35_without_nrc_6_4\\pc_tool_V35_ourfactory_without_nrc_6_4"
        #self.execPath = "C:\\pc_tool_V35_ourfactory_with_nrc_8_6"

        # 设置光标坐标位置，不同显示器分辨率计算机位置可能不一样。
        # 一位数的光标是相对(25,185)
        self.oriPosXY = {'oriPosY':125,'cffctX':7.9}#oriPosY y的坐标，cffctX：根据宽度计算x的系数
        self.posTarget = () # 根据宽度计算后返回的坐标值，可以考虑放进snIn
        self.posSetWidth14Line1=(125,226)# 14位宽度数据的光标位置(135,217)
        self.posSetWidth26Line1=(220,226)#华数26位宽度数据光标位置(220,217)

        # 初始化STBID扫描参数,这些参数用于传递进方法中进行循环
        self.snIn ={}			#扫描参数用字典确认
        """2014/06/14	目前含有参数
				str		prefix
				int		Start
				int		End
				int		Len
				str		Type	值有“10”和“16”	
				int		totalWidth	组装好的数据宽度
				之后可能会增加直接计算好的鼠标坐标posTarget:(int(x),int(y))"""


        print("初始化成功！\n"
			"\nModelVersion	:" + self.modelVersion['Version'] +
			"\nDate		:" + self.modelVersion['Date'] +
			"\nAuthor		:" + self.modelVersion['Author'] +
			"\nEmail		:" + self.modelVersion['Email'] + "\n")
		

    def loadDiagnosisCfg(self,cfg = 'DiagnosisCfg.xml'):
        """
		2014/08/12
		新增该方法，用于把读DiagnosisCfg.xml独立到初始化方法之外，使初始化不必一定要有DiagnosisCfg.xml才能完成。
		"""
        DiagnosisCfgPath = self.execPath + "\\" +cfg
        if not os.path.exists(DiagnosisCfgPath):
            print("No DiagnosisCfg.xml found in " + self.execPath + "\n You can Download it by 'http://'")
        else:
            self.DiagnosisCfgFileTree = ET.parse(DiagnosisCfgPath)
            self.DiagnosisCfgRoot = self.DiagnosisCfgFileTree.getroot()
            self.stageSet = self.DiagnosisCfgRoot.attrib['defaultStage']			
            # 读取配置文件Title
            if self.title != 0:
                print("Current Title is: " + self.title + "\n")
            else:
                self.title = self.DiagnosisCfgRoot.attrib['title']
                print("Current Title is " + self.title + "\n")
            # 读取配置文件STBID起止信息 也是sourceFilter()的数据来源
            self.ourFactoryStartId = self.DiagnosisCfgRoot[0][0].attrib
            self.thirdPartFactoryStartId = self.DiagnosisCfgRoot[0][1].attrib

    """
	1.手动设置工作环境
	"""
    def setTitle(self,title = 0):#设置Yxm目标程序的标题
        """
		2014/06/11	
		重写了该方法，会判断3次空输入则会停止重试，如果函数在调用的时候没有默认值，则会启动一共3次输入，如果3次输入还没有值，则不会重写Title
		2014/08/12
		发现如果把diagnosis编译成模块，则会出现retry变成常数无法重试，所以需要取消setTitle方法中的while循环。
		"""
        print("Set Title porcess...\n")
        if title != 0:
            self.title = title
        else:
            #retry = 1
            title = input("\n请输入测试对象Title：\n")
            self.title = title
        print("Title now is: " + self.title)


    def setYxmPath(self):#设置Yxm的工作路径
        """2014/06/11	setYxmPath 和 pathCallbackProc 两个函数共同作用，获取路径，setYxmPath本身拿不到路径值，主要用于画窗口，遍历路径，产生路径对象，通过
						pathCallbackProc去读取路径对象，解析出路径字符串赋值self.execPath"""
        try:
            flags = shellcon.BIF_STATUSTEXT
            shell.SHBrowseForFolder(0, # parent HWND
                                    None, # root PIDL.
                                    "Default of %s" % self.execPath, # title
                                    flags, # flags
                                    self.pathCallbackProc, # callback function
                                    os.getcwd() # 'data' param for the callback 每次选择一个路径后，会在这个路径上取得路径pwd的字符串，会变成回调函数的输入变量
                                    )
            return self.execPath
        except:
            print("\n寻找路径错误.\n")
    def pathCallbackProc(self, hwnd, msg, lp, data):#查询工作路径回调函数
        if msg== shellcon.BFFM_INITIALIZED:
            win32gui.SendMessage(hwnd, shellcon.BFFM_SETSELECTION, 1, data)
        elif msg == shellcon.BFFM_SELCHANGED:
            pidl = shell.AddressAsPIDL(lp)
            try:
                execPath = shell.SHGetPathFromIDList(pidl)
                win32gui.SendMessage(hwnd, shellcon.BFFM_SETSTATUSTEXT, 0, execPath)
                self.execPath = execPath.decode()
                self.stageCfgFile=self.execPath+"\\main.xml"
                #print(self.execPath) #这里实现每选一次目录都会打印
            except shell.error:
            # No path for this PIDL
                pass
    """手动设置工作环境"""


    """
	2.启动和关闭Yxm，注册Yxm到对象
	"""
    def getPID(self):
        try:
            ez = win32process.GetWindowThreadProcessId(self.handle)
            #print(ez[0]," 这里是对应线程ID")
            #print(ez[1]," 这里是对应进程ID")
            self.YxmPID = ez[1]
        except:
            print("找不到Yxm程序!\n")
    def killProc(self):
        if self.isYxmOpen == 1:
            handel = win32api.OpenProcess(1,0,self.YxmPID)
            win32api.TerminateProcess(handel,0)
            self.handle = -1
            self.isYxmOpen = 0
            self.netStatus = -1
            print("\nYxm Closed.\n")
        else:
            print("\nNo Yxm process found!\n")

    def openYxm(self):#尝试启动Yxm程序
        """2014/06/13	用于启动Yxm，主要实现从self.execPath 中启动YxmClient.exe程序"""
        try:
            if(os.path.exists(self.execPath+"\\main.xml") == False):
                shutil.copy(self.execPath+"\\main.xml.old",self.execPath+"\\main.xml")
            print("Try run :",self.execTarget,"@ ",self.execPath)
            win32api.ShellExecute(None, "open" , self.execTarget , None , self.execPath , 1 )
            self.isYxmOpen = 1
            return 1
        except:
            print("Run ",self.execTarget,"Failed！","请检查工作路径和Title设置。")
            self.isYxmOpen = 0
            return 0
        #win32api.ShellExecute(None, "open" , self.execTarget , None , "C:\\pc_tool_V35_thirdpart_4_2\\pc_tool_V35_thirdpart_4_2" , 1 )
		#（父进程句柄，打开模式，"目标程序名"，参数，"路径"，后台还是前台打开）
    def accessYxm(self):#注册Yxm对象
        """2014/06/13	用于注册Yxm程序到对象，如果Yxm没有启动，会尝试启动Yxm"""
        print("Try access Yxm...")
        try:
            retry=1
            while retry < 4:
                if not self.title or self.title == -1:
                    self.setTitle()
                #elif self.title == -1:
                elif self.execPath == -1:
                    self.setYxmPath()
                elif self.isYxmOpen == 0:
                    self.openYxm()
                    time.sleep(3)
                    retry +=1
                elif self.isYxmOpen == 1:
                    self.isYxmExist()
                    retry = self.setTarget()
                    self.checkConnection()
                    break
                else:
                    Print("对象已成功注册。")
                    break
        except:
            print("注册Yxm对象失败！")
            return -1
    def setTarget(self):#绑定Yxm窗口到对象
        """2014/06/11	重写了查询，会调用self.isYxmExist()来查询Yxm窗口句柄，当没有发现Yxm窗口时，会尝试从初始化的路径中打开Yxm"""
        print("Try find Yxm window...\n")
        retry = 4
        while retry ==4:
            self.isYxmExist()
            #self.handle = win32gui.FindWindow(None,self.title)
            if self.handle == -1:
                print("Target not found!")
            #win32api.MessageBox(0, "Not find PC tool application.","Error",win32con.MB_ICONERROR)
                retry = win32api.MessageBox(0, "Not find PC tool application.","Error",5)
                self.isYxmOpen = self.openYxm()
            #int = MessageBox(hwnd, message , title , style , language )
            #sytle(1:OK,Cancel;2:Abort,retry,Ignore;3:Yes,No,Cancel;4:Yes,No;5:Retry,Cancel;6:Cancel,Try Again,Continue;)
            #return (1:OK;2:cancel;3:Abort;4:retry;5:Ignore;6:Yes;7:No;10:Try Again;11:Continue;)
            #print(retry)
            else:
                retry = 0
                print("\nYxm Accessed!\nTarget is ",self.handle,".\n")
                return self.handle

    def termTarget(self):#关闭已绑定的Yxm窗口
        """2014/06/11	termTarget(self)用于关闭Yxm窗口,在关闭前会尝试注册一次Yxm"""
        print("Kill Yxm process...\n")
        #self.accessYxm()
        #print("Kill Yxm!\n")
        self.getPID()
        self.killProc()
        print("Yxm kill process done! If Yxm didn't be killed, Please close Yxm manually.\n")
        return 0
    def restartYxm(self):#重启Yxm窗口
        """2014/06/13	主要用于自动切换工位时的重启Yxm程序(未完成)"""
        print("Yxm restart!")
        self.termTarget()
        time.sleep(1)
        self.accessYxm()
    """启动和关闭Yxm，注册Yxm到对象"""

	
	
	

    """
	3.设置Yxm配置文件
	"""
    def setMainStage(self,stage=0):#设置执行工位
        """2014/06/11	由于有时候main.xml不是UTF-8的标准头，所以本方法采用普通文件的方式打开main.xml，查询StationIndex位置来改变工位
						修改方式会先查询main.xml.old是否存在，如果不存在会先备份main.xml到main.xml.old
						如果main.xml.old存在，则会直接用main.xml.old做为模板来修改工位
						如果main.xml和main.xml.old都不存在，则会返回设置工位失败的消息"""
        mainFile = self.execPath+"\\main.xml"
        oldMainFile = mainFile+".old"
        try:
            if not os.path.exists(oldMainFile):
                os.rename(mainFile,oldMainFile)

            self.stageSet = str(stage)
            xmlRutf8 = open(oldMainFile,'r',encoding='UTF-8')
		    #启动读取的文件句柄，由于产测的main.xml可能是gbk或GB2312编码，无法直接用ET.parse直接打开文件，所以用open重编码后打开兼容性最好。
            xmlWutf8 = open(mainFile,'w',encoding='UTF-8')

            aString= xmlRutf8.read()

            where = aString.find('StationIndex="')#解析工位attrib对应位置
            target1 = where+14
            target2 = where+15
	
            s1=aString[:target1]#切片写入的字符串的前半截
            s2=aString[target2:]#切片写入的字符串的后半截

            stage=s1+self.stageSet+s2#组装工位
 
            xmlWutf8.write(stage)
            xmlWutf8.close()
        except:
            print("\n找不到main.xml，工位设置失败！\n")
    def switchStage(self,stage = None):
        """
		2014/07/17
			封装了设置工位，可以在调用的时候设置或调用后在里面输入
        """
        print("正在切换工位！\n")
        stageList = (0,1,2,3,4)
        while stage not in stageList:
            stage = int(input("\n请输入需要设置的工位(0，1，2:Scan，3:Check,4:组合工位)："))
        self.setMainStage(stage)
        self.restartYxm()

    def renameYxmLogfile(self,suffix = None):
        """
		2014/07/17
			封装了修改Yxm logfile名的函数，该函数根据输入的suffix,或全局变量的YxmLogCount['scanCount']来标记新生成的文件
		"""
        print("正在重命名YxmLogfile!")
        logFilePath = self.execPath + '\\OutPut'
        date = str(time.strftime('%Y%m%d',time.localtime(time.time())))
        scanLogFileName = 'stbinfo_' + date + '_scan.txt'
        scanLogInput = logFilePath + '\\' + scanLogFileName
        #print(scanLogInput)
        if os.path.exists(scanLogInput) is True:
            if suffix is None:
                scanLogTarget = scanLogInput +"_"+ str(self.YxmLogCount['scanCount'])
                os.rename(scanLogInput,scanLogTarget)
                print("rename by YxmLogCount！\n")
                return 0
            else:
                scanLogTarget = scanLogInput + "_" + str(suffix)
                os.rename(scanLogInput,scanLogTarget)
                print("rename by input!\n")
                return 0
        else:
            print("Not found " + scanLogInput)



    """
		2014/06/13
			这里开始的函数findEditTarget，sendStbid，都是用于scan/check的，具体使用方式看函数说明。
    """

    def findEditTarget(self):
        """2014/06/13	这个函数用于找到输入窗口句柄"""	
        dlg1 = win32gui.FindWindowEx(self.handle, None, 'SysTabControl32', None)   
        #print(dlg1)
        dlg2 = win32gui.FindWindowEx(dlg1, None, '#32770', None)   
        #print(dlg2)
        dlg3 = win32gui.FindWindowEx(dlg2, None, 'Edit', None)
        self.editArea = dlg3
        if dlg3 == 0:
            print("No Edit area Found!")
        else:
            print("窗口句柄为："+str(self.editArea))
        return dlg3
		
    def autoSendStbid(self,ifrandom = False,ifthirdpart = False,width = 2000000):
    #def autoSendStbid(self):
        """
		2014/06/12	自动持续scan，这里设定所有输入的ID都已经转换为整型,该函数用于循环scan STBID.需要优化计算速度和计算量。
		2014/07/09
			1.增加random字段和第三方或本方工厂配置字段,配置扫描主板生成或整机生产的不同长度的盒号
			2.增加扫描3000次后重启Yxm的判断
		2014/07/17
			1.发现重启Yxm没有用，Yxm本身不会重建scanLogfile，所以增加了：
				self.YxmLogCount = {'scanWidth':5000,'scanCount':0}
				通过这个结构来计数扫描次数，并且在5000次测时候通过方法self.renameYxmLogfile()对Yxm的logfile做重命名。
		"""
        self.accessYxm()
        self.findEditTarget()
        listScan = []
        calcNumber = 0
        calcWidth = 0
        print(width)
        if ifthirdpart is True:
            posSetWidth = self.posSetWidth26Line1
            prifix = self.thirdPartFactory['prefix']
            startStbID = int(self.thirdPartFactory['start'],16)
            endStbID = int(self.thirdPartFactory['End'],16)
            lenStbID = len(self.thirdPartFactory['start'])
            #print(prifix)
        elif ifthirdpart is False:
            posSetWidth=self.posSetWidth14Line1
            prifix = self.ourFactory['prefix']
            startStbID = int(self.ourFactory['start'],16)
            endStbID = int(self.ourFactory['End'],16)
            lenStbID = len(self.ourFactory['start'])
            #print(prifix)
        else:
            print("\nautoSendStbid()第二个参数需要输入0或1,0:ourfactory,1:thirdpartfactory\n")

        print(prifix, startStbID, endStbID, lenStbID)
			# 处理随机循环列表

        if ifrandom is True:
            randomData = range(startStbID,endStbID)
            print(randomData)
            if width > int(endStbID - startStbID - 1):
                width = int(endStbID - startStbID - 1)
            print(width)
            #sampleWidth = abs(startStbID - endStbID)
            #print(sampleWidth)
            randomList = random.sample(randomData,width)
            #print("randomlist")
            listScan = randomList
            #print(listScan)
        else:
            listScan = range(startStbID,endStbID)
            print(listScan)
        for NextSn in listScan:
            #print("进入循环")
            #inputTextSn = self.ourFactory['prefix'] + ('%X' % NextSn).zfill(lenStbID)
            inputTextSn = str(prifix) + ('%X' % NextSn).zfill(lenStbID)
            #print("目标值为:"+inputTextSn)
            #print(self.editArea)
            win32api.SendMessage(self.editArea,win32con.WM_SETTEXT,None,inputTextSn)
            point_pos= win32gui.ClientToScreen(self.handle,posSetWidth)
            win32gui.SetForegroundWindow(self.handle)
            time.sleep(0.5)
            win32api.SetCursorPos(point_pos)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
            time.sleep(0.05)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
            time.sleep(0.05)
            win32gui.EnableWindow(self.handle,1)
            time.sleep(1)
            win32gui.PostMessage(self.editArea, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            time.sleep(1)
            calcNumber = calcNumber + 1
            calcWidth = calcWidth + 1
            if calcWidth >= width:
                print("完成指定宽度或完成DiagnosisCfg描述范围Scan操作！\n")
                break
            print("计数器值"+ str(calcNumber))
            if calcNumber >= self.YxmLogCount['scanWidth']:
                self.YxmLogCount['scanCount'] += 1
                print("计数器" + str(self.YxmLogCount['scanWidth'])+" "+str(self.YxmLogCount['scanCount']))
                self.termTarget()
                time.sleep(4)# 需要一个等待Yxm释放logfile的时间
                self.renameYxmLogfile(None)
                self.accessYxm()
                time.sleep(3)#需要一个等待Yxm启动并且注册handle的时间
                #print(4)
                self.findEditTarget()
                print(prifix, startStbID, endStbID, lenStbID)
                calcNumber = 0
                #print(5)
#        except:
#            print("\n第一个参数设置是否需要在范围内随机生成scan数据入0或1,0:NO,1:yes")
#            print("第二个参数需要输入0或1,0:ourfactory,1:thirdpartfactory\n")



    def sendOnce(self,hd,whd,pos,val):#发送一次值到指定位置
        """2014/06/13	主窗口句柄，编辑窗口句柄，光标位置int(x),int(y)，发送值str"""
        win32api.SendMessage(whd,win32con.WM_SETTEXT,None,val)
        point_pos= win32gui.ClientToScreen(self.handle,pos)
        win32gui.SetForegroundWindow(hd)
        time.sleep(0.5)
        win32api.SetCursorPos(point_pos)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        time.sleep(0.05)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        time.sleep(0.05)
        win32gui.EnableWindow(hd,1)
        time.sleep(1)
        win32gui.PostMessage(whd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        time.sleep(1)

    #def ts(self):
        #win32api.SetCursorPos((125,226))
        #print(random(1000))

    #def scanAndCheckOnce(self,val = None,mousePos = None):
    def scanAndCheckOnce(self,dInputVal = None):#dInputVal 是一个字典，传递负载，鼠标坐标，和之类数据
        """2014/06/13	val是str,所以只需要关注字符串本身宽度传进来即可，不需要再计算字符串宽度,dInputVal的结构应该是 dIputVal ={'Val'='xxx','mousePos'=(x,y)}"""
        self.setMainStage(2)
        self.restartYxm()
        self.findEditTarget()
        #if val == None:
        if dInputVal == None:
            ramNo = random(int(self.snIn['Start']),int(self.snIn['End']))
            sendVal = self.snIn['prefix'] + ('%d' % ramNo).zfill(int(self.snIn['Len']))
            mousePos = self.posSetWidth14Line1
        else:
            pass
            #print(sendVal)
        #elif:
            #sendVal = dInputVal['prefix']+dInputVal['Val']
            #print(sendVal)
        #prefix = self.ourFactory['prefix']
        #print(prefix)
        #inputTextSn = sendVal
        #print(inputTextSn)
        self.sendOnce(self.handle,self.editArea,dInputVal['mousePos'],dInputVal['Val'])
        self.setMainStage(3)
        self.restartYxm()
        self.findEditTarget()
        self.sendOnce(self.handle,self.editArea,dInputVal['mousePos'],dInputVal['Val'])
        time.sleep(4)
        self.termTarget()		

    def scanAndCheckInRange(self,scanAndCheckOnceCallback = None):
        """2014/06/14	确定不去管数据来源，数据来源需要用sourceFilter()初始化，函数自动读取snIn来实现循环扫描和check。
		函数主要实现自动分辨snIn里面的数据类型，根据snIn的描述组装出对应的dIputVal.
		scanAndCheckOnceCallback 默认采用scanAndCheckOnce()，默认把组装好的dIputVal传入"""
        print("进入scanAndCheckInRange()")
        if scanAndCheckOnceCallback == None:
            scanAndCheckOnceCallback = self.scanAndCheckOnce
        dIputVal = {}
        if self.snIn['Type'] == '16':
            print("进入stbTpye16")
            #print(stbidStart,type(stbidStart))
            #print(stbidEnd,type(stbidEnd))
            dIputVal['mousePos'] = self.findMousePos(self.snIn['totalWidth'])
            for NextSn in range(self.snIn['Start'],self.snIn['End']):
                #print(NextSn,type(NextSn))
                dIputVal['Val'] = self.snIn['prefix']+('%X' % (NextSn)).zfill(self.snIn['Len'])
                print(dIputVal)
                #print(inTarget)
                #self.scanAndCheckOnce(dIputVal)
                scanAndCheckOnceCallback(dIputVal)
        if self.snIn['Type'] == '10':
            print("进入stbTpye10")
            dIputVal['mousePos'] = self.findMousePos(self.snIn['totalWidth'])  
            for NextSn in range(self.snIn['Start'],self.snIn['End']):
                dIputVal['Val'] = self.snIn['prefix']+('%X' % (NextSn)).zfill(self.snIn['Len'])
                print(dIputVal)
                scanAndCheckOnceCallback(dIputVal)
            pass
        else:
            print("不是16进制输入")

    def ourFactory_scanAndCheck_noEoc_InRange(self):
        """2014/06/13	主板生产的scan&check可以反复操作，所以和整机生产的scan&Check的操作函数有区别"""
        print("进入ourFactory_scanAndCheckInRange()")
        Lentgh = int(self.snIn['Len'])
        for NextSn in range(int(self.snIn['Start']),int(self.snIn['End'])):
            #print(NextSn,type(NextSn))
            inTarget = self.snIn['prefix']+('%d' % NextSn).zfill(Lentgh)
            print(inTarget,type(inTarget))
            

    def thirdPartFactory_scanAndCheckInRange(self):
        """2014/06/13	整机生产的scan&check会导致机顶盒重启，所以需要单独的函数操作机顶盒再次进入产测"""
        pass
        
    def findMousePos(self,width,valPos = None):#迫切需要一个自动计算输入宽度和鼠标位置的函数oriPointY = self.oriPosY,ciffX = self.cffctX
        """2014/06/13	设想是传一个序列号宽度的值进来，自动计算出需要鼠标点击的位置"""
        if valPos == None:
            posY = self.oriPosXY['oriPosY']
            posXcffct = self.oriPosXY['cffctX']
        #print('posY',type(posY),posY)
        #print('posXcffct',type(posXcffct),posXcffct)
        widthOp = width * posXcffct + 14
        #print(widthOp)
        self.posTarget = (widthOp,posY)
        #print(self.posTarget)
        return self.posTarget


    def sourceFilter(self,factorySelect = 1,manualSet = None):#1：ourfactory 2：thirdpartfactory 3：manualInput
        """2014/06/13	这个函数是处理xml读取的配置文件字典,并提供手动输入字典的方式。采用这个函数为scan/check准备数据"""
        print('This is sourceFilter()')
        if factorySelect == 1:# 预处理 ourfactory 自动扫描配置文件
            self.snIn['prefix'] = self.ourFactory['prefix']
            self.snIn['Start'] = int(self.ourFactory['start'])
            self.snIn['End'] = int(self.ourFactory['End'])
            self.snIn['Len'] = len(self.ourFactory['start'])
            self.snIn['Type'] = int(self.ourFactory['type'])
            self.snIn['totalWidth'] = int(self.ourFactory['totalWidth'])
            print(self.snIn)
        elif factorySelect == 2:# 预处理thirdPartfactory自动扫描配置文件
            self.snIn['prefix'] = self.thirdPartFactory['prefix']
            self.snIn['Start'] = int(self.thirdPartFactory['start'],16)
            self.snIn['End'] = int(self.thirdPartFactory['End'],16)
            self.snIn['Len'] = len(self.thirdPartFactory['start'])
            self.snIn['Type'] = int(self.thirdPartFactory['type'])
            self.snIn['totalWidth'] = int(self.thirdPartFactory['totalWidth'])
            print(self.snIn)
        elif factorySelect == 3:# 预处理手动输入的自动扫描配置文件
            try:
                if manualSet != None:
                    self.snIn['prefix'] = manualSet['prefix']
                    self.snIn['Start'] = int(manualSet['start'],16)
                    self.snIn['End'] = int(manualSet['End'],16)
                    self.snIn['Len'] = len(manualSet['start'])
                    self.snIn['Type'] = int(manualSet['type'])
                    self.snIn['totalWidth'] = int(self.manualSet['totalWidth'])
                    print(self.snIn)
                else:
                    print("factorySelect = 3 时需要设置第二个参数输入字典数据，包含：prefix、start、End、type、totalWidth数据，其中type必须为10 或16，指的是序列号采用10进制还是16进制，totalWidth是整个值长度，用于计算相对光标位置。")
            except:
                print("手动输入必须为字典数据，包含：prefix、start、End、type、totalWidth数据，其中type必须为10 或16，指的是序列号采用10进制还是16进制，totalWidth是整个值长度，用于计算相对光标位置。")
        else:
            print("只支持1：ourFactory；2：thirdPartFactory；3：manualSet")		
		
		
    def clickMouseAndEnter(self,coordinate):
        """2014/06/13	实现在指定Yxm相对坐标点击鼠标并按下回车键"""
        win32gui.SetForegroundWindow(self.handle) 
        win32api.SetCursorPos(coordinate)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0) 
        time.sleep(1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        #time.sleep(0.05)
        time.sleep(1)
        win32gui.PostMessage(self.editArea, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)






    def readYxmCfg(self):
        """这个程序用于读取YxmCfg.xml实现产测辅助程序的初始化配置"""
        int('0xEFCD',16)#=61389
        hex(61389)#='0xefcd'

    """
	查询对象状态
	"""
    def checkConnection(self):
        """2014/06/13
			实现检查Yxm连接状态，同时在无法检测连接状态时，清空对象网络状态信息
		"""
        try:
            s1 = win32gui.FindWindowEx(self.handle, None, 'Static', None)
            s2=win32gui.FindWindowEx(self.handle,s1, 'Static', None)
            s3=win32gui.FindWindowEx(self.handle,s2, 'Static', None)
            text=win32gui.GetWindowText(s3)
            #print("\n",text,"\n")
            if (text=="机顶盒已连接"):
                self.netStatus=0
            else:
                self.netStatus=-1
        except:
            print("\n找不到Yxm窗口.\n")
            self.netStatus = -1
            self.handle = -1
            self.isYxmOpen = 0
    def DiagnosisStatus(self):#用于打印对象窗口状态
        """2014/07/18
			打印对象状态
		"""
        print("\n-----DiagnosisStatus-----")
        if self.title == -1:
            print("当前没设置窗口标题")
        else:
            print("当前目标窗口名为：",self.title)
        if self.execPath == -1:
            print("当前对象没有设置工作路径")
        else:
            print("当前对象工作路径为：",self.execPath)
        if self.handle == -1 or self.handle ==0:
            print("当前没绑定产测窗口")
        else:
            print("当前绑定产测窗口句柄为： ",self.handle)
            self.checkConnection()
            if self.netStatus == -1:
                print("网络连接异常")
            else:
                print("网络连接正常")
        print("-----DiagnosisStatus-----\n")

    def isYxmExist(self):#查询目标Title的Yxm窗口是否存在
        """
		2014/06/11
			重写了该方法，采用查询目标Title的方式来判断是否Yxm窗口存在,同时可以完成Yxm窗口句柄赋值
		2014/08/13
			修补了如果self.title为数字时无法运行的bug，并增加返回值0：不存在，1：存在
		"""
        status = win32gui.FindWindow(None,str(self.title))
        isYxmExist = status
        if status == 0:
            self.isYxmOpen = 0
        else:
            self.isYxmOpen = 1
            self.handle = status
        return isYxmExist

    """查询对象状态"""

    """
	4.串口操作
	"""

    def openCom(self,bit_rate,conNo):
        """
		2014/08/19
			本意是用返回值来返回串口句柄，但是发现如果这样可能有时误操作会导致无法及时注销串口，所以增加全局串口对象来方便注销，实际操作最好还是用返回值赋值到某变量。
		"""
        serialport = serial.Serial(conNo,int(bit_rate),timeout=1)
        self.serialport = serialport
        return serialport

    def closeCom(self):
        self.serialport.close()
        self.serialport = -1

    def breakCfeToDiag(self):
        """
		2014/08/19
			1.实现了操作机顶盒在Diagnosis状态重启并再次进入Diagnosis
			2.需要留出com1来完成自动化操作
		"""
        if self.serialport == -1:
            self.openCom(115200,'com1')
        bctrlc = bytes(chr(0x03),'ascii')
        breboot = bytes('reboot\n\r','ascii')
        bapprun2 = bytes('apprun 2\n\r','ascii')
        self.serialport.write(breboot)
        time.sleep(1)
        n = 1
        while (n < 300):
            n += 1
            self.serialport.write(bctrlc)
            time.sleep(0.02)
        time.sleep(3)
        self.serialport.write(bapprun2)
        time.sleep(1)
        self.closeCom()


	
	

# 这里是测试代码
# 测试版本：产测测试辅助器1.0
# Author: Daine Huang
# Date: 2014/6/10
if __name__ == '__main__':

    menuPrint = "\n欢迎使用产测测试辅助器1.0x：\n\n1.初始化对象\n2.打印对象状态\n3.设置工作路径\n4.重设Title\n5.启动Yxm窗口并到对象\n6.检测连接状态\n7.设置工位\n8.scan\n0.关闭Yxm\n100.退出\n99.help list.\n"
    menuRang = {0,1,2,3,4,5,6,7,8,66,99,100}
    test1 = DiagnosisClass()
    test1.loadDiagnosisCfg()
    print(menuPrint)
    while (1):

        try:
            ctrl = int(input("请输入控制序号:"))
            if ctrl in menuRang:
                if ctrl == 1:#初始化对象
                    titleInit = input("输入Yxm Title 用于初始化测试对象(或直接回车为默认，留之后输入):\n")
                    if titleInit:
                        test1 = DiagnosisClass(str(titleInit))
                    else:
                        test1 = DiagnosisClass()
                        test1.loadDiagnosisCfg()

                elif ctrl == 2:#打印对象状态
                    try:
                        test1.DiagnosisStatus()
                    except:
                        print("\n对象尚未初始化.\n")
                elif ctrl == 3:#设置工作路径
                    try:
                        test1.setYxmPath()
                        #test1.execPath = path
                        #print(test1.execPath)
                    except:
                        print("\n对象尚未初始化.\n")
                elif ctrl == 4:#重设Title
                    try:
                        titleIn = input("\n输入标题并按回车:")
                        test1.setTitle(titleIn)
                        
                    except:
                        print("\nTitle设定失败！\n")
                elif ctrl == 5:#启动Yxm窗口并绑定到对象
                    try:
                        if test1.title == -1:
                            #titleIn = input("\n输入标题并按回车:")
                            test1.setTitle()
                        elif test1.isYxmOpen == 1:
                            test1.setTarget()
                            #retry = test1.setTarget()
                            #while retry == 4:
                                #retry = test1.setTarget()
                        elif test1.isYxmOpen == 0:
                            test1.accessYxm()
                        else:
                            print("启动Yxm失败！")
                    except:
                        print("\n对象尚未初始化.\n")
                elif ctrl == 6:#检测连接状态
                    try:
                        test1.checkConnection()
                    except:
                        print("\n请检查对象状态，检查连接状态需要启动Yxm.\n")
                elif ctrl == 7:#设置工位并重启Yxm
                    try:
                        test1.switchStage()
						#test1.stageSet = input("\n输入要设置的工位：")
                        #test1.setMainStage(test1.stageSet)
                        #test1.getPID()
                        #test1.killProc()
                        #time.sleep(1)
                        #test1.accessYxm()						
                    except:
                        print("\n请检查对象状态，设置工位需要绑定工作路径和对象Title.\n")
                elif ctrl == 8:#自动发送scan
                    try:
                        ifRandom = input("\n是否产生随机数？Yes/No:")
                        if ifRandom == "Yes" or ifRandom == "yes" or ifRandom == '1':
                            ifRandom = True
                        else:
                            ifRandom = False
                        print(ifRandom)
                        ifThirdPartNo = input("\n是否是第三方生产？Yes/No:")
                        if ifThirdPartNo == "Yes" or ifThirdPartNo == "yes" or ifRandom == '1':
                            ifThirdPartNo = True
                        else:
                            ifThirdPartNo = False
                        print(ifThirdPartNo)
                        test1.autoSendStbid(ifRandom,ifThirdPartNo)
                    except:
                        print("没有找到编辑区域!\n")
                elif ctrl == 0:#关闭Yxm
                    try:
                        test1.accessYxm()
                        test1.getPID()
                        test1.killProc()
                    except:
                        print("没有找到关闭目标！\n")

                elif ctrl == 66:#测试代码入口
                    try:
                        #test1.setTitle()
                        #test1.scanAndCheckOnce()
                        #test1.scanAndCheckInRange()
                        #test1.sourceFilter()
                        #test1.ourFactory_scanAndCheckInRange()
                        suffx1 = input("输入后缀")
                        test1.renameYxmLogfile(suffx1)
                        """
						#print(test1.execPath[0],"+",test1.execPath[1])
                        #print(test1.execPath)
                        tmpPath = test1.execPath
                        print(tmpPath)
                        tmpPath1 = tmpPath
                        tmpPath2 = tmpPath
                        tmpPath1 = tmpPath1.encode('gb2312') 
                        tmpPath2 = tmpPath2.encode('UTF-8')
                        print(tmpPath1)
                        print(tmpPath2)
                        #str(tmpPath)
                        #tmpPath

                        
                        print(test1.index,test1.execTarget,test1.execPath)
                        index = input("改变index，输入数字：")
                        test1.index = index
                        """
                    except:
                        print("\n对象尚未初始化.\n")
                elif ctrl == 100:#退出该程序
                    try:
                        test1.termTarget()
                        del test1
                    except:
                        pass
                    print("\n退出产测测试辅助器。\n")
                    break
                elif ctrl == 99:#帮助菜单
                    print(menuPrint)
#                print(ctrl+1)
            else: print("Out of Range.\n")
        except:
            ctrl = -1
            print("Nothing input.")
    #input('\n按任意键关闭窗口。\n')

