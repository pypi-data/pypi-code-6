import json
import decimal
from datetime import datetime
from pywantickets import WanticketsModel

long_time_zones_map = {
    "Pacific Daylight Time": "PDT",
    "Pacific Standard Time": "PST",
    "Mountain Daylight Time": "MDT",
    "Mountain Standard Time": "MST",
    "Central Daylight Time": "CDT",
    "Central Standard Time": "CST",
    "Eastern Daylight Time": "EDT",
    "Eastern Standard Time": "EST",
    "Alaska Daylight Time": "AKDT",
    "Alaska Standard Time": "AKST",
    "Hawaii-Aleutian Daylight Time": "HADT",
    "Hawaii-Aleutian Standard Time": "HAST",
    "Hawaii Standard Time": "HST",
}

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)

def to_json(tree):
    return json.dumps(tree,
    	cls=DecimalEncoder, default=make_serializable)

def make_serializable(o):
    if isinstance(o, WanticketsModel):
    	return o.get_api_model()
    else:
    	return o

def parse_wt_dtime(string, timezone_name=None):
    if string is None or string == '':
        return None

    clean_date = string.replace('"', '').replace('T', ' ')[:-1]
    #clean_date = clean_date + long_time_zones_map.get(timezone_name, ' -0700')
 
    return datetime.strptime(clean_date, '%Y-%m-%d %H:%M:%S')

def parse_wt_date(string):
    return datetime.utcfromtimestamp(
        int(string.replace("/Date(", '').replace(')/', '')) / 1000
    )
