# core Python packages
import datetime
import itertools
import logging
import os
import re
import sys
from copy import deepcopy


# third party packages
import pyhcup
from pyhcup.db import pg_getcols
from pyhcup.parser import df_wtl
from pyhcup.parser import replace_sentinels
from pyhcup.db import insert_sql as gen_insert_sql
from pyhcup.meta import is_long as meta_is_long


# django packages
from django.utils.timezone import utc
from django.conf import settings
#import shortcuts to use with raw sql (!) later
from django.db import connections as cnxns
from django.db import transaction as tx
from django import db as djangodb


# local project and app packages
from djhcup_staging.models import State, DataSource, FileType, File, Column, ImportQueue, ImportBatch, StagingQueue, StagingBatch, StagingTable
from djhcup_staging.utils.misc import dead_batches, get_pgcnxn


# start a logger
logger = logging.getLogger('default')


# make these tasks app-agnostic with @celery.shared_task
import celery
from celery.result import AsyncResult


HACHOIR_DB_ENTRY = 'djhcup'

# check to see if psycopg2 is how we're going
DB_DEF = settings.DATABASES[HACHOIR_DB_ENTRY]
DB_BACKEND = DB_DEF['ENGINE'].split('.')[-1]

@celery.shared_task
@tx.atomic # turn off autocommit
def reset_dead():
    """Resets dead (interrupted) ImportBatch and ImportQueue objects intelligently.
    
    Types of failure:
    
    1. batch is started but not complete and celery task is no longer held in queue or being processed
        --> ignore any related ImportQueue objects where completed is not null and status is SUCCESS
        --> delete db records in related StagingTable for state-year combinations on incomplete ImportQueue objects
        Code is written in for this below
    """
    
    b_reset = 0
    iq_reset = 0
    
    # grab a database cursor for use downstream
    cursor = cnxns[HACHOIR_DB_ENTRY].cursor()

    # get the dead batches
    dead_batch_qs = dead_batches()
    
    # loop through dead batches cleaning up individual ImportQueue entries
    for b in dead_batch_qs:
        # get related ImportQueue objects
        inc_iq_qs = ImportQueue.objects.filter(batch__pk=b.pk)
        
        # but leave any successful imports alone
        dead_iq_qs = inc_iq_qs.exclude(status='SUCCESS')
        
        # make a list of tuples representing the state-years to roll back
        rollback_lst = [(iq.file.state.abbreviation, iq.file.year) for iq in dead_iq_qs]
        
        # build a SQL delete statement and list of parameters to delete records for these dead imports
        sql = "DELETE FROM "
        
        # tack on table identity (w/optional schema)
        table = b.destination.name
        if b.destination.schema is not None:
            table = b.destination.schema + "." + table
        sql += table
        
        # form WHERE clause with placeholders
        sql += " WHERE " + " OR ".join("(STATE=%s AND YEAR=%s)" for rb in rollback_lst)
        
        # cap it off
        sql += ";"
        
        params = [val for y in rollback_lst for val in y]
        
        # execute the deletes
        cursor.execute(sql, params)
        
        # the staging db has auto-commit turned off by default
        tx.commit(using=HACHOIR_DB_ENTRY)
        
        [logger.info("Deleted records in %s for %s %s" % (table, v[0], v[1])) for v in rollback_lst]
        logger.info("Total records deleted: %s" % cursor.rowcount)
        
        # move on to resetting the ImportQueue objects themselves
        dead_iq_qs.update(start=None, complete=None, status='NEW')
        iq_reset += dead_iq_qs.count()
        
        # and, finally, the batch, too
        b.start=None
        b.complete=None
        b.status='NEW'
        b.save()
        
        b_reset += 1
    
    logger.info("Reset %s dead ImportBatch objects and %s ImportQueue objects" % (b_reset, iq_reset))
    return b_reset, iq_reset


@celery.shared_task(bind=True, ignore_result=True)
def batch_import(self, batch_id):
    """Attempts to import the indicated batch"""
    
    batch = ImportBatch.objects.get(pk=batch_id)
    batch.status = 'RECEIVED'
    batch.celery_task_id = self.request.id
    batch.save()
    
    enqueued = ImportQueue.objects.filter(batch=batch)
    #destination = batch.destination
    logger.info('Found %s' % (batch))
    
    if batch.complete:
        response = 'Batch %i was previously completed at %s, and therefore will not be run' % (batch.pk, batch.complete)
        logger.error(response)
        batch.fail()
        return False
    
    elif enqueued.count() < 1:
        response = 'Batch %i has no items enqueued, and therefore will not be run' % batch.pk
        logger.warning(response)
        batch.fail()
        return True

    else:
        batch_begin = datetime.datetime.utcnow().replace(tzinfo=utc)
        batch.start = batch_begin
        batch.status = 'IN PROCESS'
        batch.save()
        logger.info('Begin batch %s' % (batch))
        
        job = celery.group(
            import_dispatch.si(load.pk) for load in enqueued
            )
        job()
        
        # put a task into background for periodic check that the batch has completed
        batch_complete.apply_async((batch.pk,), countdown=600)
        
        return True


@celery.shared_task(bind=True, ignore_result=True)
def import_dispatch(self, importqueue_pk, insert_size=5, slice_size=1000):
    load = ImportQueue.objects.get(pk=importqueue_pk)
    
    # proceed with making the file happen
    load.status = 'QUEUED'
    load.save()
    
    logger.info('Queued for import dispatch: %s' % (load))
    
    try:
        pg_import_file(load.pk)
        return True
    except:
        logger.info("Encountered an error while importing %s. Check logs for details." % load)
        load.fail(sys.exc_info()[0])
        return False
    
    # FROM HERE BELOW, SPLIT OFF PSYCOPG2 VS NOT
    # These parts are deprecated. postgresql and psycopg2 are now requirements.
    """    
    dsabbr = load.file.file_type.source.abbreviation
    
    if ('psycopg2' in DB_BACKEND and (
            ((dsabbr.upper() in [
                    'CORE',
                    'BASE',
                    'CHGS',
                    'DTE',
                    'AHAL',
                    'DX_PR_GRPS',
                    'SEVERITY'
                    ]) or
                (dsabbr.upper() in ['CHGS'] and meta_is_long(load.get_meta()))
                )
            )
        ):
        # do it Rockapella
        logger.info('Loading with pg_import_file: %s' % (load))
        try:
            pg_import_file(load.pk)
            return True
        except:
            logger.info("Encountered an error while importing %s. Check logs for details." % load)
            load.fail(sys.exc_info()[0])
            return False
    
    else:
        logger.info('Loading with chunk_import_file: %s' % (load))
        chunk_import_file.delay(load.pk)
        return True
    """


@celery.shared_task(bind=True, ignore_result=True)
def pg_import_file(self, importqueue_pk, drop_rawload=True):
    """Assumes psycopg2 availability.
    """
    
    load = ImportQueue.objects.get(pk=importqueue_pk)
    load.status = 'RECEIVED'
    load.celery_task_id = self.request.id
    load.start = datetime.datetime.utcnow().replace(tzinfo=utc)
    load.save()
    load.log('Beginning import with psycopg2',
             level='INFO', logger=logger, status='IN PROCESS')
    
    # TODO: move to integration
    #destination = load.batch.destination
    
    load.log('Begin import',
             level='INFO', logger=logger)
    
    #schema = destination.schema
    state = load.file.state.abbreviation
    year = load.file.year
    dsabbr = load.file.file_type.source.abbreviation
    
    supported_imports = {
        'CORE': 'CORE_SOURCE',
        'CHGS': 'CHARGES_SOURCE',
        'DTE': 'DAYSTOEVENT_SOURCE',
        'AHAL': 'AHALINK_SOURCE',
        'SEVERITY': 'SEVERITY_SOURCE',
        'DX_PR_GRPS': 'DX_PR_GRPS_SOURCE'
    }
    
    if dsabbr in supported_imports:
        stcat = supported_imports[dsabbr]
    else:
        raise Exception("The only imports supported are %s. Got %s." % (", ".join(["HCUP %s (becomes %s)" % (k, v) for k, v in supported_imports.iteritems()]), dsabbr))
    
    now = datetime.datetime.utcnow().replace(tzinfo=utc).strftime("%Y%m%d%H%M%S")
    stg_table_name = '_'.join(str(x) for x in ['stg', state, year, stcat, now]).lower()
    handle = load.file.open()

    # establish connection directly with psycopg2
    cnxn = get_pgcnxn()
    
    # get helper functions
    from pyhcup.db import pg_rawload, pg_staging, pg_shovel, pg_wtl_shovel, pg_drop, pg_dteload
    
    # segregate the csv loads from the non-csv loads
    if str(load.file.filename).split('.')[-1] == 'csv':
        # just do a csv load
        
        # but only for daystoevent CSV files
        if not stcat == 'DAYSTOEVENT_SOURCE':
            raise Exception("Only daystoevent data are eligible for CSV loading.")
        else:
            load.log('Importing CSV file with DaysToEvent data',
                    level='INFO', logger=logger)
        
        result = pg_dteload(cnxn, handle, stg_table_name)
        affected_rows = result[1]
        
        # save info about this import in a StagingTable object
        imported = StagingTable(
            imported_via = load,
            name = stg_table_name,
            category = stcat,
            records = affected_rows
        )
        
        imported.save()
        load.log('StagingTable %s recorded for %s' % (stg_table_name, imported.pk))
        
    else:
        # use db loading functions
        meta = load.get_meta()
        
        load.log('Creating raw import table via pg_rawload()',
                level='INFO', logger=logger)
        rawload = pg_rawload(cnxn, handle, meta)
        load.log('Raw import table %s populated' % (rawload),
                level='INFO', logger=logger)
        
        #dsabbr = load.file.file_type.source.abbreviation
        without_pk = pyhcup.parser.LONG_MAPS.keys() + ['AHAL']
        if dsabbr in without_pk:
            pk_fields = None
            load.log('Staging will be done with no primary key',
                    level='INFO', logger=logger)
        else:
            pk_fields = ['key', 'state', 'year']
            load.log('Staging will be done with primary key %s' % (pk_fields),
                    level='INFO', logger=logger)
        
        load.log('Creating staging table via pg_staging()',
                level='INFO', logger=logger)
        staging = pg_staging(cnxn, rawload, meta, state, year, pk_fields=pk_fields,
                             table_name=stg_table_name)
        load.log('Staging table populated: %s' % (stg_table_name),
                level='INFO', logger=logger)
        
        affected_rows = staging[1]
        
        # save info about this import in a StagingTable object
        imported = StagingTable(
            imported_via = load,
            name = stg_table_name,
            category = stcat,
            records = affected_rows,
            wip = False
        )
        
        imported.save()
        
        load.log('StagingTable %s recorded for %s' % (imported.pk, stg_table_name))
        
        # move on to recording summary statistics about imported columns
        # grab a dbapi2 cursor
        c = cnxn.cursor()

        # augment meta data for storage in Column object
        m_aug = pyhcup.meta.augment(meta)

        # v is a series of values in row with dict-style access by label
        for k, v in m_aug.iterrows():
            load.log("Creating Column record for %s for StagingTable %s" % (v['field'], imported.pk))
            
            # create Column object with preliminary values
            col = Column(
                stg = imported,
                name = v['field'],
                description = v['label'],
                col_type=v['data_type'].upper(),
                col_scale=v['scale'],
                col_precision=v['length'],
                informat=v['informat']
                )
            
            if v['numeric_or_int']:
                # numeric types can run descriptive statistics
                sql = """
                    SELECT
                        SUM(CASE WHEN {field} IS NULL THEN 0 ELSE 1 END) AS count_notnull,
                        SUM(CASE WHEN {field} IS NULL THEN 1 ELSE 0 END) AS count_null,
                        MIN({field}) AS min,
                        MAX({field}) AS max,
                        STDDEV_POP({field}) as stddev_pop,
                        STDDEV_SAMP({field}) AS stddev_samp,
                        AVG({field}) AS average
                    FROM {table};
                    """.format(field=col.name, table=imported.name)
                c.execute(sql)
                result = c.fetchone()
                
                col.count_notnull = result[0]
                col.count_null = result[1]
                col.min = result[2]
                col.max = result[3]
                col.stddev_pop = result[4]
                col.stddev_samp = result[5]
                col.mean = result[6]
            
            else:
                # non-numeric types can do null/not-null.
                # technically they can and probably should also do frequency
                # distributions, but those are extra tough to scrape from
                # the HCUP reference docs
                sql = """
                    SELECT
                        SUM(CASE WHEN {field} IS NULL THEN 0 ELSE 1 END) AS count_notnull,
                        SUM(CASE WHEN {field} IS NULL THEN 1 ELSE 0 END) AS count_null
                    FROM {table};
                    """.format(field=col.name, table=imported.name)
                c.execute(sql)
                result = c.fetchone()
                
                col.count_notnull = result[0]
                col.count_null = result[1]
            
            col.save()
            load.log('Recorded Column %s' % (col.pk))
            load.log('Attempting to validate Column %s' % (col.pk))
            v_result = col.validate()
            load.log('Validation status for Column %s is %s' % (col.pk, col.integrity_status))
        
        """
        else:
            fields = [x for x in meta.field if x.lower() not in ['state', 'year']]
            fields += ['state', 'year']
            
            #logger.info('Inserting contents of staging table %s to master table %s: %s' % (staging[0], table, load))
            load.log('Inserting contents of staging table %s to master table %s' % (staging[0], table),
                    level='INFO', logger=logger)
            affected_rows = pg_shovel(cnxn, staging[0], table, fields)
            logger.info('Inserted contents of staging table %s to master table %s (%s rows): %s' % (staging[0], raw_table_name, affected_rows, load))
            load.log('Inserted contents of staging table %s to master table %s (%s rows)' % (staging[0], raw_table_name, affected_rows),
                    level='INFO', logger=logger)
        """
        
        if drop_rawload:
            # TODO: Rework this section a little more elegantly
            drop_targets = [rawload]#, staging[0]]
            for dtbl in drop_targets:
                #logger.info('Dropping intermediate table %s: %s' % (dtbl, load))
                load.log('Dropping intermediate table: %s' % (dtbl),
                        level='INFO', logger=logger)
                drop_result = pg_drop(cnxn, dtbl)
                if drop_result == True:
                    logger.info('Successfully dropped intermediate table %s: %s' % (dtbl, load))
                    load.log('Successfully dropped intermediate table: %s' % (dtbl),
                            level='INFO', logger=logger)
                else:
                    logger.error('Failed to drop %s: %s' % (dtbl, load))
                    load.log('Failed to drop: %s' % (dtbl),
                            level='ERROR', logger=logger)
    
    # affected_rows will evaluate un-True in the case of any troubles
    if affected_rows:
        load.success('Import complete (%s rows)' % (affected_rows))
        #logger.info('Import complete: %s (%s rows)' % (load, affected_rows))
        return True
    else:
        load.fail('Import failed')
        #logger.error('Import failed: %s' % load)
        return False


@celery.shared_task(bind=True, max_retries=None, default_retry_delay=10)
def import_complete(self, result_lst, importqueue_pk):
    """Checks periodically to see if these have completed and updates associated ImportQueue obj with outcome
    """
    
    iq = ImportQueue.objects.get(pk=importqueue_pk)
        
    if all(r.ready() for r in itertools.chain(*result_lst)):
        if all(r.successful() for r in itertools.chain(*result_lst)):
            iq.success()
            logger.info('Import complete: %s' % iq)
            return True
        else:
            iq.fail()
            logger.error('Import failed: %s' % iq)
            raise Exception('Import failed: %s' % iq)
    else:
        raise self.retry(exc=Exception('Import not yet complete: %s' % iq))


@celery.shared_task(bind=True, max_retries=None, default_retry_delay=900)# default_retry_delay=60)
def batch_complete(self, batch_pk):
    """Checks to see if each item in the batch has a completion timestamp in db, and updates batch db entry to reflect success/failure of overall batch.
    """
    
    # grab the django representation of this ImportBatch
    b = ImportBatch.objects.get(pk=batch_pk)
    
    # and, while we're at it, the associated ImportQueue objects
    enqueued = ImportQueue.objects.filter(batch=b)
    
    try:
        # test if all completed, one way or another
        if all(q.complete is not None for q in enqueued):
            
            # test if the outcomes were all SUCCESS
            if all(q.successful() for q in enqueued):
                b.success()
                logger.info('Batch completed successfully: %s' % b)
                return True
            else:
                b.fail()
                logger.error('One or more imports failed: %s' % b)
                return False
        else:
            # since some haven't completed yet, raise IncompleteStream and retry
            raise celery.exceptions.IncompleteStream
    
    except celery.exceptions.IncompleteStream as exc:
        # try again a little later, when the streams are more complete
        raise self.retry(exc=Exception('Batch not yet complete: %s' % b))


@celery.shared_task(bind=True, ignore_result=True)
def stage_dispatch(self, stagingqueue_pk):
    stg_q = StagingQueue.objects.get(pk=stagingqueue_pk)
    
    # proceed with making the file happen
    stg_q.status = 'QUEUED'
    stg_q.save()
    
    logger.info('Queued for staging: %s' % (stg_q))
    
    try:
        pg_stage(stg_q.pk)
        return True
    except:
        logger.info("Encountered an error while staging %s. Check logs for details." % stg_q)
        stg_q.fail(sys.exc_info()[0])
        return False


@celery.shared_task(bind=True, ignore_result=True)
def pg_stage(self, stagingqueue_pk):
    """Processes StagingQueue object with primary key stagingqueue_pk. Automatically creates and records destination table as appropriate.
    """
    
    stg_q = StagingQueue.objects.get(pk=stagingqueue_pk)
    stg_q.log('pg_stage called', 
              level='INFO', logger=logger)
    
    category = stg_q.category
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    
    allowed_categories = ['CHARGES', 'DX', 'PR', 'UFLAGS', 'CORE_PROCESSED']
    #'CORE_PROCESSED' -> should be moved to an integration setting
    if category not in allowed_categories:
        message = "The only supported staging categories are %s. Got %s" % (", ".join(allowed_categories), category)
        stg_q.fail(message, logger=logger)
        raise Exception(message)
            
    else:
        stg_input = stg_q.stg_input
        input_tbl = stg_input.name
        now_hr = now.strftime("%Y%m%d%H%M%S")
        
        # grab helper functions
        from pyhcup.db import pg_wtl_shovel, pg_shovel
        
        # this is an allowed category of staging
        in_src = stg_input.category
        
        # get a connection and cursor object for use with db.* functions
        cnxn = get_pgcnxn()
        cursor = cnxn.cursor()
        
        # set aside info about the related ImportQueue object
        try:
            state = stg_input.state
            load = stg_input.imported_via
            meta = load.get_meta()
            year = stg_input.year
        except:
            if 'stg_tx' in input_tbl:
                state = 'TX'
                year = input_tbl.split('_')[2]
            else:
                raise
        
        year = stg_input.year
        
        # generate the destination table name
        output_tbl = '_'.join(str(x) for x in ['stg', state, year, category, now_hr]).lower()
        stg_q.log('output_tbl: %s' % output_tbl,
                  level='INFO', logger=logger)
        
        staged = StagingTable(
            parent = stg_input,
            name = output_tbl,
            category = category,
            records = 0
        )
        staged.save()
        stg_q.log('StagingTable %s recorded with pk %s' % (staged.name, staged.pk),
                  level='INFO', logger=logger)
        
        if category == 'CHARGES':
            if in_src != 'CHARGES_SOURCE':
                message = "Input StagingTable category must be CHARGES_SOURCE for CHARGES staging. Got %s." % in_src
                stg_q.fail(message, logger=logger)
                raise Exception(message)
            
            # create a table using "static" long charges definition
            create_sql = pyhcup.db.long_table_sql(output_tbl, 'CHGS')
            cursor.execute(create_sql)
            cnxn.commit()
            
            # check whether this load was wide or long
            if not meta_is_long(meta):
                # wide charges should get wide-to-long shoveled
                stg_q.log('This is a wide-to-long staging from CHARGES_SOURCE to CHARGES',
                          level='INFO', logger=logger)
                
                affected_rows = pg_wtl_shovel(cnxn, meta, 'CHGS', input_tbl, output_tbl)
                #logger.info('Inserted contents of staging table %s to master table %s (%s rows): %s' % (staging[0], table, affected_rows, load))
                shoveled_message = 'Moved and pivoted wide charges from %s to long charges table %s (%s rows)' % (input_tbl, output_tbl, affected_rows)
                
            else:
                # this is a straight-up shovel from long CHARGES_SOURCE to CHARGES
                stg_q.log('This is a long-to-long staging from CHARGES_SOURCE to CHARGES',
                          level='INFO', logger=logger)
                
                """
                fields_in = [x for x in meta.field if x.lower() not in ['state', 'year']]
                fields_out = [pyhcup.parser.lm_reverse('CHGS', x)
                              for x in meta.field
                              if x.lower() not in ['state', 'year'] and
                              pyhcup.parser.lm_reverse('CHGS', x) is not False
                              ]
                """
                
                from pyhcup.parser import lm_reverse
                fields_in = [x for x in meta.field if lm_reverse('CHGS', x) is not False]
                fields_out = [
                    lm_reverse('CHGS', x)
                    for x in meta.field
                    if lm_reverse('CHGS', x) is not False
                ]
                
                # these are allowable fields that won't map with lm_reverse
                id_fields = ['KEY', 'STATE', 'YEAR']
                
                all_allowed = fields_in + id_fields
                unaccounted_for = meta[ ~meta.field.isin(all_allowed) ]
                
                if len(unaccounted_for) > 0:
                    raise Exception("Some fields were unaccounted for, and the long-to-long move could not be completed. (What are %s?)" % ', '.join(unaccounted_for.field))
                
                # would normally add state and year columns here,
                # but they should be pulled by virtue of scalars
                fields_in.append('KEY')
                fields_out.append('KEY')
                
                affected_rows = pg_shovel(cnxn, input_tbl, output_tbl, fields_in, fields_out,
                                          scalars={'STATE':state, 'YEAR':year})
                shoveled_message = 'Moved long charges from %s to long charges table %s (%s rows)' % (input_tbl, output_tbl, affected_rows)
                
        elif category == 'DX':
            if in_src != 'CORE_SOURCE':
                message = "Input StagingTable category must be CORE_SOURCE for DX staging. Got %s." % in_src
                stg_q.fail(message, logger=logger)
                raise Exception(message)
            
            # create a table using "static" long DX definition
            create_sql = pyhcup.db.long_table_sql(output_tbl, 'DX')
            cursor.execute(create_sql)
            cnxn.commit()
            
            stg_q.log('This is a wide-to-long staging from CORE_SOURCE to DX',
                        level='INFO', logger=logger)
            affected_rows = pg_wtl_shovel(cnxn, meta, 'DX', input_tbl, output_tbl)
            shoveled_message = 'Moved and pivoted wide core table %s to long DX table %s (%s rows)' % (input_tbl, output_tbl, affected_rows)
                
        elif category == 'PR':
            if in_src != 'CORE_SOURCE':
                message = "Input StagingTable category must be CORE_SOURCE for PR staging. Got %s." % in_src
                stg_q.fail(message, logger=logger)
                raise Exception(message)
            
            # create a table using "static" long PR definition
            create_sql = pyhcup.db.long_table_sql(output_tbl, 'PR')
            cursor.execute(create_sql)
            cnxn.commit()
            
            stg_q.log('This is a wide-to-long staging from CORE_SOURCE to PR',
                        level='INFO', logger=logger)
            affected_rows = pg_wtl_shovel(cnxn, meta, 'PR', input_tbl, output_tbl)
            shoveled_message = 'Moved and pivoted wide core table %s to long PR table %s (%s rows)' % (input_tbl, output_tbl, affected_rows)
        
        elif category == 'UFLAGS':
            if in_src != 'CORE_SOURCE':
                message = "Input StagingTable category must be CORE_SOURCE for UFLAGS staging. Got %s." % in_src
                stg_q.fail(message, logger=logger)
                raise Exception(message)
            
            if stg_q.charges_input is None or stg_q.charges_input.category != 'CHARGES':
                message = "Must provide charges_input StagingTable with category CHARGES for UFLAGS staging."
                stg_q.fail(message, logger=logger)
                raise Exception(message)
            else:
                charges_tbl = stg_q.charges_input.name
            
            if stg_q.pr_input is None or stg_q.pr_input.category != 'PR':
                message = "Must provide pr_input StagingTable with category PR for UFLAGS staging."
                stg_q.fail(message, logger=logger)
                raise Exception(message)
            else:
                pr_tbl = stg_q.pr_input.name
            
            
            # create a table using "static" long PR definition
            create_sql = pyhcup.db.long_table_sql(output_tbl, 'UFLAGS')
            cursor.execute(create_sql)
            cnxn.commit()
            
            stg_q.log('uflag staging into %s from CORE_SOURCE %s, PR %s, and CHARGES %s' % (output_tbl, input_tbl, pr_tbl, charges_tbl),
                      level='INFO', logger=logger)
            
            # get a list of UtilizationFlagger objects from PyHCUP
            # these are built using HCUP's uflag definitions
            flaggers = pyhcup.default_uflaggers(state=state, year=year)
            affected_rows = 0
            
            for uf in flaggers:
                # take advantage of in-database processing for these
                stg_q.log('%s: processing' % uf.name)
                uflag_sql = uf.sql(output_tbl, input_tbl, pr_tbl, charges_tbl)
                cursor.execute(uflag_sql)
                uflag_count = cursor.rowcount
                affected_rows += uflag_count
                stg_q.log('%s: generated %s rows' % (uf.name, uflag_count))
            
            # commit all these inserts
            cnxn.commit()
            
            shoveled_message = 'Moved and pivoted wide core table %s to long PR table %s (%s rows)' % (input_tbl, output_tbl, affected_rows)
        
        elif category == 'CORE_PROCESSED':
            flaggers = pyhcup.default_uflaggers()
            uflag_names = [x.name for x in flaggers]
            
            if in_src != 'CORE_SOURCE':
                message = "Input StagingTable category must be CORE_SOURCE for CORE_PROCESSED staging. Got %s." % in_src
                stg_q.fail(message, logger=logger)
                raise Exception(message)
            else:
                tbl_core_source = input_tbl
                stg_q.log('Input StagingTable CORE_SOURCE: %s' % tbl_core_source, logger=logger)
                core_cols = map(lambda x: x.lower(), pg_getcols(cnxn, tbl_core_source))
            
            if stg_q.aha_input is not None:
                if stg_q.aha_input.category != 'AHALINK_SOURCE':
                    message = "If provided, aha_input must be StagingTable with category AHALINK_SOURCE for CORE_PROCESSED staging."
                    stg_q.fail(message, logger=logger)
                    raise Exception(message)
                else:
                    tbl_ahal_source = stg_q.aha_input.name
                    stg_q.log('Input StagingTable AHALINK_SOURCE: %s' % tbl_ahal_source, logger=logger)
                    ahal_cols = map(lambda x: x.lower(), pg_getcols(cnxn, tbl_ahal_source))
            else:
                tbl_ahal_source = None
            
            if stg_q.uflag_input is not None:
                if stg_q.uflag_input.category != 'UFLAGS':
                    message = "If provided, uflag_input must be StagingTable with category UFLAGS for CORE_PROCESSED staging."
                    stg_q.fail(message, logger=logger)
                    raise Exception(message)
                else:
                    tbl_uflags = stg_q.uflag_input.name
                    stg_q.log('Input StagingTable UFLAGS: %s' % tbl_uflags, logger=logger)
                    uflag_cols = map(lambda x: x.lower(), pg_getcols(cnxn, tbl_uflags))
            else:
                tbl_uflags = None
            
            if stg_q.dx_pr_grps_input is not None:
                if stg_q.dx_pr_grps_input.category != 'DX_PR_GRPS_SOURCE':
                    message = "If provided, dx_pr_grps_input must be StagingTable with category DX_PR_GRPS for CORE_PROCESSED staging."
                    stg_q.fail(message, logger=logger)
                    raise Exception(message)
                else:
                    tbl_dx_pr_grps = stg_q.dx_pr_grps_input.name
                    stg_q.log('Input StagingTable DX_PR_GRPS: %s' % tbl_dx_pr_grps, logger=logger)
                    dx_pr_grps_cols = map(lambda x: x.lower(), pg_getcols(cnxn, tbl_dx_pr_grps))
            else:
                tbl_dx_pr_grps = None
            
            if stg_q.severity_input is not None:
                if stg_q.severity_input.category != 'SEVERITY_SOURCE':
                    message = "If provided, severity_input must be StagingTable with category SEVERITY for CORE_PROCESSED staging."
                    stg_q.fail(message, logger=logger)
                    raise Exception(message)
                else:
                    tbl_severity = stg_q.severity_input.name
                    stg_q.log('Input StagingTable SEVERITY: %s' % tbl_severity, logger=logger)
                    severity_cols = map(lambda x: x.lower(), pg_getcols(cnxn, tbl_severity))            
            else:
                tbl_severity = None
            
            # scrub some extras, so we don't have duplicate columns
            omit_from_right = ['state', 'year', 'key'] + core_cols
            
            # check to see whether we need a separate dte table, based
            # on whether those columns are already in CORE_PROCESSED.
            if 'daystoevent' in core_cols and 'visitlink' in core_cols:
                # we do not need a dte_source
                # set it to None regardless of availability
                tbl_dte_source = None
            else:
                # we would really prefer a dte_source
                if stg_q.dte_input is None or stg_q.dte_input.category != 'DAYSTOEVENT_SOURCE':
                    logger.warning("CORE_SOURCE StagingTable {src} lacks daystoevent and visitlink columns, but no DAYSTOEVENT_SOURCE table was provided as dte_input or the provided input is not of category DAYSTOEVENT_SOURCE. Table generation will proceed, but no revisit analysis will be possible (CORE_PROCESSED table will lack daystoevent and visitlink columns).")
                    tbl_dte_source = None
                else:
                    # grab that table info
                    tbl_dte_source = stg_q.dte_input.name
                    stg_q.log('Input StagingTable DAYSTOEVENT_SOURCE: %s' % tbl_dte_source, logger=logger)
                    
                    # we also need to omit daystoevent and visitlink from core_cols in case one is in there somehow
                    core_cols = [i for i in core_cols if i.lower() not in ['daystoevent', 'visitlink']]
            
            
            # prepare a string for attaching JOIN clauses.
            # these might even be better if they were dictionaries with standardized keys
            # which could then generate the JOIN clauses after they were all collected.
            # for now, pure string building.
            jsql = ''
            
            select_items = ['tbl_core_source.{col}'.format(col=x) for x in core_cols]
            
            if tbl_dte_source is not None:
                select_items.append('tbl_dte_source.daystoevent AS daystoevent')
                select_items.append('tbl_dte_source.visitlink AS visitlink')
                jsql += """
                    LEFT JOIN {tbl_dte_source} AS tbl_dte_source
                    ON tbl_core_source.key = tbl_dte_source.key
                    """.format(tbl_dte_source=tbl_dte_source)

            # join in the ahalink cols
            if tbl_ahal_source is not None:
                ahal_sel_cols = [x for x in ahal_cols if x.lower() not in omit_from_right]
                
                for a in ahal_sel_cols:
                    select_items.append('tbl_ahal_source.{a} AS {a}'.format(a=a))
                
                #print ahal_cols
                if 'key' in ahal_cols:
                    ahal_join_field = 'key'
                else:
                    ahal_join_field = 'dshospid'
                
                jsql += """
                    LEFT JOIN {tbl_ahal_source} AS tbl_ahal_source
                    ON tbl_core_source.{ahal_join_field} = tbl_ahal_source.{ahal_join_field}
                    """.format(tbl_ahal_source=tbl_ahal_source, ahal_join_field=ahal_join_field)
            
            if tbl_severity is not None:
                # skip columns in omit_from_right (pk fields and CORE_SOURCE fields)
                
                for f in severity_cols:
                    if f.lower() not in omit_from_right:
                        select_items.append('tbl_severity.{f} AS {f}'.format(f=f))
                        
                jsql += """
                    LEFT JOIN {tbl_severity} AS tbl_severity
                    ON tbl_core_source.key = tbl_severity.key
                    """.format(tbl_severity=tbl_severity)
            
            if tbl_dx_pr_grps is not None:
                # skip columns in uflags
                # select in columns from tbl_dx_pr_grps
                # and prepare JOIN them
                
                for f in dx_pr_grps_cols:
                    # old way, where dx_pr_grps deferred to uflags
                    #if f.upper() not in uflag_names and f.lower() not in omit_from_right:
                    #    select_items.append('tbl_dx_pr_grps.{f} AS {f}'.format(f=f))
                    # new way, where uflags defers to dx_pr_grps
                    # due to truncation, especially in available pr and prccs, the provided
                    # uflags from HCUP cannot be completely recreated with source data
                    if f.lower() not in omit_from_right:
                        select_items.append('tbl_dx_pr_grps.{f} AS {f}'.format(f=f))
                        
                jsql += """
                    LEFT JOIN {tbl_dx_pr_grps} AS tbl_dx_pr_grps
                    ON tbl_core_source.key = tbl_dx_pr_grps.key
                    """.format(tbl_dx_pr_grps=tbl_dx_pr_grps)
            
            if tbl_uflags is not None:
                # specifically select in columns from tbl_uflags that match names
                # in pyhcup.default_uflaggers(), and prepare them as JOIN clauses
                
                for f in uflag_names:
                    if tbl_dx_pr_grps is None or f.lower() not in dx_pr_grps_cols:
                        select_items.append('tbl_{flag_name}.value AS {flag_name}'.format(flag_name=f))
                        jsql += """
                            LEFT JOIN {tbl_uflags} AS tbl_{flag_name}
                            ON tbl_{flag_name}.name = '{flag_name}' AND
                                tbl_core_source.key = tbl_{flag_name}.key
                            """.format(tbl_uflags=tbl_uflags, flag_name=f)
            
            # concat everything into a stonking huge SQL statement
            full_sql = 'CREATE TABLE {output_tbl} AS\nSELECT {selects}\nFROM {tbl_core_source} AS tbl_core_source {joins}' \
                .format(output_tbl=output_tbl, selects=',\n\t'.join(select_items), tbl_core_source=tbl_core_source, joins=jsql)
            
            # make it so
            cursor.execute(full_sql)
            affected_rows = cursor.rowcount
            
            # put a ring on it
            cnxn.commit()
            
            shoveled_message = 'Generated CORE_PROCESSED table %s (%s rows)' % (output_tbl, affected_rows)
            staged.description = 'SQL used to create table\n\n#####\n\n' + full_sql
            staged.save()
            
        stg_q.log(shoveled_message, level='INFO', logger=logger)

        # record the new table in a StagingTable object
        staged.records = affected_rows
        staged.wip = False
        staged.save()
        stg_q.success('StagingTable %s (pk %s) updated as non-WIP and %s rows' % (staged.name, staged.pk, staged.records))
        
        # save a reference to the StagingTable in the StagingQueue object as output
        stg_q.stg_output = staged
        stg_q.save()
        stg_q.success('StagingTable {tbl} (pk {tbl_pk}) saved as stg_output for StagingQueue object {stg}' \
            .format(tbl=staged.name, tbl_pk=staged.pk, stg=stg_q.pk))

        logger.info('Seeking deprecated StagingTable objects to mark as void (looking for category {cat}, state {st}, year {yr}, with pk NOT {pk})' \
            .format(cat=staged.category, st=staged.state, yr=staged.year, pk=staged.pk))
        deprecate_qs = StagingTable.objects \
            .filter(category=staged.category, wip=False, void=False) \
            .exclude(pk=staged.pk)
        deprecate_lst = filter(lambda x: x.state==staged.state and x.year==staged.year, deprecate_qs)
        for d in deprecate_lst:
            logger.info('Deprecating StagingTable object {stg_pk} ({stg_name})' \
                .format(stg_pk=d.pk, stg_name=d.name))
            d.void = True
            d.save()
        
        return True


@celery.shared_task(bind=True, ignore_result=True)
def batch_stage(self, batch_id):
    """Attempts to stage the indicated batch"""
    
    batch = StagingBatch.objects.get(pk=batch_id)
    batch.status = 'RECEIVED'
    batch.celery_task_id = self.request.id
    batch.save()
    
    enqueued = StagingQueue.objects.filter(batch=batch)
    logger.info('Found %s' % (batch))
    
    if batch.complete:
        response = 'Batch %i was previously completed at %s, and therefore will not be run' % (batch.pk, batch.complete)
        logger.error(response)
        batch.fail()
        return False
    
    elif enqueued.count() < 1:
        response = 'Batch %i has no items enqueued, and therefore will not be run' % batch.pk
        logger.warning(response)
        batch.fail()
        return True

    else:
        batch_begin = datetime.datetime.utcnow().replace(tzinfo=utc)
        batch.start = batch_begin
        batch.status = 'IN PROCESS'
        batch.save()
        logger.info('Begin batch %s' % (batch))
        
        job = celery.group(
            stage_dispatch.si(stg.pk) for stg in enqueued
            )
        job()
        
        # put a task into background for periodic check that the batch has completed
        stagebatch_complete.apply_async((batch.pk,), countdown=600)
        
        return True


@celery.shared_task(bind=True, max_retries=None, default_retry_delay=900)# default_retry_delay=60)
def stagebatch_complete(self, batch_pk):
    """Checks to see if each item in the StagingBatch has a completion timestamp in db, and updates batch db entry to reflect success/failure of overall batch.
    """
    
    # grab the django representation of this ImportBatch
    b = StagingBatch.objects.get(pk=batch_pk)
    
    # and, while we're at it, the associated ImportQueue objects
    enqueued = StagingQueue.objects.filter(batch=b)
    
    try:
        # test if all completed, one way or another
        if all(q.complete is not None for q in enqueued):
            
            # test if the outcomes were all SUCCESS
            if all(q.successful() for q in enqueued):
                b.success()
                logger.info('Batch completed successfully: %s' % b)
                return True
            else:
                b.fail()
                logger.error('One or more imports failed: %s' % b)
                return False
        else:
            # since some haven't completed yet, raise IncompleteStream and retry
            raise celery.exceptions.IncompleteStream
    
    except celery.exceptions.IncompleteStream as exc:
        # try again a little later, when the streams are more complete
        raise self.retry(exc=Exception('Batch not yet complete: %s' % b))
