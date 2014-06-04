import json
import decimal
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