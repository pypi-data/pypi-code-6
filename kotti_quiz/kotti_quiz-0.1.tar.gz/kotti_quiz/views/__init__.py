class BaseView(object):
    """BaseView"""

    def __init__(self, context, request):

        super(BaseView, self).__init__()
        self.context = context
        self.request = request
