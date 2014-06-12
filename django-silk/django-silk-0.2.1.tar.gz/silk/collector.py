from threading import local

from six import with_metaclass

from silk import models
from silk.config import SilkyConfig
from silk.errors import SilkNotConfigured, SilkInternalInconsistency
from silk.models import _time_taken
from silk.singleton import Singleton

TYP_SILK_QUERIES = 'silk_queries'
TYP_PROFILES = 'profiles'
TYP_QUERIES = 'queries'


class DataCollector(with_metaclass(Singleton, object)):
    """
    Provides the ability to save all models at the end of the request. We cannot save during
    the request due to the possibility of atomic blocks and hence must collect data and perform
    the save at the end.
    """

    def __init__(self):
        super(DataCollector, self).__init__()
        self.local = local()
        self._configure()

    @property
    def request(self):
        return getattr(self.local, 'request', None)

    def get_identifier(self):
        self.local.temp_identifier += 1
        return self.local.temp_identifier

    @request.setter
    def request(self, value):
        self.local.request = value

    def _configure(self):
        self.local.objects = {}
        self.local.temp_identifier = 0

    @property
    def objects(self):
        return getattr(self.local, 'objects', None)

    @property
    def queries(self):
        return self._get_objects(TYP_QUERIES)

    @property
    def silk_queries(self):
        return self._get_objects(TYP_SILK_QUERIES)

    def _get_objects(self, typ):
        objects = self.objects
        if objects is None:
            self._raise_not_configured('Attempt to access %s without initialisation.' % typ)
        if not typ in objects:
            objects[typ] = {}
        return objects[typ]

    @property
    def profiles(self):
        return self._get_objects(TYP_PROFILES)

    @property
    def silk_queries(self):
        return self._get_objects('silk_queries')

    def configure(self, request=None):
        self.request = request
        self._configure()

    def clear(self):
        self.request = None
        self._configure()

    def _raise_not_configured(self, err):
        raise SilkNotConfigured(err + ' Is the middleware installed correctly?')

    def register_objects(self, typ, *args):
        for arg in args:
            ident = self.get_identifier()
            objects = self.objects
            if objects is None:
                # This can happen if the SilkyMiddleware.process_request is not called for whatever reason.
                # Perhaps if another piece of middleware is not playing ball.
                self._raise_not_configured('Attempt to register object of type %s without initialisation. ')
            if not typ in objects:
                self.objects[typ] = {}
            self.objects[typ][ident] = arg

    def register_query(self, *args):
        self.register_objects(TYP_QUERIES, *args)

    def register_profile(self, *args):
        self.register_objects(TYP_PROFILES, *args)

    def _record_meta_profiling(self):
        if SilkyConfig().SILKY_META:
            num_queries = len(self.silk_queries)
            query_time = sum(_time_taken(x['start_time'], x['end_time']) for _, x in self.silk_queries.items())
            self.request.meta_num_queries = num_queries
            self.request.meta_time_spent_queries = query_time
            self.request.save()

    def finalise(self):
        for _, query in self.queries.items():
            query_model = models.SQLQuery.objects.create(**query)
            query['model'] = query_model
        for _, profile in self.profiles.items():
            profile_query_models = []
            if TYP_QUERIES in profile:
                profile_queries = profile[TYP_QUERIES]
                del profile[TYP_QUERIES]
                for query_temp_id in profile_queries:
                    try:
                        query = self.queries[query_temp_id]
                        try:
                            profile_query_models.append(query['model'])
                        except KeyError:
                            raise SilkInternalInconsistency('Profile references a query dictionary that has not '
                                                            'been converted into a Django model. This should '
                                                            'never happen, please file a bug report')
                    except KeyError:
                        raise SilkInternalInconsistency('Profile references a query temp_id that does not exist. '
                                                        'This should never happen, please file a bug report')
            profile = models.Profile.objects.create(**profile)
            if profile_query_models:
                profile.queries = profile_query_models
                profile.save()
        self._record_meta_profiling()

    def register_silk_query(self, *args):
        self.register_objects(TYP_SILK_QUERIES, *args)