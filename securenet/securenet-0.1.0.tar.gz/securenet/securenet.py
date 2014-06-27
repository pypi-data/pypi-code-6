import requests
import datetime
import json
import re

_locals = {}

def configure(id, key, url="https://gwapi.demo.securenet.com/api/"):
	_locals['id'] = str(id)
	_locals['key'] = str(key)
	_locals['url'] = url
	_locals['auth'] = (_locals['id'], _locals['key'])


################################################################################
# JSON Utilities
################################################################################

_camel_pat = re.compile(r'([A-Z])')
_under_pat = re.compile(r'_([a-z])')

def _camel_to_underscore(name):
	return _camel_pat.sub(lambda x: '_' + x.group(1).lower(), name)

def _underscore_to_camel(name):
	return _under_pat.sub(lambda x: x.group(1).upper(), name)

def _date_hook(json_dict):
    for (key, value) in json_dict.items():
        try:
            json_dict[key] = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
        except:
            pass
    return json_dict

def _convert_json(obj, convert):
	if isinstance(obj, list):
		new_l = []
		for value in obj:
			if isinstance(value, dict):
				new_l.append(_convert_json(value, convert))
			elif isinstance(i, list):
				new_l.append(_convert_json(value, convert))
			else:
				new_l.append(value)
		return new_l
	new_d = {}
	for key, value in obj.iteritems():
		if isinstance(value, dict):
			new_d[convert(key)] = _convert_json(value, convert) 
		elif isinstance(value, list):
			new_d[convert(key)] = _convert_json(value, convert)
		else:
			new_d[convert(key)] = value
	return new_d

def _json_load(text):
	dict = json.loads(text, object_hook=_date_hook)
	return _convert_json(dict, _camel_to_underscore)

def _json_dump(dict):
	dict = _convert_json(dict, _underscore_to_camel)
	return json.dumps(dict)


################################################################################
# Socket Utilities
################################################################################

_headers = {'content-type': 'application/json'}

def _error(message):
	r = {}
	r['success'] = false
	r['message'] = message
	r['result'] = 'COMMUNICATION_ERROR'
	return r

def _post(path, payload):
	url = _locals['url'] + path
	data = _json_dump(payload)
	r = requests.post(url, auth=_locals['auth'], data=data, headers=_headers)
	return _json_load(r.text)

def _put(path, payload):
	url = _locals['url'] + path
	data = _json_dump(payload)
	r = requests.put(url, auth=_locals['auth'], data=data, headers=_headers)
	return _json_load(r.text)

def _delete(path, payload):
	url = _locals['url'] + path
	data = _json_dump(payload)
	r = requests.delete(url, auth=_locals['auth'], data=data, headers=_headers)
	return _json_load(r.text)

def _get(path):
	url = _locals['url'] + path
	r = requests.get(url, auth=_locals['auth'], headers=_headers)
	return _json_load(r.text)


################################################################################
# Batch Processsing
################################################################################

def get_batch(batchId="Current"):
	return _get("batches/" + str(batchId))

def get_current_batch():
	return get_batch()

def close_batch():
	return _post("batches/Close")


################################################################################
# Transaction Processing
################################################################################

def authorize(req):
	return _post("Payments/Authorize", req)

def capture(req):
	return _post("/Payments/Capture", req)

def charge(req):
	return _post("/Payments/Charge", req)


################################################################################
# Vault
################################################################################

def create_customer(req):
	return _post("/Customers", req)

def get_customer(req):
	if isinstance(req, dict):
		if 'customer_id' in req:
			customer_id = str(req['customer_id'])
		else:
			return _error("customer_id is required")
	else:
		customer_id = str(req)
	return _get("/Customers/" + customer_id)

def update_customer(req):
	if 'customer_id' in req:
		customer_id = str(req['customer_id'])
	else:
		return _error("customer_id is required")
	return _put("/Customers/" + customer_id, req)

def create_customer_payment_method(req):
	if 'customer_id' in req:
		customer_id = str(req['customer_id'])
	else:
		return _error("customer_id is required")
	return _post("/Customers/" + customer_id + "/PaymentMethod", req)


def get_customer_payment_method(req):
	if 'customer_id' in req:
		customer_id = str(req['customer_id'])
	else:
		return _error("customer_id is required")
	if 'payment_method_id' in req:
		payment_method_id = str(req['payment_method_id'])
	else:
		return _error("payment_method_id is required")
	return _get("/Customers/" + customer_id + "/PaymentMethod/" + payment_method_id)


def delete_customer_payment_method(req):
	if 'customer_id' in req:
		customer_id = str(req['customer_id'])
	else:
		return _error("customer_id is required")
	if 'payment_method_id' in req:
		payment_method_id = str(req['payment_method_id'])
	else:
		return _error("payment_method_id is required")
	return _delete("/Customers/" + customer_id + "/PaymentMethod/" + payment_method_id)


################################################################################
# Installment Plans
################################################################################

def create_installment_plan(req):
	if 'customer_id' in req:
		customer_id = str(req['customer_id'])
	else:
		return _error("customer_id is required")
	return _post("/Customers/" + customer_id + "/PaymentSchedules/Installment", req)

def create_variable_plan(req):
	if 'customer_id' in req:
		customer_id = str(req['customer_id'])
	else:
		return _error("customer_id is required")
	return _post("/Customers/" + customer_id + "/PaymentSchedules/Variable", req)

def create_recurring_plan(req):
	if 'customer_id' in req:
		customer_id = str(req['customer_id'])
	else:
		return _error("customer_id is required")
	return _post("/Customers/" + customer_id + "/PaymentSchedules/Recurring", req)

def get_plan(req):
	if 'customer_id' in req:
		customer_id = str(req['customer_id'])
	else:
		return _error("customer_id is required")
	if 'plan_id' in req:
		plan_id = str(req['plan_id'])
	else:
		return _error("plan_id is required")
	return _get("/Customers/" + customer_id + "/PaymentSchedules/" + plan_id)
	
def delete_plan(req):
	if 'customer_id' in req:
		customer_id = str(req['customer_id'])
	else:
		return _error("customer_id is required")
	if 'plan_id' in req:
		plan_id = str(req['plan_id'])
	else:
		return _error("plan_id is required")
	return _delete("/Customers/" + customer_id + "/PaymentSchedules/" + plan_id)


################################################################################
# Credits
################################################################################

def credit(req):
	return _post("/Payments/Credit", req)


################################################################################
# Refunds and Voids
################################################################################

def refund(req):
	if isinstance(req, dict):
		if 'transaction_id' in req:
			obj = dict
		else:
			return _error("transaction_id is required")
	else:
		obj = { "transaction_id" : req }
	return _post("/Payments/Refund", obj)

def void(req):
	if isinstance(req, dict):
		if 'transaction_id' in req:
			obj = dict
		else:
			return _error("transaction_id is required")
	else:
		obj = { "transaction_id" : req }
	return _post("/Payments/Void", obj)


################################################################################
# Transactions
################################################################################

def get_transactions(req):
	if isinstance(req, dict):
		return _post("/Transactions/Search", req)
	return _get("/Transactions/" + str(req))

def get_transaction(req):
	if isinstance(req, dict):
		if 'transaction_id' in req:
			transaction_id = str(req['transaction_id'])
		else:
			return _error("transaction_id is required")
	else:
		transaction_id = str(req)
	return _get("/Transactions/" + transaction_id)

def update_transaction(req):
	if 'reference_transaction_id' in req:
		reference_transaction_id = str(req['reference_transaction_id'])
	else:
		return _error("reference_transaction_id is required")
	return _put("/Transactions/" + reference_transaction_id, req)
