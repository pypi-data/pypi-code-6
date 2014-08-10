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
    def terror(self,arg,display=False):
        if display==True:print arg
        "to execute code in daemon script"
        try: exec(arg)
        except Exception as e:print "Error",e,"\n",arg
    def deliver(self):pass
    def update(self,space,display=False):
        self.box=space
        if display==True:print "storing:",self.name,"data:",self.box
    def get(self,display=False):
        if display==True:print "throwing:",self.name,"data:",self.box
        return self.box
    def check(self):
        print '"'+self.name+'"',"container","\n","data:",self.box

__DEMON1993_1Efreet1=[]
def evoc(names,host="localhost",port=30238,unixsocket=None, nathost=None, natport=None):
    d=Daemon(host,port,unixsocket,nathost,natport)
    locals()["{0}{1}Efreet".format(host,port)]=d
    for i in names:
        locals()[i]=summon(i)
        uri=locals()["{0}{1}Efreet".format(host,port)].register(locals()[i],i)
        print uri
    __DEMON1993_1Efreet1.append(["DEMON{0}{1}".format(host,port),names,host,port,unixsocket,nathost,natport,locals()["{0}{1}Efreet".format(host,port)]])
    return {"__DEMON1993_1Efreet1":__DEMON1993_1Efreet1}

__spirit={}
def invoc(i,port=30238,hostname="localhost"):
    for g in i:
        locals()[g]=Proxy("PYRO:"+str(g)+"@"+str(hostname)+":"+str(port))
        print locals()[g]
        __spirit.update({g:locals()[g]})
    return __spirit

def conjure():
    while 1:
        map(lambda b: map(lambda s:b[7].events([s]),select(b[7].sockets,[],[],0)[0]),__DEMON1993_1Efreet1)