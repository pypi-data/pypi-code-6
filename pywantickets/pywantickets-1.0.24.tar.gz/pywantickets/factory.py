import pywantickets.client as wt_clients

def create_wt_client(name="search", auth_code=None,
					 username=None, password=None):
	if name == "search":
		return wt_clients.WanticketsSearchClient()
	elif name == "purchase":
		return wt_clients.WanticketsPurchaseClient(
			username=username,
			password=password,
			auth_code=auth_code,
		)
