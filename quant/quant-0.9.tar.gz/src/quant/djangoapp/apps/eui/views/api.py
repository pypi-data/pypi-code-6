from dm.view.api import ApiView

# Todo: Setup quant roles (market analyst, quant analyst, trader, auditor). 

class QuantApiView(ApiView):

    apiKeyHeaderName = 'X-Quant-API-Key'


def api(request):
    view = QuantApiView(request=request)
    return view.getResponse()
