# core Python packages
import datetime
import logging
import os
import sys
import psycopg2


# third party packages
import pandas as pd
import pyhcup


# django packages
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.timezone import utc
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db import connections as cnxns
from django.db import transaction as tx


# local project and app packages
from djhcup_integration.models import Edition, Definition, Column, ColumnName, IntegrationTable, IntTblStgTblMembers, MappedColumn


# sister app stuff
from djhcup_staging.models import DataSource, StagingTable, File
from djhcup_staging.utils.misc import dead_batches, get_pgcnxn


# start a logger
logger = logging.getLogger('default')


def integrate_tables(definition_pk, edition_pk, indexes=['key', 'state', 'year', 'visitlink']):
    """
    Creates a new table integration using provided definition and edition.
    
    TODO: Consider how much, if any, of these things should be preserved
    as provenance somewhere, somehow. Is description field appropriate?
    Alternatively, maybe a logging filter could be used, or an
    additional handler, that sends certain provenance items away for
    safekeeping.
    """
    logger.debug("integrate_tables() called with definition_pk {d} and edition_pk {e}" \
        .format(d=definition_pk, e=edition_pk)
    )
    
    try:
        # grab the definition for which we'll make an integration table
        d = Definition.objects.get(pk=definition_pk)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist("Function integrate_tables() was unable to find Definition with primary key %s" % definition_pk)
    
    try:
        e = Edition.objects.get(pk=edition_pk)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist("Function integrate_tables() was unable to find Edition with primary key %s" % edition_pk)
    
    
    cnxn = get_pgcnxn()

    # use the Edition timestamp for table names and the like down the line
    now = e.created_at.strftime("%Y%m%d%H%M%S")
    
    # get the integration Columns we'll shop for among StagingTables
    def_cols = Column.objects.filter(definition=d)
    logger.debug("Columns in Definition: %s" % ', '.join([str(x) for x in def_cols]))
    
    # create the empty table
    tbl_clauses = []
    for dcol in d.columns.all():
        # construct a clause representing this column, based on its name and data type
        clause = "{f} {type}".format(f=dcol.field_out.value, type=dcol.field_out_data_type)
        
        # only append the clause if it doesn't already exist in the clauses list
        # (avoids duplicates)
        if clause not in tbl_clauses:
            tbl_clauses.append(clause)
    
    int_tbl_name = 'int_{ds_parent}_{cat}_{now}'.format(
        ds_parent=d.data_source.mr_descriptor,
        cat=d.category,
        now=now,
    )
    logger.info("Creating new database table {tbl} for table integration" \
        .format(tbl=int_tbl_name))
    create = "CREATE TABLE {tbl} ({clauses});" \
        .format(tbl=int_tbl_name, clauses=", ".join(tbl_clauses))
    cursor = cnxn.cursor()
    cursor.execute(create)
    cnxn.commit()
    logger.info("Created new database table {tbl}" \
        .format(tbl=int_tbl_name))
    
    logger.info("Creating new IntegrationTable object for table {tbl}" \
        .format(tbl=int_tbl_name))
    # create a new IntegrationTable to hold results and meta
    int_tbl = IntegrationTable(
        name=int_tbl_name,
        definition=d,
        edition=e
    )
    int_tbl.save()
    logger.info("Created new IntegrationTable object for table {tbl}" \
        .format(tbl=int_tbl_name))
    
    logger.info("Checking for indexes to add to table {tbl}" \
        .format(tbl=int_tbl_name))
    for i in indexes:
        logger.info("Attempting to create index on column {i} in table {tbl}" \
            .format(i=i, tbl=int_tbl_name))
        try:
            i_sql = pyhcup.db.index_sql(str(i), int_tbl_name)
            cursor.execute(i_sql)
            cnxn.commit()
            logger.info("Created index on column {i} in table {tbl}" \
                .format(i=i, tbl=int_tbl_name))
        except:
            logger.warning("Failed to create index on column {i} in table {tbl}" \
                .format(i=i, tbl=int_tbl_name))
            cnxn.rollback()
    
    # get StagingTables to be included in this integration
    # according to category indicated by Definition
    stgtbls = StagingTable.objects \
                .filter(category=d.category, wip=False, void=False) \
                .order_by('-created_at') # most recent first
    
    # extra filter step to make sure these are all in the same family.
    # this cannot be combined with above since this is a property,
    # rather than a model column
    stgtbls = filter(
        lambda x: x.data_source.parent == d.data_source,
        stgtbls
    )
    
    integrated_sy = []
    shoveled_lst = []
    for sttbl in stgtbls:
        # put a check in here to make sure
        # we do not double-add.
        state = sttbl.state
        year = sttbl.year
        sy = dict(state=state, year=year)
        if sy in integrated_sy:
            # do not proceed
            logger.info("StagingTable {st_pk} ({tbl}) will be omitted, as {st} {yr} have already been integrated" \
                .format(st_pk=sttbl.pk, st=state, yr=year, tbl=sttbl.name)
            )
        else:
            logger.info("Integrating StagingTable {st_pk} ({tbl})" \
                .format(st_pk=sttbl.pk, tbl=sttbl.name)
            )
            integrated_sy.append(sy)
        
            st_cols = [s.lower() for s in pyhcup.db.pg_getcols(cnxn, sttbl.name)]
            
            int_member = IntTblStgTblMembers(
                integrationtable = int_tbl,
                stagingtable = sttbl,
            )
            int_member.save()
            fields_in_lst = []
            fields_out_lst = []
            
            for c in st_cols:
                matches = d.columns.filter(fields_in__value__iexact=c)
                if len(matches) == 1:
                    matched_col = matches[0]
                    matched_cn = ColumnName.objects.filter(fields_in=matched_col, value__iexact=c)[0]
                    mapped_col = MappedColumn(
                        inttblstgtblmembers=int_member,
                        column=matched_col,
                        matched_in=matched_cn)
                    mapped_col.save()
                    fields_in_lst.append(c)
                    fields_out_lst.append(matched_cn.value)
                else:
                    logger.debug(
                        "Unable to resolve {sttbl}.{c}; skpping".format(
                            sttbl=sttbl.name,
                            c=c
                        )
                    )
        
            
            # shovel the resolved columns from source to integration table
            shoveled = pyhcup.db.pg_shovel(cnxn, tbl_source=sttbl.name, tbl_destination=int_tbl.name, fields_in=fields_in_lst, fields_out=fields_out_lst)
            shoveled_lst.append(dict(
                state=state,
                year=year,
                shoveled=shoveled,
                StagingTable=sttbl,
                fields_in=fields_in_lst,
                fields_out=fields_out_lst
            ))
            
            logger.info("Shoveled {ct} rows from StagingTable {st_pk} ({tbl})" \
                .format(ct=shoveled, st_pk=sttbl.pk, tbl=sttbl.name)
            )
            
            logger.debug(
                "TABLE: {tbl}\nROWS: {rows}\nFIELDS IN: {fields_in}\nFIELDS OUT: {fields_out}" \
                    .format(
                        tbl=sttbl,
                        rows=shoveled,
                        fields_in=fields_in_lst,
                        fields_out=fields_out_lst
                    )
            )
    
    # log a summary about the entire enterprise
    total_shoveled = sum([x['shoveled'] if 'shoveled' in x else 0 for x in shoveled_lst])
    logger.info("Integrated a total of {total} rows from {ct} tables" \
        .format(total=total_shoveled, ct=len(shoveled_lst))
    )
    
    # record some details in the integration table description
    int_tbl.description = 'Integration of {ds} {category} as of {now}\n\nDIGEST\n##########\n\n' \
        .format(ds=d.data_source, category=d.category, now=now)
    int_tbl.description += '\n\n'.join([
        "State: {st}\nYear: {yr}\nTable in: {tbl}\nRows moved: {rows}\nFields in: {fields_in}\nFields out: {fields_out}" \
            .format(
                st=x['state'],
                yr=x['year'],
                tbl=str(x['StagingTable']),
                rows=x['shoveled'],
                fields_in=x['fields_in'],
                fields_out=x['fields_out'],
            )
        for x in shoveled_lst
    ])
    int_tbl.wip = False
    int_tbl.save()
    
    return int_tbl



# deprecated; ran up against max 1600 column limit in PostgreSQL
def master_table(ds_id, category, timestamp=None, extra=None):
    """
    Generates a master table for the DataSource corresponding to ds_id. Returns an IntegrationTable.
    
    Uses all known loadfiles for source and generates one master table.
    """
    
    source = DataSource.objects.get(pk=ds_id)
    logger.info('Attempting to generate master table for %s' % source)
    
    cursor = cnxns[DJHCUP_DB_ENTRY].cursor()

    # need later for table creation, but want the value to be based on the start of the process
    if timestamp == None:
        timestamp = datetime.datetime.utcnow().replace(tzinfo=utc).strftime("%Y%m%d%H%M%S")
    
    db_table = "int_%s_%s_%s" % (source.mr_descriptor, category, timestamp)
    db_table = db_table.lower()
    pk_fields = []
    index_fields = []
    
    # check to see whether this source has a LONG_MAPS entry, which would indicate it ought to be a long table
    if source.abbreviation in pyhcup.parser.LONG_MAPS.keys():
        logger.warning("The indicated data source has an analog in pyhcup.parser.LONG_MAPS. Generation will proceed, but this may indicate an error.")
    
    src_loadfiles = File.objects.filter(
        file_type__content_type__in=['LOAD'],
        file_type__source=source
    )
    logger.info('Found %d loadfile records matching source' % len(src_loadfiles))
    
    meta_list = []
    excluded = []
    for lf in src_loadfiles:
        mdf = pyhcup.sas.meta_from_sas(lf.full_path)
        augmented = pyhcup.meta.augment(mdf)
        meta_list.append(augmented)
    
    merged_meta = pyhcup.meta.merge(meta_list)
    logger.info('Merged %d meta DataFrames successfully, with %d columns after de-duplication' % (len(meta_list), len(merged_meta)))
    
    constraints = ['NULL']
    pk_fields = ['year', 'state', 'key']
    index_fields += pk_fields
    
    create_sql = pyhcup.db.table_sql(
        merged_meta, db_table, pk_fields=pk_fields, ine=True,
        append_state=True, default_constraints=constraints
    )
        
    try:
        cursor.execute(create_sql)
        tx.commit(using=DJHCUP_DB_ENTRY)
    except:
        e = sys.exc_info()[0]
        raise Exception("Failed to create master table with query %s (%s)" % (create_sql, e))
    
    logger.info('Created master table %s with on database %s' % (db_table, DJHCUP_DB_ENTRY))
    
    if category in EXTRA_COLUMNS.keys():
        # clean out any columns that will be added back on
        # re-add them with proper definitions
        for c in EXTRA_COLUMNS[category]:
            dropif_sql = 'ALTER TABLE {t} DROP COLUMN IF EXISTS {c};' \
                .format(t=db_table, c=c['field'])
            add_sql = 'ALTER TABLE {t} ADD COLUMN {c} {coltype};' \
                .format(t=db_table, c=c['field'], coltype=c['type'])
            logger.info('Dropping column if exists: {c}' \
                .format(c=c['field']))
            cursor.execute(dropif_sql)
            logger.info('Adding column: {c} {coltype}' \
                .format(c=c['field'], coltype=c['type']))
            cursor.execute(add_sql)
        
        tx.commit(using=DJHCUP_DB_ENTRY)
    
    
    if index_fields != None:
        try:
            for col in index_fields:
                index = pyhcup.db.index_sql(col, db_table)
                cursor.execute(index)
                tx.commit(using=DJHCUP_DB_ENTRY)
                logger.info('Created index for column %s with on table %s' % (col, db_table))
        except:
            raise Exception("Failed to create indexes on table, particularly one that should have resulted from this query: %s" % index)
    
    table_record = IntegrationTable(
        data_source=source,
        name=db_table,
        database=DJHCUP_DB_ENTRY,
        category=category
    )
    table_record.save()
    logger.info('Saved master table details as IntegrationTable record %d' % table_record.pk)
    
    return table_record
