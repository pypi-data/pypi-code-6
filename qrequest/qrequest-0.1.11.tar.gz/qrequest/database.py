import json
import os
import re
import io
import csv
import sys


def construct_dict(cursor):
    """ transforms the db cursor rows from table format to a
        list of dictionary objects
    """
    rows = cursor.fetchall()
    return [dict((cursor.description[i][0], value) for i, value in enumerate(row))
            for row in rows]


def construct_list(cursor):
    """ transforms the db cursor into a list of records,
        where the first item is the header
    """
    header = [h[0] for h in cursor.description]
    data = cursor.fetchall()
    return header, data


def construct_csv(cursor):
    """ transforms the db cursor rows into a csv file string
    """

    header, data = construct_list(cursor)
    # python 2 and 3 handle writing files differently
    if sys.version_info[0] <= 2:
        output = io.BytesIO()
    else:
        output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(header)
    for row in data:
        writer.writerow(row)

    return output.getvalue()


def build_settings(sql_path, settings_filename):
    """ returns a dictionary with the db connection settings and a list of
        queries
    """
    with open(os.path.join(sql_path, settings_filename)) as sf:
        settings = json.load(sf)

    # get a list of all directories in the sql folder
    site_names = next(os.walk(sql_path))[1]
    sites = {s: [f for f in os.listdir(os.path.join(sql_path, s))
                 if f[-4:] == '.sql']
             for s in site_names}

    return settings, sites


def load_query(sql_path, site_name, query_filename):
    with open(os.path.join(sql_path, site_name, query_filename)) as f:
        return f.read()


def get_params(sql_path, site_name, query_filename):
    """  returns a list of all the parameters in the sql file
    """
    query_text = load_query(sql_path, site_name, query_filename)
    return re.compile(r':(\w+)').findall(query_text)


def get_driver(driver_name):
    if driver_name == 'sqlite3':
        import sqlite3 as db_driver
    elif driver_name == 'cx_Oracle':
        import cx_Oracle as db_driver
    elif driver_name == 'psycopg2':
        import psycopg2 as db_driver
    elif driver_name == 'PyMySql':
        import PyMySql as db_driver
    elif driver_name == 'pyodbc':
        import pyodbc as db_driver
    else:
        # TODO: pick a better exception type and message
        raise ImportError
    return db_driver


def run_query(settings, sql_path, site_name, query_filename, params_dict, data_format='list'):
    # set up a db connection from the settings
    db_driver = get_driver(settings['sites'][site_name]['db_driver'])
    conn = db_driver.connect(settings['sites'][site_name]['db_connection_string'])
    cursor = conn.cursor()

    # convert the query which used named params into one with ? mark params
    query_text = load_query(sql_path, site_name, query_filename)
    query_params = get_params(sql_path, site_name, query_filename)
    for k in params_dict:
        query_text = query_text.replace(':' + k, '?')

    # run the query
    cursor.execute(query_text, [params_dict[p] for p in query_params])

    if data_format == 'list':
        # format into a table with header
        query_results = construct_list(cursor)
    elif data_format == 'dict':
        # format into dictionary
        query_results = construct_dict(cursor)
    elif data_format == 'csv':
        # format into dictionary
        query_results = construct_csv(cursor)
    else:
        query_results = None
    conn.close()

    return query_results