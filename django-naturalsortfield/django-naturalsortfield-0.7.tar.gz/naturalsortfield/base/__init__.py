import re

from django.db import models

class NaturalSortField(models.CharField):
    def __init__(self, for_field, **kwargs):
        self.for_field = for_field
        super(NaturalSortField, self).__init__(**kwargs)

    def pre_save(self, model_instance, add):
        return self.naturalize(getattr(model_instance, self.for_field))
    
    def naturalize(self, string):
        def naturalize_int_match(match):
            return '%08d' % (int(match.group(0)),)
        
        string = string.lower()
        string = string.strip()
        string = re.sub(r'\d+', naturalize_int_match, string)
        
        return string
