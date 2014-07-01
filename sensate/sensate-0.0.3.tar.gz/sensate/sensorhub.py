from datetime import datetime
import json

from sensorcheck import SensorCheck
from utils import CustomJsonEncoder, CustomJsonDecoder

# TODO: make equipment swappable (when more equipment presents itself)
from equipment.wsg30 import get_sensor_oid
from equipment.wsg30 import BATTERY_TROUBLE, BATTERY_OK, BATTERY_LOW
from transports.snmp import SNMPobject

# MAX_SENSORS_PER_HUB restricts SNMP guesswork to a reasonable level.
# (theoretical max # of sensors per WSG30 hub = 30 wireless + 1 Power + 1 Battery.)
MAX_SENSORS_PER_HUB = 32 


class SensorHub(object):
    '''The central communications hub that sensors report back to. 

    Uses SNMP to poll the hub directly over the network. 
    
    Required argument:  
    
    hostname                -- (string) fqdn or LAN-routable hostname (no protocol prefix)
    
    Optional keyword arguments:
    
    match           -- (string) restrict results to only those sensors with `match` in their name
    auto            -- (bool) whether to perform SNMP connections immediately (default: True)
    port            -- (int) port used to connect via snmp (default: 161)
    timeout         -- (int or float) time in seconds to wait for SNMP response.
    retries			-- (int) number of times to retry connection (default: 0)
    snmp_method     -- (string) if pysnmp isn't working for you, try 'cli' (default: 'pysnmp')
    
    Currently decoration-only attributes that can be set by keyword arguments:
    
    model           -- (string) defines model of Sensaphone equipment (default: WSG30)
    ''' 
    
    def __init__(self, hostname, **kwargs):
        '''
        Constructor for SensorHub.

        Uses SNMP to poll the hub directly over the network.
           
        Supply "match" to restrict results to only those sensors
        with "match" in their name.

        :param hostname: (required) fqdn or reachable local hostname.
        :param match: (optional) only load sensors where match (string) can be found in name.
        '''
    
        self.hostname = hostname        
        self.match = kwargs.get('match', '')
        self.model = str(kwargs.get('model', 'WSG30')).upper()
        
        # whether to complete SNMP checks immediately
        auto = kwargs.get('auto', True)
        
        ## SNMP ##
        self.snmp_method = kwargs.get('snmp_method', 'pysnmp')
        self.retries = kwargs.get('retries', 0)
        # generic timeout length in seconds for any type of connection.
        self.timeout = kwargs.get('timeout', 10)  
        
        # Updated every time snmp_check_sensors used.
        self.lastchecktime = None

        # Assign self.snmp_get to a generated snmp get function.  
        self.snmp_get = SNMPobject(hostname=self.hostname, timeout=self.timeout,
            			retries=self.retries, method=self.snmp_method).snmp_getter()

        self.sensors_by_idx = {}   # idx: name mapping. Filled during discover()
        self.checks_by_idx = {}    # idx: SensorCheck mapping. Filled during check()
        self.checks_by_serial = {} # serial: SensorCheck mapping. Filled during check()
        self.checks = []

        if auto:
            self.reload()

    def check(self):
        '''Populates and returns self.checks by retrieving SensorCheck objects via SNMP (destructive update)
        
        Also sets up self.checks_by_idx (idx to SensorCheck mapping) and self.checks_by_serial
        (they have both been useful in different contexts, so let's have both.)
        ''' 
        self.checks = []
        self.checks_by_idx = {}
        self.checks_by_serial = {}
        
        for idx in self.sensors_by_idx.keys():
            checktime = datetime.utcnow()
            check = SensorCheck.from_snmp(self.hostname, idx, name=self.sensors_by_idx[idx], checktime=checktime)
            self.checks.append(check)
            self.checks_by_idx[idx] = check
            # ignore Power and Battery for checks_by_serial mapping.
            if check.serial != '0':
                self.checks_by_serial[check.serial] = check

    def discover(self):
        '''Populates and returns self.sensors_by_idx (destructive update)
        
        :rtype: dictionary mapping of sensor index (int) to name (str) 
        '''
        self.sensors_by_idx = {} 
        self.lastchecktime = datetime.utcnow()
        
        for idx in range(MAX_SENSORS_PER_HUB+1):
            name = self.snmp_get(get_sensor_oid(idx, 'name'))
            # we sometimes get garbage characters in the sensor name :(
            try:
                name.decode()
            except UnicodeDecodeError, e:
                #TODO: CONVERT name (don't just give up on it)
                #logger.debug(e)
                continue
            except AttributeError, e:
                # name was returned as None
                #logger.debug(e)
                continue

            if self.match:
                if self.match in name:
                    self.sensors_by_idx[idx] = name
            else:
                if name and name != 'Unconfigured':
                    self.sensors_by_idx[idx] = name
        return self.sensors_by_idx
           
    def get_alarms(self, attr='serial'):
        '''returns dictionary of calculated alarms based on each sensor's reported
        alarmhigh, alarmlow, and battery_status conditions.
        
        Does NOT include hub's built-in Battery and Power items.
        
        :param attr: attribute taken from SensorCheck to record alarm state [default: serial]
        '''
        alarms = {'high': [], 'low': [], 'low_battery': [], 'trouble': [] }
        
        for check in self.checks_by_serial.values():
            if check.measurement > check.alarmhigh:
                alarms['high'].append(getattr(check, attr))
            elif check.measurement < check.alarmlow:
                alarms['low'].append(getattr(check, attr))

            if check.battery_status == BATTERY_LOW:
                alarms['low_battery'].append(getattr(check, attr))
            elif check.battery_status == BATTERY_TROUBLE:
                alarms['trouble'].append(getattr(check, attr))
        return alarms

    def reload(self):
        '''Convenience interface to self.discover() and self.check()'''
        self.discover()
        self.check()
    
    def __str__(self):
        out = 'Sensaphone Hub at %s\n\n' % self.hostname
        for idx in sorted(self.sensors_by_idx.keys()):
            out += '%d: %s\n' % (idx, self.sensors_by_idx[idx])
        return out
    
    def to_dict(self, by_idx=False):
        '''returns dictionary representing hub and all checked sensors.
        
        if self.check() has successfully run, the 'sensors' key will have 
        self.checks_by_serial as its value, or self.checks_by_idx if by_idx=True.
        
        if only self.discover() has run, the 'sensors' key = self.sensors_by_idx
        '''
        
        if self.checks_by_idx:
            if by_idx:
                sensord = dict([(k,v.to_dict()) for k,v in self.checks_by_idx.items()])
            else:
                sensord = dict([(k,v.to_dict()) for k,v in self.checks_by_serial.items()])
            alarms = self.get_alarms('idx' if by_idx else 'serial')
        else:
            alarms = {}
            sensord = self.sensors_by_idx

        return { 'hostname': self.hostname,
                 'lastchecktime': self.lastchecktime,
                 'match': self.match,
                 'model': self.model,
                 'sensors': sensord,
                 'alarms': alarms
               }

    def to_json(self):
        return json.dumps(self.to_dict(), cls=CustomJsonEncoder)
