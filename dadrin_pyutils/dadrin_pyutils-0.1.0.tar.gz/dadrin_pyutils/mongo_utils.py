from pymongo.mongo_client import MongoClient

import pymongo
import logging

__author__ = 'Lluis Canet'

def get_mongo_client(config, section):
    """
    Get mongo_client from ConfigParser
    input:
        config : ConfigParser instance
        section: ConfigParser section containing MongoDB IP and Port
    """
    mongo_ip = config.get(section, 'mongo_ip')
    mongo_port = config.getint(section, 'mongo_port')

    return MongoClient(mongo_ip, mongo_port)

def save_to_mongo(df, client, db_name, col_name):
    """
    Save data rows in a Dataframe to MongoDB
    inputs:
        df: Dataframe
        client: Initialized MongoDB client
        db_name: Name of the database where we want to include our data
        col_name: Name of the collection where we want to add our data

    """
    db = client[db_name]
    for row in df.iterrows():
        db[col_name].insert(row[1].to_dict())
    logging.info('Added %d elements to Mongo DB' % (len(df)))

def update_to_mongo(df, client, db_name, col_name, index, upsert=True):
    """
    Update data rows in a Dataframe to MongoDB
    inputs:
        df: Dataframe
        client: Initialized MongoDB client
        db_name: Name of the database where we want to include our data
        col_name: Name of the collection where we want to add our data
        index: Index of the data frame that will be used as search criteria for replacement

    """
    df_store = df.reset_index()
    df_store.set_index(index, inplace=True)
    db = client[db_name]
    for row in df_store.iterrows():
        row_keys = row[0]
        if type(row_keys) is not tuple:
            row_keys = [(row_keys)]
        key_dict = dict(zip(index, row_keys))
        row_content = row[1].to_dict()
        db[col_name].update(key_dict, {'$set': row_content, '$currentDate': {'lastModified': True}}, upsert)
    logging.info('Updated %d elements to Mongo DB' % (len(df_store)))


def transfer_documents(source_client, source_db, source_col, destin_client, destin_db, destin_col):
    """
    Transfer all documents from a collection in a MongoDB instance to another collection in another MongoDB instance
    inputs:
        source_client : Source pyMongo client
        source_db : Name of source DB
        source_col : Name of source collection
        destin_client : Destination pyMongo client
        destin_db : Name of destination DB
        destin_col : Name of destination collection
    """
    src_db = source_client[source_db]
    src_col = src_db[source_col]
    dest_db = destin_client[destin_db]
    dest_col = dest_db[destin_col]
    for document in src_col.find():
        dest_col.insert(document)