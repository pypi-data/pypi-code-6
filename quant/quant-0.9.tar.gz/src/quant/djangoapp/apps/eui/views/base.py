import quant.djangoapp.settings.main
from dm.view.base import SessionView

class QuantView(SessionView):

    majorNavigation = []

    def __init__(self, *args, **kwds):
        super(QuantView, self).__init__(*args, **kwds)

    def setMajorNavigationItems(self):
        self.majorNavigation = [
            {'title': 'Home', 'url': '/'},
            {'title': 'Codes', 'url': '/codes/'},
            {'title': 'Markets', 'url': '/symbols/'},
            {'title': 'Images', 'url': '/images/'},
            {'title': 'Books', 'url': '/books/'},
            {'title': 'Trades', 'url': '/trades/'},
            {'title': 'Results', 'url': '/results/'},
        ]

