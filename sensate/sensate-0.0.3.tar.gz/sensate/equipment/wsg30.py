__doc__='''The SensaphoneRecord object encapsulates the historical records 
currently stored on the Sensaphone device.

This object assists in populating historical records of sensor values.

The input data structure is a comma-separated CSV containing records for either a single 
selected sensor or for all sensors.  (see below copied from the Sensaphone WSG30 manual)

From there, we construct SensorCheck objects which can be converted to 

    # dict of SensorCheck objects (similar to SensorHub.sensor_check attribute)

The challenge here is that the sensaphone stores data based on the POSITION ("idx")
of the sensors on the device in its internal reckoning. Therefore the records don't 
provide a contiguous record of monitoring in real-world terms -- we have to piece
that back together ourselves.
'''

### SNMP helpers used by hub.py and sensor.py

# Magic SNMP number for Sensaphone WSG30, used in constructing Object IDs for sensor value lookups.
SENSAPHONE_OIDBASE = '.1.3.6.1.4.1.8338.1.1.4.1.1'

SENSOR_DATA_MAP = { 'name': 15, 
                    'units': 19,
                    'alarmlow': 11,
                    'alarmhigh': 12,
                    'measurement': 48,
                    'warnlow': 74,              # STRING: "3.7C"   ?? warn at low value ?? 
                    'warnhigh': 75,             # STRING: "7.6C"   ?? warn at high value ?? 
                    'battery_status': 91,       # STRING: "OK" or "Low Battery" or "Trouble"
                    'measurement_type': 92,     # STRING: 'Temp 2.8k C' or other type.  
                    'battery_level': 93,        # STRING: "4.5"     ?? battery level ??
                    'lastalarm': 98,            # STRING: "3/3/2014 1:31:14am"
                    'serial': 35,               # STRING: "13500" 
                  }

BATTERY_TROUBLE = 'Trouble'
BATTERY_OK = 'OK'
BATTERY_LOW = 'Low Battery'

def get_sensor_oid(idx, datum=''):
    '''Returns OID for individual sensor (or, if `datum` supplied, the named data point for 
    sensor) at index `idx`.  Uses global SENSAPHONE_OIDBASE to construct and return full OID.
    
    Named data points:
    
    %r

    :param idx: (required) the "index" (1-32) of the sensor on the hub.
    :param datum: (optional) 
    :return oid (string) allowing retrieval of named data point.
    ''' % SENSOR_DATA_MAP

    if datum:
        return '%s.1.%i.%i' % (SENSAPHONE_OIDBASE, idx, SENSOR_DATA_MAP[datum])
    else:
        return '%s.1.%i' % (SENSAPHONE_OIDBASE, idx)

