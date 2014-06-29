import psycopg2
import logging


from django.conf import settings
from django.db import models


from djhcup_staging.models import StagingTable, DataSource


# pull these into local ns for psycopg2/dbapi2 objects
DB_DEF = settings.DATABASES['djhcup']

# start a logger
default_logger = logging.getLogger('default')


class Edition(models.Model):
    name = models.CharField(max_length=250, blank=False)
    description = models.TextField(blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    void = models.BooleanField(default=False)
    voided_at = models.DateTimeField(blank=True, null=True, default=None)
    
    def generate_tables(self):
        """
        EDITION_CATS = [
            # a list of categories to include in each edition of an integration table set
            dict(val='CORE_PROCESSED', long_entry=None, ds_abbr='CORE'),
            dict(val='DX', long_entry='DX'),
            dict(val='PR', long_entry='PR'),
            dict(val='CHARGES', long_entry='CHGS'),
            dict(val='UFLAGS', long_entry='UFLAGS'),
        ]
        
        # for each category of data
            # grab StagingTables with that category
            # for each unique DataSource
                # filter StagingTables down to those matching DataSource (within category)
                
        # need to somehow deal with extra columns--might just have to define integration/reporting field sets or something
        create_sql = pyhcup.db.long_table_sql(db_table, str(source.abbreviation))
        index_fields = ['KEY', 'VISITLINK', 'STATE', 'YEAR']
        """
        pass


class IntegrationTable(models.Model):
    """This is a record of integration tables created/populated.
    
    stagingtables should share category and data_source
    
    IntegrationTables should always have state and year fields.
    """
    stagingtables = models.ManyToManyField(
        StagingTable,
        help_text="StagingTable objects comprising this IntegrationTable",
        through = 'IntTblStgTblMembers'
        )
    name = models.CharField(max_length=250, blank=False)
    description = models.TextField(blank=True, null=True, default=None)
    edition = models.ForeignKey('Edition')
    definition = models.ForeignKey('Definition', blank=True, null=True)
    schema = models.CharField(max_length=250, blank=True)
    database = models.CharField(max_length=250, blank=True, help_text="Leave blank to use default connection specified in Django's setings.py file")
    wip = models.BooleanField(
        default=True,
        help_text="This table is work-in-progress, and should not be used."
    )
    
    #meta cruft
    created_at = models.DateTimeField(auto_now_add=True)
    void = models.BooleanField(default=False)
    voided_at = models.DateTimeField(blank=True, null=True, default=None)
    records = models.IntegerField(blank=True, null=True, default=None)
    
    def __unicode__(self):
        return "IntegrationTable %d: %s" % (self.pk, self.name)
    
    # overwrite to drop associated table by default when deleting
    def delete(self, drop_table=True, *args, **kwargs):
        if drop_table:
            cnxn = psycopg2.connect(
                host=DB_DEF['HOST'],
                port=DB_DEF['PORT'],
                user=DB_DEF['USER'],
                password=DB_DEF['PASSWORD'],
                database=DB_DEF['NAME'],
            )
            drop_result = pyhcup.db.pg_drop(cnxn, self.name)
            if drop_result == True:
                default_logger.info('Dropped table {table} from database'.format(table=self.name))
            else:
                default_logger.error('Unable to drop table {table} from database'.format(table=self.name))
        
        super(IntegrationTable, self).delete(*args, **kwargs)
    
    """
    def get_absolute_url(self):
        return reverse(
            'djhcup_integration.views.obj_detail',
            kwargs={'obj_id': self.pk, 'obj_type': 'IntegrationTable'}
        )
    """


class Definition(models.Model):
    """
    Groups a set of integration Column objects 
    """
    
    data_source = models.ForeignKey(
        DataSource,
        help_text="""
            Parent DataSource object from djhcup_staging; e.g., HCUP SID. This is more correctly thought of
            as a DataSource family rather than the specific DataSource associated with the planned integration.
            """,
        blank=True, # this is optional,
        null=True
    )
    TBL_CAT_CHOICES = [
        ('CHARGES','Charges data in long format (converted from wide source if necessary)'),
        ('DX','Diagnoses data in long format (from CORE_SOURCE)'),
        ('PR','Procedures data in long format (from CORE_SOURCE)'),
        ('UFLAGS','Utilization flag data, long format (from CORE_SOURCE, CHARGES, and PR)'),
        ('CORE_PROCESSED','CORE Processed: CORE, DaysToEvent/VisitLink, wide charges, wide uflags'),
    ]
    
    category = models.CharField(
        max_length=100,
        choices=TBL_CAT_CHOICES,
        blank=False
    )
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    columns = models.ManyToManyField('Column')
    
    def __unicode__(self):
        return '<Integration Definition: {n} ({c})>' \
            .format(n=self.name, c=self.category)


class IntTblStgTblMembers(models.Model):
    integrationtable = models.ForeignKey('IntegrationTable')
    stagingtable = models.ForeignKey(StagingTable)
    mappedcols = models.ManyToManyField('Column', through='MappedColumn')
    unmappedcols = models.ManyToManyField('Column', related_name='unmappedcols')


class MappedColumn(models.Model):
    inttblstgtblmembers = models.ForeignKey('IntTblStgTblMembers')
    column = models.ForeignKey('Column')
    matched_in = models.ForeignKey('ColumnName')


class Column(models.Model):
    """
    Personally I believe this would be better if fields_in actually referred
    to djhcup_staging.models.Column objects, but then I'd need another layer
    that establishes the list of column names which qualify for inclusion.
    
    Might still be good to do at a future date but right now is kind of a
    hassle.
    """
    fields_in = models.ManyToManyField('ColumnName', related_name='fields_in')
    field_out = models.ForeignKey('ColumnName', related_name='field_out')
    TYPE_CHOICES = [
            ('INT', 'Integer'),
            ('BIGINT', 'Integer'),
            ('TEXT', 'Text field'),
            ('VARCHAR', 'Character varying'),
            ('NUMERIC(2, 15)', 'Decimal, out to hundredths'),
        ]
    field_out_data_type = models.CharField(max_length=15, choices=TYPE_CHOICES, default='VARCHAR')
    field_out_scale = models.IntegerField(blank=True, null=True, default=None)
    field_out_precision = models.IntegerField(blank=True, null=True, default=None)
    
    def __unicode__(self):
        return '<Integration Column: {i} to {o} ({pk})>' \
            .format(i=[str(x.value) for x in self.fields_in.all()],
                    o=self.field_out.value, pk=self.pk)


class ColumnName(models.Model):
    value = models.CharField(max_length=150, blank=False)
    
    def __unicode__(self):
        return 'ColumnName: {v}'.format(v=self.value)
