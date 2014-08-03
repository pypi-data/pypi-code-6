__author__ = 'Eric'


class FishPoint(dict):

    fields = ['fish_type',
         'fish_subtype',
         'index',
         'pos_x',
         'pos_y',
         'organism_length',
         'organism_area',]

    def __init__(self, **kwargs):
        super(FishPoint, self).__init__()
        for field in self.fields:
            self[field] = None

        self.update(kwargs)

        self.line = None # a list of two points (tuples) if set
        self.polygon = None # a list of points if set


    def __getattr__(self, item):
        """Maps values to attributes.
        Only called if there *isn't* an attribute with this name
        """
        try:
            return self.__getitem__(item)
        except KeyError:
            raise AttributeError(item)

    def __setattr__(self, item, value):
        """Maps attributes to values.
        Only if we are initialised
        """
        #if not self.__dict__.has_key('_FishPoint__initialized'):  # this test allows attributes to be set in the __init__ method
        #    return dict.__setattr__(self, item, value)
        if self.__dict__.has_key(item):       # any normal attributes are handled normally
            dict.__setattr__(self, item, value)
        else:
            self.__setitem__(item, value)