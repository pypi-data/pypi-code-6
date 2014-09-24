#coding:utf-8
'''
Created on 06.04.2011

@author: kamashev
'''

import os, sqlite3

from m3.helpers import logger

def create_sqlite_from_sql(sql_text_path, db_ready_path):
    '''
    Запускает команды из SQL-файла
    @param db_ready_path: путь и файл базы данных
    '''
    def compose_queries(file_data):
        query_queue = []
        cache = ""
        for line in file_data:
            line = line.strip()
            cache += line
            if line.endswith(";"): #конец запроса
                query_queue.append(cache)
                cache = ""
        return query_queue
    
    if not os.path.exists(sql_text_path):
        return False
    connection = sqlite3.connect(db_ready_path)
    cursor = connection.cursor()
    file_data = open(sql_text_path).read() or ""
    file_data = file_data.split("\n")
    query_queue = compose_queries(file_data)

    for query in query_queue:
        try:
            cursor.execute(query)
        except Exception, err:
            logger.exception(err.message)
            raise Exception(u"Не удалось выполнить запрос %s" % query)
    cursor.close()
    connection.commit()
    connection.close()
