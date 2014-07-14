from django.db import models


# sister app imports
from djhcup_integration.models import IntegrationTable


FILTER_OPERATOR_MAP = {
    # no operator is represented here for
    # values in list.
    # instead, if value passed to Filter instantiation
    # is a list, then operator is ignored
    "eq": "=",
    "neq": "!=",
    "gt": ">",
    "lt": "<",
    "gte": ">=",
    "lte": "<="
}

FILTER_OPERATOR_CHOICES = [
        ('=','Equal to'),
        ('!=','Not equal to'),
        ('>','Greater than'),
        ('<','Less than'),
        ('>=','Greater than or equal to'),
        ('<=','Less than or equal to'),
        ('IN','In list (comma-separated)'),
        ('NOT IN','Not in list (comma-separated)')
    ]

def is_numeric(s):
    if type(s) is bool:
        return False
    else:
        try:
            float(s)
            return True
        except ValueError:
            return False

# Create your models here.
"""
class DataSet(models.Model):
    name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    # owner
    # table name in here? does this object refer to a db obj?


class Query(models.Model):
    statement = models.TextField(blank=True) # sql generated from Filter objects
    filtergroup = models.ForeignKey('FilterGroup')
"""


class FilterGroup(models.Model):
    any = models.BooleanField(default=True)
    # default True, e.g. join the related filters with an OR
    parent = models.ForeignKey('self',
        default=None, null=True, blank=True)
    # may be None; start with FilterGroup(parent=None)
    
    def _filters(self):
        children = [x for x in FilterGroup.objects.filter(parent=self) if len(x.filter_set.all()) > 0]
        members = [x for x in self.filter_set.all()]
        return children + members
    filters = property(_filters)
    
    def _sql(self):
        if self.any:
            joperator = "OR"
        else:
            joperator = "AND"
        
        return " (%s) " % (" %s " % joperator) \
            .join([f.sql for f in self.filters]) #\
            #.replace (" () ","")
    sql = property(_sql)


class Filter(models.Model):
    filtergroup = models.ForeignKey('FilterGroup')
    column = models.ForeignKey('Column', blank=False)
    value = models.TextField(blank=False)
    # comparison value e.g. column operator [not] value
        
    operator = models.CharField(
        max_length=6, choices=FILTER_OPERATOR_CHOICES,
        default='=', blank=False
    )
    
    
    def _sql(self):
        if self.value is None:
            return None
        else:
            template = '{c} {op} {v}' # noun verb noun
            o = self.operator
            if o not in [x[0] for x in FILTER_OPERATOR_CHOICES]:
                raise Exception("Cannot build sql clause without valid operator. (got '%s')" % self.operator)
            
            if o in ['IN', 'NOT IN']:
                v_lst = [str(x) if is_numeric(x) else "'%s'" % str(x) for x in self.value.split(',')]
                v = " (%s) " % ', '.join(v_lst)
            else:
                if is_numeric(self.value):
                    v = self.value
                else:
                    v = "'%s'" % str(self.value)
            
            return template.format(c=self.column.name, op=o, v=v)
    sql = property(_sql)
    
    
    def __unicode__(self):
        template = '<Filter: {c} {o} {v}, in FilterGroup {fg}>'
        return template.format(
            c = self.column.name,
            o = self.operator,
            v = self.value,
            fg = self.filtergroup.pk
        )
    
    def __repr__(self):
        return self.__unicode__()


class Universe(models.Model):
    name = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=True, null=True, default=None)
    data = models.ForeignKey(
        'ReportingTable',
        related_name = 'data',
        help_text = 'ReportingTable with actual reporting data (ie, CORE PROCESSED integration)'
        )
    lookups = models.ManyToManyField(
        'ReportingTable',
        help_text = "Connects ReportingTable objects to use as lookup tables",
        through = 'LookupTable',
        related_name = 'lookups'
        )
    created_at = models.DateTimeField(auto_now_add=True)
    wip = models.BooleanField(default=True)
    void = models.BooleanField(default=False)
    void_at = models.DateTimeField(blank=True, default=None, null=True)


class LookupTable(models.Model):
    universe = models.ForeignKey('Universe') # fk Universe
    table = models.ForeignKey('ReportingTable') # fk ReportingTable
    lu_type = models.CharField(
        max_length = 10,
        choices = [
            ('DX', 'Diagnoses (long format)'),
            ('PR', 'Procedures (long format)'),
            ('UFLAGS', 'Utilization flags (long format)'),
            ('CHGS', 'Charges (long format)'),
        ],
        blank = False
    )


class ReportingTable(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True, default=None)
    description = models.TextField(blank=True, null=True, default=None)
    suitable_for_lookup = models.BooleanField(default=False) # loosely enforced
    via = models.ForeignKey(IntegrationTable)
    
    def _dbo_name(self): # database object name
        return self.via.name
    dbo_name = property(_dbo_name)


class Column(models.Model):
    name = models.CharField(max_length=100, blank=False)
    #type # alphanumeric, numeric, boolean
    description = models.TextField(blank=True, default=None, null=True)
    table = models.ForeignKey('ReportingTable', blank=False, null=True)
    #distinct_values # m2m Value, cached here for reference
    # need a method to return fully qualified name
    # also need to build filterset stuff so that it has
    # a reference to each required table (via JOIN?).
    # there's probably a way to get a queryset that pulls a distinct list of
    # tables involved here
    
    def __unicode__(self):
        template = '<Reporting Column: {c}>'
        return template.format(c=self.name)
    
    def __repr__(self):
        return self.__unicode__()


"""
class Value(models.Model):
    value
    created
    void


{
    "query": {
        "name": "name_string",
        "description": "desc_string",
        "criteria": [
            # everything in here will be a Filter belonging to a FilterSet with FilterSet._any = False
            # ie NOT ... AND NOT ... AND NOT ... etc
            {
                "column_id": "number",
                "reverse": boolean,
                "operator": "=",
                "values": [
                    "a",
                    "b",
                    "etc"
                ]
            },
            {
            }
        ]
    }
}
"""
