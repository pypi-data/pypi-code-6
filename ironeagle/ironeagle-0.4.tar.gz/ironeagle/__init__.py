from cassandra.concurrent import execute_concurrent_with_args

import pandas

def save_dataframe_to_cassandra(session, dataframe, table, types=None):
    """

    :param session:
    :type session: cassandra.cluster.Session
    :param dataframe:
    :type dataframe: pandas.DataFrame
    :param table:
    :return:
    """


    statement = get_prepared_statement(dataframe, table)

    prepared = session.prepare(statement)

    dataframe = dataframe.where(dataframe.notnull(), None)

    def dgenerator():
        for x in dataframe.itertuples(index=False):
            yield x

    execute_concurrent_with_args(session, prepared, dgenerator())

def get_prepared_statement(dataframe, table):
    """

    :param session:
    :param dataframe:
    :type dataframe pandas.DataFrame
    :param table:
    :return:
    """
    keys = dataframe.keys()

    str_keys = ", ".join(keys)

    placeholders = ",".join(["?"] * len(keys))

    stmt = "INSERT INTO %s (%s) VALUES (%s)" % (table, str_keys, placeholders)

    return stmt


