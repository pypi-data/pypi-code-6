from livefyre.src.api.personalizedstream import PersonalizedStream


class TimelineCursor(object):
    def __init__(self, core, resource, limit, date):
        self.core = core
        self.resource = resource
        self.limit = limit
        self.cursor_time = date.utcnow().isoformat() + 'Z'
        self.hasNext = False
        self.hasPrevious = False
        
    def next(self, limit = None):
        if limit is None:
            limit = self.limit
        
        data = PersonalizedStream.get_timeline_stream(self.core, self.resource, limit, None, self.cursor_time)
        cursor = data['meta']['cursor']
        
        self.hasNext = cursor['hasNext']
        self.hasPrevious = cursor['next'] is not None
        self.cursor_time = cursor['next']

        return data
        
    def previous(self, limit = None):
        if limit is None:
            limit = self.limit

        data = PersonalizedStream.get_timeline_stream(self.core, self.resource, limit, self.cursor_time, None)
        cursor = data['meta']['cursor']
        
        self.hasPrevious = cursor['hasPrev']
        self.hasNext = cursor['prev'] is not None
        self.cursor_time = cursor['prev']

        return data
    
    def set_cursor_time(self, new_time):
        self.cursor_time = new_time.utcnow().isoformat() + 'Z'