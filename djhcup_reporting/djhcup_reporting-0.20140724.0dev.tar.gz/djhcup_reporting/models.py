import datetime
import logging


from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import utc
from django.core.urlresolvers import reverse


# sister app imports
from djhcup_core.utils import salt
from djhcup_integration.models import IntegrationTable, Column as IntegrationColumn, Definition as IntegrationDefinition, Edition as IntegrationEdition


logger = logging.getLogger('default')
DEFAULT_LOGGER = logger


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

ALLOWED_LOG_LEVELS = ['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


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
class DataSet(models.Model):
    name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    query = models.OneToOneField('Query', blank=False)
    created = models.DateTimeField(auto_now_add=True)
    start = models.DateTimeField(blank=True, null=True)
    complete = models.DateTimeField(blank=True, null=True)
    dbo_name = models.CharField(max_length=53, blank=True, default=None, null=True)
    dbo_name_prefix = models.CharField(max_length=12, default='rpt_dataset_',
                                       editable=False)
    #owner = # fk django user object (m2m?)
    # link
    void = models.BooleanField(default=False)
    void_at = models.DateTimeField(blank=True, default=None, null=True)
    # voided_by? # fk django user object 
    
    STATUS_CHOICES = [
        ('NEW', 'Not started'),
        ('QUEUED', 'Request for processing sent'),
        ('DISPATCHED', 'Sent to Celery'),
        ('RECEIVED', 'Received by Celery'),
        ('IN PROCESS', 'Running'),
        ('FAILED', 'Failed to complete'),
        ('SUCCESS', 'Completed successfully'),
    ]
    status = models.CharField(max_length=25, choices=STATUS_CHOICES,
                              default='NEW')
    
    
    def extract(self, cnxn, dry_run=False):
        """Generates SQL and runs a query to extract a dataset.
        
        Parameters
        ===============
        cnxn: dbapi connection object (e.g., from psycopg2.connect())
        
        dry_run: boolean (default False)
            If True, the database will be read but not modified.
        """
        
        self.start = datetime.datetime.utcnow().replace(tzinfo=utc)
        
        if self.dbo_name is None or len(self.dbo_name) == 0:
            self.gen_dbo(overwrite=True)
            
            if not dry_run:
                self.save()
                self.log("Set dbo_name to %s" % self.dbo_name)
        
        cursor = cnxn.cursor()
        stmt_check_exists = "SELECT COUNT(*) FROM pg_tables WHERE tablename='{tbl}';" \
            .format(tbl=self.dbo_name)
        cursor.execute(stmt_check_exists)
        if cursor.fetchone()[0] > 0:
            self.log("Table already exists in database; extraction halted.")
            return False
        
        
        stmt_template = "CREATE TABLE {des} AS\n{src}"
        q = self.query
        q.statement = stmt_template.format(des=self.dbo_name, src=q.sql)
        q.statement_last_update = datetime.datetime.utcnow().replace(tzinfo=utc)
        if not dry_run:
            q.save()
        
        if not dry_run:
            try:
                cursor.execute(q.statement)
                cnxn.commit()
            except:
                self.fail("Failed to execute statement")
                raise
            
            self.success("Populated dataset in %s" % self.dbo_name)
        
        return self.dbo_name
    
    
    def fail(self, message=None, logger=None, level='ERROR'):
        self.status = 'FAILED'
        self.complete = datetime.datetime.utcnow().replace(tzinfo=utc)
        self.save()
        
        if message is not None:
            self.log(message, level=level, logger=logger)
        
        return message
    
    def success(self, message=None, logger=None):
        self.status = 'SUCCESS'
        self.complete = datetime.datetime.utcnow().replace(tzinfo=utc)
        self.save()
        
        if message is not None:
            self.log(message, logger=logger)
        
        return message
    
    def log(self, message, level='INFO', status=None, logger=None):
        """Emit a log message at the specified log level and optionally update the ImportQueue object status attribute.
        """
        
        if level not in ALLOWED_LOG_LEVELS:
            raise Exception("Invalid log level specified: %s" % level)
        else:
            level = getattr(logging, level)
        
        if logger is None:
            logger = DEFAULT_LOGGER
        
        if status is not None:
            self.status = status
        
        logger_message = "[DataSet %s] %s" % (self.pk, message)
        logger.log(level, logger_message)
        return message    
    
    def _universe(self):
        return self.query.universe
    universe = property(_universe)
    
    def gen_dbo(self, overwrite=False):
        """Find a table name not presently in use, and
        save it as the table name for this DataSet.
        
        Pseudo-randomly generated.
        """
        unused = False
        while unused == False:
            candidate = self.dbo_name_prefix + salt()
            check = DataSet.objects.filter(dbo_name=candidate)
            if len(check) == 0:
                unused = True
        
        if overwrite:
            self.dbo_name = candidate
        
        return candidate
    
    def __unicode__(self):
        template = '<DataSet {pk}: name=\'{nm}\', query={qpk},'
        template += ' started={st}, completed={cd},'
        template += ' dbo_name={dbo}>'
        
        if self.pk == None:
            pk = '[unsaved]'
        else:
            pk = self.pk
        
        return template.format(
            pk = pk,
            nm = self.name,
            qpk = self.query.pk,
            st = self.start,
            cd = self.complete,
            dbo = self.dbo_name
        )
    
    def __repr__(self):
        return self.__unicode__()
    
    def get_absolute_url(self):
        return reverse(
            'djhcup_reporting.views.dataset_details',
            kwargs={'dataset_dbo_name': self.dbo_name}
        )


class Query(models.Model):
    """Brings together a universe and a filtergroup. Can then generate
    (and store) an SQL statement
    """
    statement = models.TextField(default=None, blank=True, null=True,
                                 help_text='Generated from filtergroup')
    statement_last_update = models.DateTimeField(default=None, blank=True, null=True)
    explain = models.TextField(default=None, blank=True, null=True, 
                               help_text='Generated from statement')
    explain_last_update = models.DateTimeField(default=None, blank=True, null=True)
    universe = models.ForeignKey('Universe')
    filtergroup = models.OneToOneField('FilterGroup', blank=False)
    #owner = # fk django user object
    
    def _select(self, use_fqdbo=False):
        try:
            if use_fqdbo:
                return ', '.join([c.fqdbo for c in self.universe.data.column_set.all()])
            else:
                return ', '.join([c.name for c in self.universe.data.columns.all()])
        except:
            return None
    clause_select = property(_select)
    
    
    def _from(self):
        # NOTE: this may be extended in the future for multi-table support
        try:
            return self.universe.data.dbo_name
        except:
            return None
    clause_from = property(_from)
    
    
    def _where(self):
        try:
            return self.filtergroup.sql
        except:
            return None
    clause_where = property(_where)
    
    
    def _sql(self, update_statement=True, use_fqdbo=False):
        # set general template
        template = """
        SELECT {fields}
        FROM {table}
        WHERE {conditions}
        """
        
        # push into template
        _statement = template.format(fields=self.clause_select,
                                     table=self.clause_from,
                                     conditions=self.clause_where)
        
        # update, if requested
        if update_statement:
            self.statement = _statement
            self.statement_last_update = datetime.datetime.utcnow().replace(tzinfo=utc)
            self.save()
        
        return _statement
    sql = property(_sql)
    
    
    def __unicode__(self):
        template = '<Query {pk}: universe={u}, valid_select={vs},'
        template += ' valid_from={vf}, valid_where={vw}>'
        
        if self.pk == None:
            pk = '[unsaved]'
        else:
            pk = self.pk
            
        if len(self.universe.name) > 0:
            u = self.universe.name
        else:
            u = self.universe.pk
        
        return template.format(
            pk = pk,
            u = u,
            vs = self.clause_select is not None,
            vf = self.clause_from is not None,
            vw = self.clause_where is not None
        )
    
    def __repr__(self):
        return self.__unicode__()
    

class FilterGroup(models.Model):
    any = models.BooleanField(default=True)
    # default True, e.g. join the related filters with an OR
    parent = models.ForeignKey('self', default=None, null=True,
                               blank=True)
    # may be None; start with FilterGroup(parent=None)
    
    def _filters(self):
        children = [x for x in FilterGroup.objects.filter(parent=self)
                    if len(x.filter_set.all()) > 0]
        members = [x for x in self.filter_set.all()]
        return children + members
    filters = property(_filters)
    
    def _sql(self):
        if self.any:
            joperator = "OR"
        else:
            joperator = "AND"
        
        return "(%s) " % (" %s " % joperator) \
            .join([f.sql for f in self.filters]) #\
            #.replace (" () ","")
    sql = property(_sql)
    
    def _tables(self):
        tables = []
        t_lst = []
        for f in self.filters:
            if isinstance(f, Filter):
                try:
                    t_lst.append(f.tbl_dbo)
                except:
                    pass
            else: # ought to be FilterGroup
                try:
                    t_lst.extend(f.tables)
                except:
                    pass
        for t in t_lst:
            if t not in tables:
                tables.append(t)
        return tables
    tables = property(_tables)
    
    # TODO:
    # If parent == None, need to round up all the required
    # table names, plus format this stuff properly within a
    # SELECT * FROM the_big_table WHERE ({filter_sql}) stmt
    
    def __unicode__(self):
        return "<FilterGroup {pk}>".format(pk=self.pk)


class Filter(models.Model):
    filtergroup = models.ForeignKey('FilterGroup')
    column = models.ForeignKey('Column', blank=False)
    value = models.TextField(blank=False)
    # comparison value e.g. column operator [not] value
        
    operator = models.CharField(
        max_length=6, choices=FILTER_OPERATOR_CHOICES,
        default='=', blank=False
    )
    
    def operator_is_valid(self):
        if self.operator in [x[0] for x in FILTER_OPERATOR_CHOICES]:
            return True
        else:
            return False
    
    def operator_is_list_type(self):
        if self.operator in ['IN', 'NOT IN']:
            return True
        else:
            return False
    
    def _tbl_dbo(self):
        try:
            return self.column.table.dbo_name
        except:
            return None
    tbl_dbo = property(_tbl_dbo)
    
    def _sql(self):
        # noun verb noun
        # column operator value
        
        if self.value is None:
            return None
        else:
            o = self.operator
            if not self.operator_is_valid():
                raise Exception("Cannot build sql clause without valid operator. (got '%s')" % self.operator)
            
            if self.column.is_lookup:
                # template takes the form of a subquery, returning KEY values only
                template = 'KEY IN (SELECT KEY FROM {t} WHERE {c} {op} {v})'
            else:
                template = '{t}.{c} {op} {v}'
                
            
            if self.operator_is_list_type():
                v_lst = ["'%s'" % str(x).strip() for x in self.value.split(',')]
                v = " (%s) " % ', '.join(v_lst)
            else:
                v = "'%s'" % str(self.value)
            
            return template.format(t=self.column.table.dbo_name, c=self.column.name, op=o, v=v)
    sql = property(_sql)
    
    
    def __unicode__(self):
        template = '<Filter: {c} {o} {v}, in FilterGroup {fg}>'
        return template.format(
            c = self.column.fqdbo,
            o = self.operator,
            v = self.value,
            fg = self.filtergroup.pk
        )
    
    def __repr__(self):
        return self.__unicode__()


class Definition(models.Model):
    name = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=True, null=True, default=None)
    data = models.ForeignKey(
        IntegrationDefinition,
        related_name = 'data',
        help_text = 'Integration module Definition which should be used as a data table in a reporting universe.'
    )
    lookups = models.ManyToManyField(
        IntegrationDefinition,
        related_name = 'lookups',
        help_text = 'Integration module Definitions to be used as lookup tables in a reporting universe.',
        through = 'DefLookups'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    void = models.BooleanField(default=False)
    void_at = models.DateTimeField(blank=True, default=None, null=True)
    
    
    def refresh_universe(self, name, description=None):
        """
        Returns djhcup_reporting.models.Universe object if a newer Edition
        is available for all the inputs in this Definition.
        
        Returns False if no newer Edition exists with all the required inputs.
        
        Parameters
        ===============
        name: string (required)
            Name for the newly-created Universe object.
        
        decription: string (optional)
            Description for the newly-created Universe object.
        """
        # TODO: Add a name template for ReportingTable objects
        # this is where latest edition with all elements should be found
        # and a new universe should be made.
        
        e_qs = IntegrationEdition.objects.filter(
            void=False,
        ).order_by(
            '-created_at'
        )
        print "e_qs is %s" % e_qs
        
        def_u_qs = Universe.objects.filter(definition=self)
        print "def_u_qs is %s" % def_u_qs
        
        if len(def_u_qs) > 0:
            # make sure the editions we're choosing from are
            # more recent than the current most recent universe
            e_qs = e_qs.filter(created_at__gt=def_u_qs[0].created_at)
            print "e_qs is %s" % e_qs
        
        if len(e_qs) == 0:
            return False
        
        # need not indent here; will have exited already from the return call
        u = None
        for e in e_qs:
            # cycle through these Edition objects in descending order
            # by creation timestamp.
            
            if u == None:
                # proceed
                # u will be overwritten if something is found
                data_int_tables = IntegrationTable.objects.filter(
                    definition=self.data,
                    void=False,
                    wip=False,
                    edition=e
                )
                print "data_int_tables is %s" % data_int_tables
                logger.debug("Found {ct} IntegrationTable objects for " +\
                        "definition {d}, edition {e}".format(
                            ct=len(data_int_tables), d=self.data, e=e
                        )
                )
                
                if len(data_int_tables) > 0:
                    # set this aside for Universe later
                    data_int_tbl = data_int_tables[0]
                    
                    # proceed to looking for lookup tables
                    lu_table_lst = []
                    lu_defs = self.deflookups_set.all()
                    
                    for def_lu in lu_defs:
                        #LookupTable
                        print "looking for IntegrationTable objects with definition %s" % def_lu.int_definition
                        lu_tables = IntegrationTable.objects.filter(
                            definition=def_lu.int_definition,
                            void=False,
                        ).order_by(
                            '-created_at'
                        )
                        
                        print len(lu_tables)
                        # just use the first
                        if len(lu_tables) == 1:
                            lu_table_lst.append(dict(
                                int_definition=def_lu.int_definition,
                                table=lu_tables[0],
                                lu_type=def_lu.lu_type
                            ))
                    
                    # make col objects for ReportingTable
                    if len(lu_defs) == len(lu_table_lst):
                        # got all the required ones (hootie hooooo!)
                        print "found all required lookup tables"
                        name_template = "Reporting Definition {d}, Edition {e}"
                        
                        # make a ReportingTable obj for data
                        data_tbl = ReportingTable(
                            via=data_int_tbl,
                            name=name_template.format(d=self.data.pk, e=e)
                        )
                        data_tbl.save()
                        
                        # make col objects for ReportingTable
                        for icol in self.data.columns.all():
                            dcol = Column(
                                table=data_tbl,
                                int_column=icol
                            )
                            dcol.save()
                        
                        # proceed to make Universe and populate it
                        # (have to do this before lookups, as m2m
                        # require a key on each table to create)
                        u = Universe(
                            definition=self,
                            name=name,
                            description=description,
                            edition=e,
                            data=data_tbl
                        )
                        u.save()
                        
                        for lu in lu_table_lst:
                            # bake the lookups back in, via intermediate table
                            r_tbl = ReportingTable(
                                is_lookup=True,
                                via=lu['table'],
                                name=name_template.format(d=self.data.pk, e=e)
                            )
                            r_tbl.save()
                            
                            # make col objects for ReportingTable
                            for icol in lu['int_definition'].columns.all():
                                dcol = Column(
                                    table=r_tbl,
                                    int_column=icol
                                )
                                dcol.save()
                            
                            lu_tbl = LookupTable(
                                universe=u,
                                table=r_tbl,
                                lu_type=lu['lu_type']
                            )
                            lu_tbl.save()
                        
                        u.wip = False
                        u.save()
                    else:
                        print "Did not find all required lookup tables"
                else:
                    print "Found no data integration tables"
        return u        


    def __unicode__(self):
        return '<Reporting Definition {pk}: {name}>' \
            .format(pk=self.pk, name=self.name)

        
    def __repr__(self):
        return self.__unicode__()


class DefLookups(models.Model):
    """The lookup table part of a definition for universe generation.
    """
    definition = models.ForeignKey('Definition')
    int_definition = models.ForeignKey(IntegrationDefinition)
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
    created_at = models.DateTimeField(auto_now_add=True)
    void = models.BooleanField(default=False)
    void_at = models.DateTimeField(blank=True, default=None, null=True)
    
    def __unicode__(self):
        return "<DefLookups {pk}: reporting definition={d}, integration definition={i}>" \
            .format(pk=self.pk, d=self.definition.pk, i=self.int_definition.pk)


class Universe(models.Model):
    definition = models.ForeignKey('Definition')
    name = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=True, null=True, default=None)
    edition = models.ForeignKey(IntegrationEdition)
    data = models.ForeignKey(
        'ReportingTable',
        related_name = 'data',
        help_text = 'ReportingTable with actual reporting data (ie, CORE PROCESSED integration)'
    )
    lookups = models.ManyToManyField(
        'ReportingTable',
        related_name = 'lookups',
        help_text = "Connects ReportingTable objects to use as lookup tables",
        through = 'LookupTable',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    wip = models.BooleanField(default=True)
    void = models.BooleanField(default=False)
    void_at = models.DateTimeField(blank=True, default=None,
                                   null=True)
    
    def filters_for_display(self):
        filters = []
        
        # gather cols from the "data" table in this definition
        try:
            t = self.data
        except:
            raise Exception("Unable to find a data table from Universe {pk} for determining filters".format(pk=self.pk))
        
        options = []
        for c in t.column_set.all().order_by('int_column__field_out__value'):
            try:
                options.append(dict(value=c.pk, display=c.name.lower()))
            except:
                pass
        filters.append(dict(label="Data Fields", options=options))
        
        # gather cols similarly for lookup tables
        lookup_tables = self.lookuptable_set.all()
        for lu in lookup_tables:

            try:
                t = lu.table
                options = []
                for c in t.column_set.all().order_by('int_column__field_out__value'):
                    try:
                        options.append(dict(value=c.pk, display=c.name.lower()))
                    except:
                        pass
                filters.append(dict(label="Lookup Table: " + lu.get_lu_type_display(), options=options))
            except:
                pass
        
        return filters    
    
    def __unicode__(self):
        try:
            d = self.data.dbo_name
        except:
            d = None
        template = '<Universe {pk}: {n}, data={d} with {l_ct} lookups>'
        return template.format(pk=self.pk, n=self.name, d=d, l_ct=self.lookups.all().count())
    
    def __repr__(self):
        return self.__unicode__()


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
    created_at = models.DateTimeField(auto_now_add=True)
    void = models.BooleanField(default=False)
    void_at = models.DateTimeField(blank=True, default=None, null=True)
    
    def __unicode__(self):
        template = '<LookupTable {pk}: {lu} ({dbo})>'
        return template.format(pk=self.pk, lu=self.get_lu_type_display(), dbo=self.table.dbo_name)
    
    def __repr__(self):
        return self.__unicode__()


class ReportingTable(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True, default=None)
    description = models.TextField(blank=True, null=True, default=None)
    is_lookup = models.BooleanField(default=False)
    via = models.ForeignKey(IntegrationTable)
    created_at = models.DateTimeField(auto_now_add=True)
    void = models.BooleanField(default=False)
    void_at = models.DateTimeField(blank=True, default=None, null=True)
    
    columns = models.ManyToManyField(IntegrationColumn, through='Column')
    
    def _dbo_name(self): # database object name
        try:
            return self.via.name
        except:
            return None
    dbo_name = property(_dbo_name)
    
    def __unicode__(self):
        template = '<ReportingTable {pk}: {t} ({dbo})>'
        return template.format(pk=self.pk, t=self.name, dbo=self.dbo_name)
    
    def __repr__(self):
        return self.__unicode__()


class Column(models.Model):
    table = models.ForeignKey('ReportingTable', blank=False, null=True)
    int_column = models.ForeignKey(IntegrationColumn, blank=False, null=True)
    #distinct_values # m2m Value, cached here for reference
    # need a method to return fully qualified name
    # also need to build filterset stuff so that it has
    # a reference to each required table (via JOIN?).
    # there's probably a way to get a queryset that pulls a distinct list of
    # tables involved here
    
    def _name(self):
        return self.int_column.field_out.value
    name = property(_name)
    
    def _is_lookup(self):
        """Returns True if column is from a lookup table.
        Otherwise, returns False.
        """
        try:
            if self.table.is_lookup == True:
                return True
            else:
                return False
        except:
            logger.warning("Caught an Exception while calling" +\
                "_is_lookup() on Column {pk}".format(pk=pk))
            return False
    is_lookup = property(_is_lookup)
    
    def _fqdbo(self):
        """Returns fully-qualified database object (column name with
        dot-notated table).
        """
        return '{t}.{c}'.format(c=self.name, t=self.table.dbo_name)
    fqdbo = property(_fqdbo)
    
    def __unicode__(self):
        template = '<Reporting Column: {fqdbo}>'
        return template.format(fqdbo=self.fqdbo)
    
    def __repr__(self):
        return self.__unicode__()
