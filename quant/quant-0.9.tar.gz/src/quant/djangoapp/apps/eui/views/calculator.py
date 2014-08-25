from quant.djangoapp.apps.eui.views.base import QuantView

class CalculatorView(QuantView):

    templatePath = 'calculator'
    majorNavigationItem = '/calculator/'
    minorNavigationItem = '/calculator/'

    def __init__(self, **kwds):
        super(CalculatorView, self).__init__(**kwds)

    def setMinorNavigationItems(self):
        self.minorNavigation = [
            {'title': 'Calculator', 'url': '/calculator/'},
        ]

    def canAccess(self):
        return self.canReadSystem()

    def setContext(self, **kwds):
        super(CalculatorView, self).setContext(**kwds)
        self.context.update({
        })


def calculator(request):
    view = CalculatorView(request=request)
    return view.getResponse()
 
