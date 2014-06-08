import logging
import traceback

from django.db.models.sql import EmptyResultSet
from django.utils import timezone

from silk.collector import DataCollector
from silk.config import SilkyConfig


Logger = logging.getLogger('silk')


def _should_wrap(sql_query):
    for ignore_str in SilkyConfig().SILKY_IGNORE_QUERIES:
        if ignore_str in sql_query:
            return False
    return True


def execute_sql(self, *args, **kwargs):
    """wrapper around real execute_sql in order to extract information"""
    if self.query.model.__module__ != 'silk.models':
        try:
            q, params = self.as_sql()
            if not q:
                raise EmptyResultSet
        except EmptyResultSet:
            if kwargs.get('result_type', 'multi') == 'multi':
                return iter([])
            else:
                return
        tb = ''.join(reversed(traceback.format_stack()))
        sql_query = q % params
        if _should_wrap(sql_query):
            query_dict = {
                'query': sql_query,
                'start_time': timezone.now(),
                'traceback': tb
            }
            try:
                return self._execute_sql(*args, **kwargs)
            finally:
                query_dict['end_time'] = timezone.now()
                request = DataCollector().request
                if request:
                    query_dict['request'] = request
                DataCollector().register_query(query_dict)
    return self._execute_sql(*args, **kwargs)