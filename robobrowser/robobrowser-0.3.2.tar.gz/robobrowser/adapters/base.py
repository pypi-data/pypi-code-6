

class BaseAdapter(object):

    def __init__(self):
        self.browsers = []


class RateLimitAdapter(BaseAdapter):

    def __init__(self, predicate):
        super(RateLimitAdapter, self).__init__()
        self.predicate = predicate

    def register(self, browser):
        pass


class DelayRateLimitAdapter(RateLimitAdapter):

    def __init__(self, delay):
