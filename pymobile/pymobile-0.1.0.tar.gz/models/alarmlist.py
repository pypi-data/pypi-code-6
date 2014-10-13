import time

alarmlist = [  
    [time.ctime(time.time() - 6000),"ID1", "Område, +TAG=OM-LS1 Feil.", 1],
    [time.ctime(time.time() - 600), "ID2", "Område, +TAG=OM-LS2 Feil.", 2],
    [time.ctime(),                  "ID3", "Område, +TAG=OM-LS3 Feil.", 3]
    ]

alarms = list()

class Alarm(object):
    def __init__(self,time, id, desc, stat):
        self.time = time
        self.id = id
        self.desc = desc
        self.stat = stat
    
    active = property(lambda self: self.stat == 1 or self.stat == 2 )
    active_unack = property(lambda self: self.stat == 1)
    active_ack = property(lambda self: self.stat == 2)
    inactive_unack = property(lambda self: self.stat == 3)
    inactive_ack = property(lambda self: self.stat == 0)
    
# Legger til kolonne for status
for al in alarmlist:
    alarms.append(Alarm(*al))

def getAlarms():
    return alarms
