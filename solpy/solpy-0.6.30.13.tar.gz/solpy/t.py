import pv
import json

def test_virr1():
    import datetime
    p1 = """{"system_name":"HAPPY CUSTOMER",
    "address":"15013 Denver W Pkwy, Golden, CO",
    "zipcode":"80401",
    "phase":1,
    "voltage":240,
    "array":[
        {"inverter":"Enphase Energy: M215-60-2LL-S2x-IG-NA (240 V) 240V",
        "panel":"Mage Solar : Powertec Plus 250-6 PL",
        "quantity":20,
        "azimuth":180,
        "tilt":25
        }
        ]}"""
    plant = pv.jsonToSystem(json.loads(p1))
    ts =datetime.datetime(2000,9,22,19)
    print ts
    weatherData = {}
    weatherData['temperature'] = 25
    weatherData['windSpeed'] = 0
    rs = plant.virr(2000,ts, weatherData)
    print rs

test_virr1()
