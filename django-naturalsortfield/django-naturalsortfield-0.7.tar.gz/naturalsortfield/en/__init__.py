import re

from naturalsortfield.base import NaturalSortField as BaseNaturalSortField

class NaturalSortFieldEn(BaseNaturalSortField):
    def naturalize(self, string):
        string = super(NaturalSortFieldEn, self).naturalize(string)
        string = re.sub(r'^(?i)the\s+', '', string)
        return string
