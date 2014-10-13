import time
from pymobile import shared
from queue import Queue

alarmlist = [  
    [time.ctime(),                      "ID1", "Område, +TAG=OM-LS1 Feil.", 1],
    [time.ctime(time.time() - 600),     "ID2", "Område, +TAG=OM-LS2 Feil.", 3],
    [time.ctime(time.time() - 700),     "ID3", "Område, +TAG=OM-LS3 Feil.", 1],
    [time.ctime(time.time() - 900),     "ID4", "Område, +TAG=AR-PS1 Feil.", 3],
    [time.ctime(time.time() - 6000),    "ID5", "Område, +TAG=AR-PS2 Feil.", 1],
    [time.ctime(time.time() - 8000),    "ID6", "Område, +TAG=AR-PS3 Feil.", 3]
    ]


alarms = dict()
trash = dict()

def getAlarms():
    return alarms.values()

alarm_queues = []

def get_alarmqueue():
    newq = Queue()
    alarm_queues.append(newq)
    return newq

def remove_alarmqueue(oldq):
    alarm_queues.remove(oldq)


class Alarm(object):
    def __init__(self,time, id, desc, state):
        self.s_time = time
        self.id = id
        self.dpe = id
        self.desc = desc
        self.update(state)
        
    def update(self, state, add=False, remove=False):
        if add:
            self.table = "add"
        elif remove:
            self.table = "remove"
        else:
            self.table = "update"
        
        self.state = state
        if state == 1:
            self.s_state = 'Aktiv / ikke kvittert !!'
            self.s_state_color = '#AA0000'
        elif state == 2:
            self.s_state = 'Aktiv / kvittert'
            self.s_state_color = '#AA0000'
        elif state == 3:
            self.s_state = 'Ikke aktiv / ikke kvittert !!'
            self.s_state_color = '#0000AA'
        else:
            self.s_state = 'Ikke aktiv.'
            self.s_state_color = '#000000'
    

# Legger til kolonne for status
with shared.lock:
    for al in alarmlist:
        alarms[al[1]] = (Alarm(*al))

    alarm_sim = list(alarms.keys())

@shared.worker
def alarm_simulator_worker():
    while not shared.stop.wait(3):
        with shared.lock:
            for id in alarm_sim:
                if id in alarms:
                    a = alarms[id]
                    if a.state == 0 or a.state == 2:
                        a.update(0, remove=True)
                        for q in alarm_queues:
                            q.put_nowait([a.__dict__])
                        trash[id] = alarms.pop(id)
                else:
                    if id in trash:
                        a = trash.pop(id)
                        a.update(1, add=True)
                        a.s_time = time.ctime()
                        alarms[id] = a
                        for q in alarm_queues:
                            q.put_nowait([a.__dict__])
                            
    for q in alarm_queues:
        q.put_nowait(None)
                            
                            
def ack_alarm(id):
    with shared.lock:
        if id in alarms:
            a = alarms[id]
            a.update( (a.state + 1) % 4)
            for q in alarm_queues:
                q.put_nowait([a.__dict__])
            
            