from Pyro4 import Daemon,Proxy
from Pyro4.core import DaemonObject
from select import select

class summon(object):
    def __init__(self,name):
        self.name=name
        self.box=None
        self.func1=None
        self.func2=None
        self.func3=None
    def terror(self,arg):
        "to execute code in daemon script"
        try:
            exec(arg)
        except Exception as e:
            print "Error",e
            print arg
    def update(self,space,display=False):
        self.box=space
        if display==True:
            print "storing:",self.name,"data:",self.box
    def get(self,display=False):
        if display==True:
            print "throwing:",self.name,"data:",self.box
        return self.box
    def check(self):
        print '"'+self.name+'"',"container"
        print "data:",self.box


def evoc(names,host="localhost",port=30238,unixsocket=None, nathost=None, natport=None):
    __LEGION={}
    if host!="localhost":
        host1="_{0}_".format(host)
    else:
        host1="_"
    for i in names:
        globals()[i]=summon(i)
        __LEGION.update({i:globals()[i]})
    globals()["{0}{1}Efreet".format(host1,port)]=Daemon(host,port,unixsocket,nathost,natport)
    __LEGION.update({"DEMON{0}{1}".format(host1,port):["DEMON{0}{1}".format(host1,port),names,host,port,unixsocket,nathost,natport,globals()["{0}{1}Efreet".format(host1,port)]]})
    return __LEGION

def invoc(i,port=30238,hostname="localhost"):
    spirit=[]
    for g in i:
        print g
        ana="PYRO:"+str(g)+"@"+str(hostname)+":"+str(port)
        spirit.append(Proxy(ana))
    return dict(zip(i,spirit))

####DEAD MULTIPLEX VERS
def evoken(n):
    for b in n:
        for c in range(0,len(b[1])):
            uri=b[7].register(globals()["{0}".format(b[1][c])],objectId="{0}".format(b[1][c]))
            print uri
    while 1==1:
        for b in n:
            global _nanners
            _nanners=datetime.now()
            def Func():
                if datetime.now()-_nanners>timedelta(milliseconds=2):
                    return 0
                else:
                    return 1
            b[7].requestLoop(loopCondition=lambda: Func())

def conjure(n):
    for b in n:
        for c in range(0,len(b[1])):
            uri=b[7].register(globals()["{0}".format(b[1][c])],objectId="{0}".format(b[1][c]))
            print uri
    #Benchmarking
    #nem=datetime.now()
    while 1:
        for b in n:
            sin,sout,sex=select(b[7].sockets,[],[],0)
            for s in sin:
                b[7].events([s])
                break
        #if datetime.now()-nem>timedelta(seconds=15):
        #    break
        #    global cb
        #    cb+=1
        #if (datetime.now())-dtp>(timedelta(seconds=15)):
        #    print cb
        #    global vw
        #    vw=1
        #    print "done"
        #if vw==1:
        #    break

