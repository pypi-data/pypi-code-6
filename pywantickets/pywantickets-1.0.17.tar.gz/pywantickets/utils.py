import json
import decimal
from datetime import datetime
from pywantickets import WanticketsModel


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

def parse_wt_dtime(string):
    return datetime.strptime(string, '"%Y-%m-%dT%H:%M:%SZ"')

def parse_wt_date(string):
    try:
        return datetime.utcfromtimestamp(
            int(string.replace("/Date(", '').replace(')/', '')) / 1000
        )
    except:
        return None
