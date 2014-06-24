import pywantickets.client as wt_clients

def create_wt_client(name="search", api_token=None,
					 username=None, password=None):
	if name == "search":
		return wt_clients.WanticketsSearchClient()
	elif name == "purchase":
		return wt_clients.WanticketsPurchaseClient(
			username=username,
			password=password
		)
