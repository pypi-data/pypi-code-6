class ClientDataMiddleware(object):
    def process_request(self, request):
        request.client_data = {}
