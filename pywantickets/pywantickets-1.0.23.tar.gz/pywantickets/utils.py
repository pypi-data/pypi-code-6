import json
import decimal
from datetime import datetime, timedelta, tzinfo
from pywantickets import WanticketsModel

long_time_zones_map = {
    "Pacific Daylight Time": "PDT",
    "Pacific Standard Time": "PST",
    "Mountain Daylight Time": "MDT",
    "Mountain Standard Time": "MST",
    "US Mountain Standard Time": "MST",
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

time_zones_offsets = {
    'EDT': -4,
    'EST': -5,
    'CDT': -5,
    'CST': -6,
    'MDT': -6,
    'MST': -7,
    'PDT': -7,
    'PST': -8,
    'AKDT': -8,
    'AKST': -9,
    'HADT': -9,
    'HAST': -10,
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

    clean_date = string.replace('"', '')
    the_date = datetime.strptime(clean_date, '%Y-%m-%dT%H:%M:%SZ')

    if not timezone_name is None:
        timezone = long_time_zones_map.get(timezone_name)
        offset = time_zones_offsets.get(timezone, 0)
        if offset < 0:
            return the_date - timedelta(hours=abs(offset))
        else:
            return the_date + timedelta(hours=offset)
    
    return the_date
        

def parse_wt_date(string):
    return datetime.utcfromtimestamp(
        int(string.replace("/Date(", '').replace(')/', '')) / 1000
    )
