from .exceptions import InputDataError
import json


class TopicApiMixin(object):
    """Mixing class which encapsulates the functionality of the object API
    service.
    """

    #: Supported attributes for objects.
    TOPIC_ATTRIBUTES = set([
        'title', 'is_ready', 'override_managed_subscription',
        'noise_level', 'query', 'seeder', 'type', 'owner_id',
    ])

    #: Supported attributes for projects.
    FOLDER_ATTRIBUTES = set([
        'dashboard', 'default_search',
    ])

    #
    # Items
    #

    def get_items(self, project_id, **kwargs):
        """Returns items for the provided project.

        :param project_id: Project identifier.
        :param kwargs: Query parameters.
        :returns: A dict which contains the items for the project.

        Example::

            >>> client.get_items('2aEVClLRRA-vCCIvnuEAvQ', count=1)
            {u'count': 1,
             u'eof': False,
             u'items': [{u'created_at': u'2012-10-06T08:27:58',
                         u'id': u'haG6fhr9RLCm7ZKz1Meouw',
                         u'link': u'https://www.youtube.com/watch?v=Zzvhu42dWAc&feature=youtube_gdata',
                         u'read': True,
                         u'item_score': 0.5,
                         u'score': 0.56,
                         u'sources': [{u'id': u'oMNOQ-3rQo21q3UmaiaLHw',
                                       u'link': u'https://gdata.youtube.com/feeds/api/users/mymemonic/uploads',
                                       u'provider': u'feed',
                                       u'title': u'Uploads by mymemonic'},
                                      {u'id': u'H4nd0CasQQe_PMNDM0DnNA',
                                       u'link': None,
                                       u'provider': u'savedsearch',
                                       u'title': u'Squirro Alerts for "memonic"'}],
                         u'starred': False,
                         u'thumbler_url': u'22327aa6b6f4d2492346bed39ae354c0e94bf804/thumb/trunk/6f/87/f9/6f87f929773bd941d4a84209604ed014c7a21d7d.jpg',
                         u'title': u'Web Clipping - made easy with Memonic',
                         u'objects': [],
                         u'webshot_height': 360,
                         u'webshot_url': u'http://webshot.trunk.cluster.squirro.net.s3.amazonaws.com/6f/87/f9/6f87f929773bd941d4a84209604ed014c7a21d7d.jpg',
                         u'webshot_width': 480}],
             u'now': u'2012-10-11T14:39:54'}

        """

        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/projects/%(project_id)s/items'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id})

        res = self._perform_request('get', url, params=kwargs)
        return self._process_response(res)

    def get_item(self, project_id, item_id, **kwargs):
        """Returns the requested item for the provided project.

        :param project_id: Project identifier.
        :param item_id: Item identifier.
        :param kwargs: Query parameters.
        :returns: A dict which contains the individual item.

        Example::

            >>> client.get_project_item('2aEVClLRRA-vCCIvnuEAvQ', 'haG6fhr9RLCm7ZKz1Meouw')
            {u'item': {u'created_at': u'2012-10-06T08:27:58',
                       u'id': u'haG6fhr9RLCm7ZKz1Meouw',
                       u'link': u'https://www.youtube.com/watch?v=Zzvhu42dWAc&feature=youtube_gdata',
                       u'read': True,
                       u'item_score': 0.5,
                       u'score': 0.56,
                       u'sources': [{u'id': u'oMNOQ-3rQo21q3UmaiaLHw',
                                     u'link': u'https://gdata.youtube.com/feeds/api/users/mymemonic/uploads',
                                     u'provider': u'feed',
                                     u'title': u'Uploads by mymemonic'},
                                    {u'id': u'H4nd0CasQQe_PMNDM0DnNA',
                                     u'link': None,
                                     u'provider': u'savedsearch',
                                     u'title': u'Squirro Alerts for "memonic"'}],
                       u'starred': False,
                       u'thumbler_url': u'22327aa6b6f4d2492346bed39ae354c0e94bf804/thumb/trunk/6f/87/f9/6f87f929773bd941d4a84209604ed014c7a21d7d.jpg',
                       u'title': u'Web Clipping - made easy with Memonic',
                       u'objects': [],
                       u'webshot_height': 360,
                       u'webshot_url': u'http://webshot.trunk.cluster.squirro.net.s3.amazonaws.com/6f/87/f9/6f87f929773bd941d4a84209604ed014c7a21d7d.jpg',
                       u'webshot_width': 480}}

        """

        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/projects/%(project_id)s/items/%(item_id)s'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'item_id': item_id})

        res = self._perform_request('get', url, params=kwargs)
        return self._process_response(res)

    def modify_item(self, project_id, item_id, star=None, read=None,
                    keywords=None):
        """Adds per-user flags to a single item.

        :param project_id: Project identifier.
        :param item_id: Item identifier.
        :param star: Starred flag for the item, either `True` or `False`.
        :param read: Read flag for the item, either `True` or `False`.
        :param keywords: Dict of keyword-lists, pass in `None` as the
            dict-value to remove a keyword.

        Example::

            >>> client.modify_item('2aEVClLRRA-vCCIvnuEAvQ', 'haG6fhr9RLCm7ZKz1Meouw', star=True, read=False, keywords={'Canton': ['Berne'], 'Topic': None})

        """

        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/projects/%(project_id)s/items/%(item_id)s'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'item_id': item_id})

        # build item state
        state = {}
        if star is not None:
            state['starred'] = star
        if read is not None:
            state['read'] = read

        data = {'state': state}

        if not keywords is None:
            data['keywords'] = keywords

        headers = {'Content-Type': 'application/json'}

        res = self._perform_request(
            'put', url, data=json.dumps(data), headers=headers)
        self._process_response(res, [204])

    def delete_item(self, project_id, item_id, object_ids=None):
        """Deletes an item. If `object_ids` is provided the item gets not
        deleted but is de-associated from these objects.

        :param project_id: Project identifier.
        :param item_id: Item identifier.
        :param object_ids: Object identifiers from which the item is
            de-associated.

        Example::

            >>> client.delete_item('2aEVClLRRA-vCCIvnuEAvQ', 'haG6fhr9RLCm7ZKz1Meouw', object_ids=['object01'])
        """

        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/projects/%(project_id)s/items/%(item_id)s'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'item_id': item_id})

        # build params
        params = {}
        if object_ids:
            params['object_ids'] = ','.join(object_ids)

        res = self._perform_request('delete', url, params=params)
        self._process_response(res, [204])

    #
    # Objects
    #

    def get_user_objects(self, project_id, seeder=None, full=None):
        """Get all objects for the provided user.

        :param project_id: Folder identifier from which the objects should be
            returned. If it is not provided all objects are returned.
        :param seeder: Seeder name from which the objects shoule be returned.
        :param full: Include subscription and source details in the response.
        :returns: A list which contains the objects.

        Example::

            >>> client.get_user_objects(project_id='Sz7LLLbyTzy_SddblwIxaA')
            [{u'project_id': u'Sz7LLLbyTzy_SddblwIxaA',
              u'id': u'zFe3V-3hQlSjPtkIKpjkXg',
              u'is_ready': True,
              u'needs_preview': False,
              u'noise_level': None,
              u'seeder': u'team',
              u'title': u'Alexander Sennhauser',
              u'type': u'contact'}]

        """

        url = '%(ep)s/%(version)s/%(tenant)s' \
              '/projects/%(project_id)s/objects'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id})
        if full:
            url += '/full'

        # build params
        params = {}
        if seeder is not None:
            params['seeder'] = seeder

        res = self._perform_request('get', url, params=params)
        return self._process_response(res)

    def get_object(self, project_id, object_id):
        """Get object details.

        :param object_id: Object identifier.
        :returns: A dict which contains the object.

        Example::

            >>> client.get_object('2sic33jZTi-ifflvQAVcfw')
            {u'project_id': u'2aEVClLRRA-vCCIvnuEAvQ',
             u'id': u'2sic33jZTi-ifflvQAVcfw',
             u'is_ready': True,
             u'managed_subscription': False,
             u'needs_preview': False,
             u'noise_level': None,
             u'seeder': u'team',
             u'subscriptions': [u'3qTRv4W9RvuOxcGwnnAYbg',
                                u'hw8j7LUBRM28-jAellgQdA',
                                u'4qBkea4bTv-QagNS76_akA',
                                u'NyfRri_2SUa_JNptx0JAnQ',
                                u'oTvI6rlaRmKvmYCfCvLwpw',
                                u'c3aEwdz5TMefc_u7hCl4PA',
                                u'Xc0MN_7KTAuDOUbO4mhG6A',
                                u'y1Ur-vLuRmmzUNMi4xGrJw',
                                u'iTdms4wgTRapn1ehMqJgwA',
                                u'MawimNPKSlmpeS9YlMzzaw'],
             u'title': u'Squirro',
             u'type': u'organization'}

        """

        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/projects/%(project_id)s/objects/%(object_id)s' % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'object_id': object_id})

        res = self._perform_request('get', url)
        return self._process_response(res)

    def new_object(self, project_id, title, owner_id=None, seeder=None,
                   type=None, is_ready=None):
        """Create a new object.

        :param project_id: Folder identifier.
        :param title: Object title.
        :param owner_id: User identifier which owns the objects.
        :param seeder: Seeder which manages this object.
        :param type: Object type.
        :param is_ready: Object `is_ready` flag, either `True` or `False`.
        :returns: A dict which contains the project identifier and the
            new object identifier.

        Example::

            >>> client.new_object('H5Qv-WhgSBGW0WL8xolSCQ', '2aEVClLRRA-vCCIvnuEAvQ', 'Memonic', type='organization')
            {u'project_id': u'2aEVClLRRA-vCCIvnuEAvQ', u'id': u'2TBYtWgRRIa23h1rEveI3g'}

        """

        url = '%(ep)s/%(version)s/%(tenant)s/projects/%(project_id)s/objects' % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id})

        # build data
        data = {'title': title}
        user_values = locals()
        for key in self.TOPIC_ATTRIBUTES:
            if user_values.get(key) is not None:
                data[key] = user_values[key]

        res = self._perform_request('post', url, data=data)
        return self._process_response(res, [201])

    def modify_object(self, project_id, object_id,title=None,
                      is_ready=None, override_managed_subscription=None,
                      noise_level=None, query=None):
        """Modify a object.

        :param object_id: Object identifier.
        :param project_id: Project identifier for the object.
        :param title: New object title.
        :param is_ready: New object `is_ready` flag, either `True` for `False`.
        :param override_managed_subscription: New object
            `override_managed_subscription` flag, either `True` of `False`.
        :param noise_level: New object noise level. Can be any float value from
            0.0 to 1.0.
        :returns: A dict which contains the object.

        Example::

            >>> client.modify_object('2aEVClLRRA-vCCIvnuEAvQ', '2TBYtWgRRIa23h1rEveI3g', is_ready=False)
            {}

        """

        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/projects/%(project_id)s/objects/%(object_id)s' % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id, 'object_id': object_id})

        # build data
        data = {}
        user_values = locals()
        for key in self.TOPIC_ATTRIBUTES:
            if user_values.get(key) is not None:
                data[key] = user_values[key]

        headers = {'Content-Type': 'application/json'}

        res = self._perform_request(
            'put', url, data=json.dumps(data), headers=headers)
        return self._process_response(res, [201, 204])

    def delete_object(self, project_id, object_id):
        """Delete a object.

        :param project_id: Project identifier.
        :param object_id: Object identifier.

        Example::

            >>> client.delete_object('2aEVClLRRA-vCCIvnuEAvQ', '2TBYtWgRRIa23h1rEveI3g')

        """

        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/projects/%(project_id)s/objects/%(object_id)s' % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id, 'object_id': object_id})

        res = self._perform_request('delete', url)
        self._process_response(res, [204])

    #
    # Folders
    #

    def get_user_projects(self, owner_id=None, seeder=None,
                          include_objects=False):
        """Get projects for the provided user.

        :param owner_id: User identifier which owns the objects.
        :param seeder: Seeder of projects to return.
        :param include_objects: Whether to include object information, either
            `True` or `False`.
        :returns: A list of projects.

        Example::

            >>> client.get_user_projects()
            [{u'id': u'Sz7LLLbyTzy_SddblwIxaA',
              u'seeder': u'team',
              u'title': u'My Contacts',
              u'objects': 1,
              u'type': u'my contacts'},
             {u'id': u'2aEVClLRRA-vCCIvnuEAvQ',
              u'seeder': u'team',
              u'title': u'My Organizations',
              u'objects': 2,
              u'type': u'my organizations'}]

        """

        url = '%(ep)s/%(version)s/%(tenant)s/projects' % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant})

        # build params
        params = {'include_objects': include_objects}
        if owner_id is not None:
            params['owner_id'] = owner_id
        if seeder is not None:
            params['seeder'] = seeder

        res = self._perform_request('get', url, params=params)
        return self._process_response(res)

    def get_project(self, project_id):
        """Get project details.

        :param project_id: Folder identifier.
        :returns: A dict which contains the project.

        Example::

            >>> client.get_project('2aEVClLRRA-vCCIvnuEAvQ')
            {u'id': u'2aEVClLRRA-vCCIvnuEAvQ',
             u'seeder': u'team',
             u'title': u'My Organizations',
             u'type': u'my organizations'}

        """

        url = '%(ep)s/%(version)s/%(tenant)s/projects/%(project_id)s' % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id})

        res = self._perform_request('get', url)
        return self._process_response(res)

    def new_project(self, title, owner_id=None, seeder=None, locator=None):
        """Create a new project.

        :param title: Folder title.
        :param owner_id: User identifier which owns the objects.
        :param seeder: Seeder which manages this project.
        :param locator: Custom index locator configuration which is a `dict`
            which contains the `index_server` (full URI including the port for
            index server) and `project_index` (if `True` a project specific
            index is created, otherwise the default index is used) keys.
        :returns: A dict which contains the project identifier.

        Example::

            >>> locator = {'index_server': 'http://10.0.0.1:9200', 'project_index': True}
            >>> client.new_project('My Project', locator=locator)
            {u'id': u'gd9eIipOQ-KobU0SwJ8VcQ'}
        """

        url = '%(ep)s/%(version)s/%(tenant)s/projects' % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant})

        # build data
        data = {'title': title}
        if owner_id is not None:
            data['owner_id'] = owner_id
        if seeder is not None:
            data['seeder'] = seeder
        if locator is not None:
            data['locator'] = json.dumps(locator)

        res = self._perform_request('post', url, data=data)
        return self._process_response(res, [201])

    def modify_project(self, project_id, title=None, **kwargs):
        """Modify a project.

        :param project_id: Folder identifier.
        :param title: New project title.
        :param dashboard: JSON data structure for the dashboard.
        :param default_search: JSON data structure for the default search.
        :returns: A dict which contains the project.

        Example::

            >>> client.modify_project('gd9eIipOQ-KobU0SwJ8VcQ', title='My Other Folder')
            {}

        """
        url = '%(ep)s/%(version)s/%(tenant)s/projects/%(project_id)s' % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id})

        # build data
        data = {}
        for key in self.FOLDER_ATTRIBUTES:
            if key in kwargs:
                data[key] = kwargs[key]

        headers = {'Content-Type': 'application/json'}

        res = self._perform_request(
            'put', url, data=json.dumps(data), headers=headers)
        return self._process_response(res, [201, 204])

    def delete_project(self, project_id):
        """Delete a project.

        :param project_id: Folder identifier.

        Example::

            >>> client.delete_project('gd9eIipOQ-KobU0SwJ8VcQ')

        """

        url = '%(ep)s/%(version)s/%(tenant)s/projects/%(project_id)s' % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id})

        res = self._perform_request('delete', url)
        self._process_response(res, [204])

    #
    # Project Sources
    #

    def get_project_sources(self, project_id):
        """Get all sources of a project.

        Example::

            >>> client.get_project_sources('gd9eIipOQ-KobU0SwJ8VcQ')

        """

        url = '%(ep)s/%(version)s/%(tenant)s/projects/%(project_id)s' \
              '/sources'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id})

        res = self._perform_request('get', url)
        return self._process_response(res)

    def delete_project_source(self, project_id, source_id):
        """Deletes a source of a project.

        Example::

            >>> client.delete_project_source('gd9eIipOQ-KobU0SwJ8VcQ', '2VkLodDHTmiMO3rlWi2MVQ')

        """

        url = self._url_for_project_source(project_id, source_id)

        res = self._perform_request('delete', url)
        return self._process_response(res)

    def modify_project_source(self, project_id, source_id, config):
        """Modifies a source of a project.

        Example::

            >>> client.delete_project_source('gd9eIipOQ-KobU0SwJ8VcQ', '2VkLodDHTmiMO3rlWi2MVQ')

        """

        url = self._url_for_project_source(project_id, source_id)

        data = {'config': config}
        headers = {'Content-Type': 'application/json'}
        res = self._perform_request(
            'put', url, data=json.dumps(data), headers=headers)
        return self._process_response(res)

    def get_project_source(self, project_id, source_id):
        """Retrieves a source of a project.

        Example::

            >>> client.delete_project_source('gd9eIipOQ-KobU0SwJ8VcQ', '2VkLodDHTmiMO3rlWi2MVQ')

        """

        url = self._url_for_project_source(project_id, source_id)

        res = self._perform_request('get', url)
        return self._process_response(res)

    def _url_for_project_source(self, project_id, source_id):
        """Constructs a URL to a project source"""
        url = '%(ep)s/%(version)s/%(tenant)s/projects/%(project_id)s' \
              '/sources/%(source_id)s'\

        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'source_id': source_id})

        return url

    #
    # Seeders
    #

    def get_user_seeders(self):
        """Get all seeders for the user.

        :returns: A dict which contains all seeders.

        Example::

            >>> client.get_user_seeders()
            {u'seeders': [{u'seeder': u'team', u'title': u'Objects'}]}

        """

        url = '%(ep)s/%(version)s/%(tenant)s/objects/seeders' % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant})

        res = self._perform_request('get', url)
        return self._process_response(res, [200])

    #
    # Subscriptions
    #

    def get_object_subscriptions(self, project_id, object_id, user_id=None,
                                 filter_deleted=None):
        """Get all subscriptions for the provided object.

        :param object_id: Object identifier.
        :param user_id: User identifier.
        :param filter_deleted: If `True` returns only non-deleted
            subscriptions.
        :returns: A list which contains subscriptions.

        Example::

            >>> client.get_object_subscriptions('2sic33jZTi-ifflvQAVcfw')
            [{u'active': True,
              u'config': {u'market': u'de-CH',
                          u'query': u'squirro',
                          u'vertical': u'News'},
              u'deleted': False,
              u'id': u'hw8j7LUBRM28-jAellgQdA',
              u'link': u'http://bing.com/news/search?q=squirro',
              u'modified_at': u'2012-10-09T07:54:12',
              u'provider': u'bing',
              u'seeder': u'team',
              u'source_id': u'2VkLodDHTmiMO3rlWi2MVQ',
              u'title': u'News Alerts for "squirro" in Switzerland'},
             {u'active': True,
              u'config': {u'tenant': u'test',
                          u'user': u'H5Qv-WhgSBGW0WL8xolSCQ',
                          u'username': u'mysquirro'},
              u'deleted': False,
              u'id': u'MawimNPKSlmpeS9YlMzzaw',
              u'link': u'http://twitter.com/mysquirro',
              u'modified_at': u'2012-10-09T07:54:11',
              u'provider': u'twitter',
              u'seeder': u'team',
              u'source_id': u'CYsM3wWTTQu3jgYatvzHDQ',
              u'title': u'@mysquirro'}]

        """

        url = '%(ep)s/%(version)s/%(tenant)s' \
              '/projects/%(project_id)s' \
              '/objects/%(object_id)s/subscriptions'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'object_id': object_id})

        # build params
        params = {}
        if user_id is not None:
            params['user_id'] = user_id
        if filter_deleted is not None:
            params['filter_deleted'] = filter_deleted

        res = self._perform_request('get', url, params=params)
        return self._process_response(res)

    def get_subscription(self, project_id, object_id, subscription_id):
        """Get subscription details.

        :param object_id: Object identifier.
        :param subscription_id: Subscription identifier.
        :returns: A dict which contains the subscription.

        Example::

            >>> client.get_subscription('2sic33jZTi-ifflvQAVcfw', 'MawimNPKSlmpeS9YlMzzaw')
            {u'active': True,
             u'config': {u'tenant': u'test',
                         u'user': u'H5Qv-WhgSBGW0WL8xolSCQ',
                         u'username': u'mysquirro'},
             u'deleted': False,
             u'id': u'MawimNPKSlmpeS9YlMzzaw',
             u'link': u'http://twitter.com/mysquirro',
             u'modified_at': u'2012-10-09T07:54:11',
             u'provider': u'twitter',
             u'seeder': u'team',
             u'source_id': u'CYsM3wWTTQu3jgYatvzHDQ',
             u'title': u'@mysquirro'}

        """

        url = '%(ep)s/%(version)s/%(tenant)s' \
              '/projects/%(project_id)s' \
              '/objects/%(object_id)s/subscriptions/%(subscription_id)s'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'object_id': object_id,
            'subscription_id': subscription_id})

        res = self._perform_request('get', url)
        return self._process_response(res)

    def new_subscription(self, project_id, object_id, provider, config,
                         user_id=None, seeder=None, active=None, private=None):
        """Create a new subscription.

        :param object_id: Object identifier.
        :param provider: Provider name.
        :param config: Provider configuration dict.
        :param user_id: User identifier.
        :param seeder: Seeder which manages the subscription.
        :param active: Whether the new subscription is active, either `True`
            or `False`.
        :param private: Hints that the contents for this subscriptions should
            be treated as private.
        :returns: A dict which contains the new subscription.

        Example::

            >>> client.new_subscription('2sic33jZTi-ifflvQAVcfw', 'feed', {'url': 'http://blog.squirro.com/rss'})
            {u'active': True,
             u'config': {u'url': u'http://blog.squirro.com/rss'},
             u'deleted': False,
             u'id': u'oTvI6rlaRmKvmYCfCvLwpw',
             u'link': u'http://blog.squirro.com/rss',
             u'modified_at': u'2012-10-12T09:32:09',
             u'provider': u'feed',
             u'seeder': u'team',
             u'source_id': u'D3Q8AiPoTg69bIkqFhe3Bw',
             u'title': u'Squirro'}

        """

        url = '%(ep)s/%(version)s/%(tenant)s' \
              '/projects/%(project_id)s' \
              '/objects/%(object_id)s/subscriptions'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'object_id': object_id})

        # build data
        data = {
            'provider': provider, 'config': json.dumps(config)
        }
        if user_id is not None:
            data['user_id'] = user_id
        if seeder is not None:
            data['seeder'] = seeder
        if active is not None:
            data['active'] = active
        if private is not None:
            data['private'] = private

        res = self._perform_request('post', url, data=data)
        return self._process_response(res, [200, 201])

    def modify_subscription(self, project_id, object_id, subscription_id,
                            active=None, config=None):
        """Modify an existing subscription.

        :param object_id: Object identifier.
        :param subscription_id: Subscription identifier.
        :param active: Whether the subscription is active, either `True`
            or `False`.
        :param config: Changed config of the subscription.

        Example::

            >>> client.modify_subscription('2sic33jZTi-ifflvQAVcfw', 'oTvI6rlaRmKvmYCfCvLwpw', active=False)
        """

        url = '%(ep)s/%(version)s/%(tenant)s' \
              '/projects/%(project_id)s' \
              '/objects/%(object_id)s/subscriptions/%(subscription_id)s'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'object_id': object_id, 'subscription_id': subscription_id})

        # build data
        data = {}
        if active is not None:
            data['active'] = active
        if config is not None:
            data['config'] = json.dumps(config)

        res = self._perform_request('put', url, data=data)
        return self._process_response(res, [200])

    def delete_subscription(self, project_id, object_id, subscription_id,
                            seeder=None):
        """Delete an existing subscription.

        :param object_id: Object identifier.
        :param subscription_id: Subscription identifier.
        :param seeder: Seeder that deletes the subscription.

        Example::

            >>> client.delete_subscription('2sic33jZTi-ifflvQAVcfw', 'oTvI6rlaRmKvmYCfCvLwpw')

        """

        url = '%(ep)s/%(version)s/%(tenant)s' \
              '/projects/%(project_id)s' \
              '/objects/%(object_id)s/subscriptions/%(subscription_id)s'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'object_id': object_id,
            'subscription_id': subscription_id})

        # build params
        params = {}
        if seeder is not None:
            params['seeder'] = seeder

        res = self._perform_request('delete', url, params=params)
        self._process_response(res, [204])

    #
    # Temporal Signals
    #

    def new_temporal_signal(self, object_id, event_subject,
                            event_start, event_end, start, end, tag=None,
                            boost=1.0, delete=None):
        """Creates a new temporal signal for the provided object identifier.

        :param object_id: Object identifier.
        :param event_subject: Subject of the event.
        :param event_start: ISO formatted event start date and time.
        :param event_end: ISO formatted event end date and time.
        :param start: ISO formatted start date and time for boosting.
        :param end: ISO formatted end date and time for boosting.
        :param tag: Event tag.
        :param boost: Event boost value. Can be any float value from -1.0 to
            1.0.
        :param delete: Temporal signals to be deleted in the same request.
        :returns: A dict which contains the created temporal signals.

        Example::

            >>> client.new_temporal_signal('2sic33jZTi-ifflvQAVcfw', 'Introductory Call and Squirro Demo', '2012-10-16T12:30:50', '2012-10-17T12:30:50', '2012-10-16T10:30:50', '2012-10-17T10:30:50', boost=0.5)
            {u'created': [{u'boost_factor': 0.5,
                           u'end_at': u'2012-10-17T10:30:50',
                           u'event_endtime': u'2012-10-17T12:30:50',
                           u'event_starttime': u'2012-10-16T12:30:50',
                           u'event_subject': u'Introductory Call and Squirro Demo',
                           u'id': u'4AqYjBQ4SyeBWEMpLhN48A',
                           u'start_at': u'2012-10-16T10:30:50',
                           u'tag': None,
                           u'object_id': u'c2on-G2KR-OufdebYEFEsw'}]}

        """

        if delete is None:
            delete = {}

        url = '%(ep)s/%(version)s/%(tenant)s' \
              '/objects/%(object_id)s/temporal_signals'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'object_id': object_id})

        # build params
        data = {
            'create': [{
                'event_subject': event_subject,
                'event_starttime': event_start,
                'event_endtime': event_end, 'start_at': start, 'end_at': end,
                'boost_factor': boost,
            }]
        }
        if tag is not None:
            data['create'][0]['tag'] = tag
        if delete:
            data['delete'] = delete

        headers = {'Content-Type': 'application/json'}

        res = self._perform_request(
            'post', url, data=json.dumps(data), headers=headers)
        return self._process_response(res, [200, 201, 204])

    def get_object_temporal_signals(self, object_id):
        """Get all temporal signals for the provided object.

        :param object_id: Object identifier.
        :returns: Dictionary of temporal signals.

        Example::

            >>> client.get_object_temporal_signals()
        """
        url = '%(ep)s/%(version)s/%(tenant)s' \
              '/objects/%(object_id)s/temporal_signals'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'object_id': object_id})

        res = self._perform_request('get', url)
        return self._process_response(res, [200])

    def delete_temporal_signal(self, object_id, signal_id):
        """Delete an existing temporal signal.

        :param object_id: Object identifier.
        :param signal_id: Temporal signal identifier.

        Example::

            >>> client.delete_temporal_signal('c2on-G2KR-OufdebYEFEsw', '4AqYjBQ4SyeBWEMpLhN48A')

        """

        url = '%(ep)s/%(version)s/%(tenant)s' \
              '/objects/%(object_id)s/temporal_signals/%(signal_id)s'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'object_id': object_id,
            'signal_id': signal_id})

        res = self._perform_request('delete', url)
        return self._process_response(res, [204])

    #
    # Object Signals
    #

    def get_object_signals(self, project_id, object_id, flat=False):
        """Return a dictionary of object signals for a object.

        :param project_id: Project identifier.
        :param object_id: Object identifier.
        :param flat: Set to `True` to receive a simpler dictionary
            representation. The `seeder` information is not displayed in that
            case.
        :returns: Dictionary of signals on this object.

        Example::

            >>> client.get_object_signals('gd9eIipOQ-KobU0SwJ8VcQ', '2sic33jZTi-ifflvQAVcfw')
            {'signals': [{u'key': u'email_domain',
                          u'value': 'nestle.com',
                          u'seeder': 'salesforce'}]}

            >>> client.get_object_signals('gd9eIipOQ-KobU0SwJ8VcQ', '2sic33jZTi-ifflvQAVcfw', flat=True)
            {u'email_domain': 'nestle.com'}
        """
        url = '%(ep)s/%(version)s/%(tenant)s' \
              '/projects/%(project_id)s/objects/%(object_id)s/signals'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'object_id': object_id})

        res = self._perform_request('get', url)
        retval = self._convert_flat(flat, self._process_response(res, [200]))
        return retval

    def update_object_signals(self, project_id, object_id, signals,
                              seeder=None, flat=False):
        """Updates the object signals of a object.

        :param project_id: Prooject identifier.
        :param object_id: Object identifier.
        :param signals: List of all objects to update. Only signals that exist
            in this list will be touched, the others are left intact. Use the value
            `None` for a key to delete that signal.
        :param seeder: Seeder that owns these signals. Should be set for
            automatically written values.
        :param flat: Set to `True` to pass in and receive a simpler dictionary
            representation. The `seeder` information is not displayed in that
            case.
        :returns: List or dictionary of all signals of that object in the same
            format as returned by `get_object_signals`.

        Example::

            >>> client.update_object_signals('gd9eIipOQ-KobU0SwJ8VcQ', '2sic33jZTi-ifflvQAVcfw',
                [{'key': 'essentials',
                  'value': ['discovery-baseobject-A96PWkLzTIWSJy3WMsvzzw']}])
            [
                {u'key': u'essentials',
                 u'value': [u'discovery-baseobject-A96PWkLzTIWSJy3WMsvzzw'],
                 u'seeder': None},
                {u'key': u'email_domain',
                 u'value': 'nestle.com',
                 u'seeder': 'salesforce'}
            ]

            >>> client.update_object_signals('gd9eIipOQ-KobU0SwJ8VcQ', '2sic33jZTi-ifflvQAVcfw',
                {'essentials': ['discovery-baseobject-A96PWkLzTIWSJy3WMsvzzw']},
                flat=True)
            {u'essentials': [u'discovery-baseobject-A96PWkLzTIWSJy3WMsvzzw'],
             u'email_domain': u'nestle.com'}
        """
        url = '%(ep)s/%(version)s/%(tenant)s' \
              '/projects/%(project_id)s/objects/%(object_id)s/signals'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id,
            'object_id': object_id})

        if flat:
            signals = [{'key': key, 'value': value}
                       for key, value in signals.iteritems()]

        data = {'signals': signals, 'seeder': seeder}

        headers = {'Content-Type': 'application/json'}
        res = self._perform_request(
            'post', url, data=json.dumps(data), headers=headers)
        retval = self._convert_flat(flat, self._process_response(res, [200]))
        return retval

    def _convert_flat(self, flat, retval):
        """Converts the object API response to the flat format.
        """
        if flat:
            retval = dict([(s['key'], s['value']) for s in retval['signals']])
        return retval

    #
    # Preview
    #

    def get_preview(self, project_id, provider, config):
        """Preview the provider configuration.

        :param project_id: Project identifier.
        :param provider: Provider name.
        :param config: Provider configuration.
        :returns: A dict which contains the provider preview items.

        Example::

            >>> client.get_preview('feed', {'url': ''})
            {u'count': 2,
             u'items': [{u'created_at': u'2012-10-01T20:12:07',
                         u'id': u'F7EENNQeTz2z7O7htPACgw',
                         u'link': u'http://blog.squirro.com/post/32680369129/swisscom-features-our-sister-product-memonic-in-its-all',
                         u'read': False,
                         u'item_score': 0,
                         u'score': 0,
                         u'starred': False,
                         u'thumbler_url': u'd486ac63fc3490b42ce044feba7b71b18cb84061/thumb/trunk/57/cd/10/57cd10d6e0163a7e068370d91f14ed0e46dca085.jpg',
                         u'title': u'Swisscom features our sister product Memonic in its all new App Store',
                         u'webshot_height': 237,
                         u'webshot_url': u'http://webshot.trunk.cluster.squirro.net.s3.amazonaws.com/57/cd/10/57cd10d6e0163a7e068370d91f14ed0e46dca085.jpg',
                         u'webshot_width': 600},
                        {u'created_at': u'2012-09-25T08:09:24',
                         u'id': u'Nrj308UNTEixra3qTYLn7w',
                         u'link': u'http://blog.squirro.com/post/32253089480/247-million-emails-are-sent-every-day-80-are',
                         u'read': False,
                         u'item_score': 0,
                         u'score': 0,
                         u'starred': False,
                         u'thumbler_url': u'b4269d64a8b5993678a33a68ea013e1e8875bc67/thumb/trunk/ca/24/f2/ca24f263eb044e8ed3bc5135ab7d56112cb8206a.jpg',
                         u'title': u'247 million emails are sent every day - 80% are spam.\\nPeople...',
                         u'webshot_height': 360,
                         u'webshot_url': u'http://webshot.trunk.cluster.squirro.net.s3.amazonaws.com/ca/24/f2/ca24f263eb044e8ed3bc5135ab7d56112cb8206a.jpg',
                         u'webshot_width': 480}]}

        """

        url = '%(ep)s/%(version)s/%(tenant)s/projects/%(project_id)s/preview' % ({
            'ep': self.topic_api_url, 'project_id': project_id,
            'version': self.version, 'tenant': self.tenant})

        # build params
        params = {'provider': provider, 'config': json.dumps(config)}

        res = self._perform_request('get', url, params=params)
        return self._process_response(res)

    #
    # Collection
    #

    def get_collection(self):
        """Returns all collection objects which is the full hierarchical view
        of seeders, projects, and objects that the user can see.

        :returns: A dict.

        Example::

            >>> client.get_collection()
            {u'children': [{u'children': [{u'children': [{u'project_id': u'Sz7LLLbyTzy_SddblwIxaA',
                                                          u'id': u'zFe3V-3hQlSjPtkIKpjkXg',
                                                          u'is_ready': True,
                                                          u'managed_subscription': True,
                                                          u'needs_preview': False,
                                                          u'noise_level': None,
                                                          u'seeder': u'team',
                                                          u'title': u'Alexander Sennhauser',
                                                          u'type': u'contact'}],
                                           u'id': u'Sz7LLLbyTzy_SddblwIxaA',
                                           u'seeder': u'team',
                                           u'title': u'My Contacts',
                                           u'type': u'my contacts'},
                                          {u'children': [{u'project_id': u'2aEVClLRRA-vCCIvnuEAvQ',
                                                          u'id': u'Ygbk_7psQhqvmjqhjlTYsw',
                                                          u'is_ready': True,
                                                          u'managed_subscription': False,
                                                          u'needs_preview': True,
                                                          u'noise_level': None,
                                                          u'seeder': None,
                                                          u'title': u'Memonic',
                                                          u'type': None},
                                                         {u'project_id': u'2aEVClLRRA-vCCIvnuEAvQ',
                                                          u'id': u'2sic33jZTi-ifflvQAVcfw',
                                                          u'is_ready': True,
                                                          u'managed_subscription': False,
                                                          u'needs_preview': False,
                                                          u'noise_level': None,
                                                          u'seeder': u'team',
                                                          u'title': u'Squirro',
                                                          u'type': u'organization'}],
                                           u'id': u'2aEVClLRRA-vCCIvnuEAvQ',
                                           u'seeder': u'team',
                                           u'title': u'My Organizations',
                                           u'type': u'my organizations'}],
                            u'seeder': u'team',
                            u'title': u'Objects'},
                           {u'children': [{u'children': [{u'project_id': u'Sz7LLLbyTzy_SddblwIxaA',
                                                          u'id': u'zFe3V-3hQlSjPtkIKpjkXg',
                                                          u'is_ready': True,
                                                          u'managed_subscription': True,
                                                          u'needs_preview': False,
                                                          u'noise_level': None,
                                                          u'seeder': u'team',
                                                          u'title': u'Alexander Sennhauser',
                                                          u'type': u'contact'}],
                                           u'id': u'Sz7LLLbyTzy_SddblwIxaA',
                                           u'seeder': u'team',
                                           u'title': u'My Contacts',
                                           u'type': u'my contacts'},
                                          {u'children': [{u'project_id': u'2aEVClLRRA-vCCIvnuEAvQ',
                                                          u'id': u'Ygbk_7psQhqvmjqhjlTYsw',
                                                          u'is_ready': True,
                                                          u'managed_subscription': False,
                                                          u'needs_preview': True,
                                                          u'noise_level': None,
                                                          u'seeder': None,
                                                          u'title': u'Memonic',
                                                          u'type': None},
                                                         {u'project_id': u'2aEVClLRRA-vCCIvnuEAvQ',
                                                          u'id': u'2sic33jZTi-ifflvQAVcfw',
                                                          u'is_ready': True,
                                                          u'managed_subscription': False,
                                                          u'needs_preview': False,
                                                          u'noise_level': None,
                                                          u'seeder': u'team',
                                                          u'title': u'Squirro',
                                                          u'type': u'organization'}],
                                           u'id': u'2aEVClLRRA-vCCIvnuEAvQ',
                                           u'seeder': u'team',
                                           u'title': u'My Organizations',
                                           u'type': u'my organizations'}],
                            u'seeder': u'team',
                            u'title': u'Objects'}]}

        """

        url = '%(ep)s/%(version)s/%(tenant)s/collection' % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant})

        res = self._perform_request('get', url)
        return self._process_response(res)

    def get_collection_object(self, object_id):
        """Returns details about the provided object. It can be the identifier
        of any seeder, project, or object that the user can see.

        :param object_id: Object identifier.
        :returns: A dict which contains the object details.

        Example::

            >>> client.get_collection_object('2sic33jZTi-ifflvQAVcfw')
            {u'project_id': u'2aEVClLRRA-vCCIvnuEAvQ',
             u'id': u'2sic33jZTi-ifflvQAVcfw',
             u'is_ready': True,
             u'managed_subscription': False,
             u'needs_preview': False,
             u'noise_level': None,
             u'seeder': u'team',
             u'title': u'Squirro',
             u'type': u'organization'}
        """

        url = '%(ep)s/%(version)s/%(tenant)s/collection/%(object_id)s' % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'object_id': object_id})

        res = self._perform_request('get', url)
        return self._process_response(res)

    #
    # Savedsearches
    #

    def new_savedsearch(self, scope_type, scope_id, query,
                   name=None, actions=None, created_before=None,
                   created_after=None, relative_start=None,
                   relative_end=None):
        """Create a new savedsearch.

        :param scope_type: Savedsearch scope type.
        :param scope_id: Savedsearch scope identifier.
        :param query: Savedsearch query.
        :param name: Savedsearch name.
        :param created_before: Only show items created before.
        :param created_after: Only show items created after.
        :param relative_start: Relative start date for displaying.
        :param relative_end: Relative end date for displaying.
        :param actions: List of actions to execute.
        :returns: A dict with created savedsearch.

        Example:

            >>> client.new_savedsearch(
                    scope_id='2sic33jZTi-ifflvQAVcfw',
                    scope_type='project',
                    query='hello world',
                )
            {u'actions': [{u'id': u'678b8102e5c55683130a469c12f6ce55a97ab8b5',
                           u'type': u'show'}],
             u'id': u'1ba32747c302d1c3cd4f2d43cfe937d7ae64489b',
             u'query': u'hello world'}
        """
        url = self._get_savedsearch_base_url(scope_type) % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'scope_id': scope_id,
        })
        headers = {'Content-Type': 'application/json'}
        data = {
            'query': query,
            'actions': actions,
            'name': name,
            'created_before': created_before,
            'created_after': created_after,
            'relative_start': relative_start,
            'relative_end': relative_end,
        }
        res = self._perform_request(
            'post', url, data=json.dumps(data), headers=headers)
        return self._process_response(res, [201, 200])

    def modify_savedsearch(self, savedsearch_id, scope_type, scope_id, query,
                      name=None, actions=None, created_before=None,
                      created_after=None, relative_start=None,
                      relative_end=None):
        """Modify a savedsearch.

        :param savedsearch_id: Savedsearch identifier.
        :param scope_type: Savedsearch scope type.
        :param scope_id: Savedsearch scope identifier.
        :param created_before: Only show items created before.
        :param created_after: Only show items created after.
        :param relative_start: Relative start date for displaying.
        :param relative_end: Relative end date for displaying.
        :param query: Savedsearch query.
        :return: A dict with updated savedsearch data.

        Example:

            >>> client.modify_savedsearch(
                    savedsearch_id='77e2bbb206527a2e1ff2e5baf548656a8cb999cc',
                    scope_id='2sic33jZTi-ifflvQAVcfw',
                    scope_type='project',
                    query='test me'
                )
            {u'actions': [{u'id': u'4e23249793e9a3df2126321109c6619df66aaa51',
                           u'type': u'show'}],
             u'id': u'77e2bbb206527a2e1ff2e5baf548656a8cb999cc',
             u'query': u'test me'}
        """
        url = self._get_savedsearch_base_url(scope_type, savedsearch_id) % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'scope_id': scope_id,
            'savedsearch_id': savedsearch_id,
        })
        data = {
            'query': query,
            'actions': actions,
            'name': name,
            'created_before': created_before,
            'created_after': created_after,
            'relative_start': relative_start,
            'relative_end': relative_end,
        }
        headers = {'Content-Type': 'application/json'}
        res = self._perform_request(
            'put', url, data=json.dumps(data), headers=headers)
        return self._process_response(res)

    def get_savedsearches(self, scope_type, scope_id):
        """Get savedsearches for the provided scope.

        :param scope_type: Savedsearch scope type.
        :param scope_id: Savedsearch scope identifier.
        :returns: A dict with data for the savedsearches.

        Example:

            >>> client.get_savedsearches(scope_type='project', scope_id='2sic33jZTi-ifflvQAVcfw')
            {u'savedsearches': [{u'actions': [{u'id': u'ff18180f74ebdf4b964ac8b5dde66531e0acba83',
                                               u'type': u'show'}],
                                 u'id': u'9c2d1a9002a8a152395d74880528fbe4acadc5a1',
                                 u'query': u'hello world',
                                 u'relative_start': '24h',
                                 u'relative_end': None,
                                 u'created_before': None,
                                 u'created_after': None}]}
        """
        url = self._get_savedsearch_base_url(scope_type) % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'scope_id': scope_id,
        })
        res = self._perform_request('get', url)
        return self._process_response(res)

    def get_savedsearch(self, scope_type, scope_id, savedsearch_id):
        """Get savedsearch details.

        :param scope_type: Savedsearch scope type.
        :param scope_id: Savedsearch scope identifier.
        :param savedsearch_id: Savedsearch identifier.
        :returns: A dict with savedsearch data.

        Example:

            >>> client.get_savedsearch(scope_type='project',
                                       scope_id='2sic33jZTi-ifflvQAVcfw',
                                       savedsearch_id='77e2bbb206527a2e1ff2e5baf548656a8cb999cc')
            {u'actions': [{u'id': u'4e23249793e9a3df2126321109c6619df66aaa51',
                           u'type': u'show'}],
             u'id': u'77e2bbb206527a2e1ff2e5baf548656a8cb999cc',
             u'query': u'test me',
             u'relative_start': '24h',
             u'relative_end': None,
             u'created_before': None,
             u'created_after': None}
        """

        url = self._get_savedsearch_base_url(scope_type, savedsearch_id) % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'scope_type': scope_type,
            'scope_id': scope_id,
            'savedsearch_id': savedsearch_id,
        })
        res = self._perform_request('get', url)
        return self._process_response(res)

    def delete_savedsearch(self, scope_type, scope_id, savedsearch_id):
        """Delete a savedsearch.

        :param scope_type: Savedsearch scope type.
        :param scope_id: Savedsearch scope identifier.
        :param savedsearch_id: Savedsearch identifier.

        Example:
            >>> client.delete_savedsearch(scope_type='project',
                                          scope_id='2sic33jZTi-ifflvQAVcfw',
                                          savedsearch_id='9c2d1a9002a8a152395d74880528fbe4acadc5a1')
        """
        url = self._get_savedsearch_base_url(scope_type, savedsearch_id) % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'scope_type': scope_type,
            'scope_id': scope_id,
            'savedsearch_id': savedsearch_id,
        })
        res = self._perform_request('delete', url)
        self._process_response(res, [204])

    def _get_savedsearch_base_url(self, scope_type, savedsearch_id=None):
        """Returns the URL template for the savedsearches of this scope
        type."""
        parts = ['%(ep)s/v0/%(tenant)s']
        if scope_type == 'project':
            parts.append('/projects/%(scope_id)s/savedsearches')
        else:
            raise InputDataError(400, 'Invalid scope type %r' % scope_type)

        if savedsearch_id:
            parts.append('/%(savedsearch_id)s')

        return ''.join(parts)

    #
    # Fingerprint
    #

    def get_project_fingerprints(self, project_id, tags=None):
        """Get all fingerprints which are applicable on a object.

        :param project_id: Project identifier.
        :param tags: Comma-separated tag string which can be used to
            filtering the returned fingerprints.
        :returns: A `list` of fingerprints.

        Example::
            >>> client.get_project_fingerprints('zgxIdCxSRWSwJzL1fwNX1Q')
            []
        """

        url = '%(ep)s/%(version)s/%(tenant)s/projects/%(project_id)s/fingerprints'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id})

        params = {}
        if tags is not None:
            params['tags'] = tags

        res = self._perform_request('get', url, params=params)
        return self._process_response(res)

    def get_tenant_fingerprints(self, tags=None):
        """Get all fingerprints for the tenant.

        :param tags: Comma-separated tag string which can be used to
            filtering the returned fingerprints.
        :returns: A `list` of fingerprints.

        Example::
            >>> client.get_tenant_fingerprints()
            []
        """

        url = '%(ep)s/%(version)s/%(tenant)s/fingerprints'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant})

        params = {}
        if tags is not None:
            params['tags'] = tags

        res = self._perform_request('get', url, params=params)
        return self._process_response(res)

    def get_fingerprint(self, type, type_id, name, debug=False):
        """Get a single fingerprint for the provided parameters.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type identifier.
        :param name: Fingerprint name.
        :param debug: If set to `True` debug information is returned.
        :returns: Fingerprint information in a `dict`.

        Example::
            >>> client.get_fingerprint('object', 'zgxIdCxSRWSwJzL1fwNX1Q', 'default')
            {}
        """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/fingerprint/%(type)s/%(type_id)s/%(name)s'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'type': type, 'type_id': type_id,
            'name': name})

        params = {'debug': debug}

        res = self._perform_request('get', url, params=params)
        return self._process_response(res, [200])

    def get_project_fingerprint_scores(self, project_id, tags, object_id=None,
                                       fields=None):
        """Get the fingerprint scores for all items contained in the specified
        project. One ore more fingerprints are selected by specifying tags.

        :param project_id: Project identifier.
        :param tags: String of comma-separated tags.
        :param object_id: Identifier of the object.
        :param fields: String of comma-separated item fields to include in the
            result.
        :returns: A `list` of fingerprint score entries.

        Example::

            >>> client.get_project_fingerprint_scores('Sz7LLLbyTzy_SddblwIxaA', 'poc,testing')
            [{u'fingerprint': {u'filter_min_score': None,
                               u'name': u'ma',
                               u'title': u'',
                               u'type': u'tenant',
                               u'type_id': u'squirro'},
              u'scores': [{u'fields': {u'external_id': u'a38515'}, u'noise_level': 0.0},
                          {u'fields': {u'external_id': u'a37402'}, u'noise_level': 0.0},
                          {u'fields': {u'external_id': u'a38116'}, u'noise_level': 0.1}]},
             {u'fingerprint': {u'filter_min_score': 1.2950184,
                               u'name': u'something',
                               u'title': u'Something',
                               u'type': u'tenant',
                               u'type_id': u'squirro'},
              u'scores': [{u'fields': {u'external_id': u'a38515'}, u'noise_level': 0.0},
                          {u'fields': {u'external_id': u'a37402'}, u'noise_level': 0.1},
                          {u'fields': {u'external_id': u'a38116'}, u'noise_level': 0.1}]}]
        """
        url = '%(ep)s/%(version)s/%(tenant)s/projects/%(project_id)s/scores'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'project_id': project_id})

        params = {'tags': tags}

        if object_id is not None:
            params['object_id'] = object_id

        if fields is not None:
            params['fields'] = fields

        res = self._perform_request('get', url, params=params)
        return self._process_response(res)

    def new_fingerprint(self, type, type_id, name, data=None):
        """Create a new fingerprint for the provided parameters.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type identifier.
        :param name: Fingerprint name.
        :param data: Fingerprint attributes.

        Example::
            >>> data = {'title': 'Earnings Call'}
            >>> client.new_fingerprint('user', 'bgFtu5rkR1STpx1xR2u1UQ', 'default', data)
            {}
        """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/fingerprint/%(type)s/%(type_id)s/%(name)s'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'type': type, 'type_id': type_id,
            'name': name})

        headers = {'Content-Type': 'application/json'}

        if data is None:
            data = {}

        res = self._perform_request(
            'post', url, data=json.dumps(data), headers=headers)
        return self._process_response(res, [201])

    def update_fingerprint_from_signals(self, type, type_id):
        """Update the fingerprint for the provided parameters from signals.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type identifier.

        Example::
            >>> client.update_fingerprint_from_signals('user', 'bgFtu5rkR1STpx1xR2u1UQ')
            {}
        """

        parts = ['%(ep)s/%(version)s/%(tenant)s']

        if type == 'user':
            parts.append('/users/%(type_id)s/fingerprint/signals')

        elif type == 'object':
            parts.append('/objects/%(type_id)s/fingerprint/signals')

        else:
            raise InputDataError(400, 'invalid type')

        url = ''.join(parts) % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'type_id': type_id,
        })

        res = self._perform_request('post', url)
        return self._process_response(res, [202])

    def recalculate_fingerprint(self, type, type_id, name):
        """Recalculates the fingerprint for the provided parameters. Existing
        contributing records are used during the process.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type identifier.
        :param name: Fingerprint name.

        Example::
            >>> client.recalculate_fingerprint('tenant', 'squirro', 'ma')
            {}
        """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/fingerprint/%(type)s/%(type_id)s/%(name)s/recalc'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'type': type, 'type_id': type_id,
            'name': name
        })

        res = self._perform_request('post', url)
        return self._process_response(res, [202])

    def update_fingerprint_from_content(self, type, type_id, name, content):
        """Updates the fingerprint for the provided parameters from content
        data.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type identifier.
        :param name: Fingerprint name.
        :param content: Content data which is a list of dicts which contain
            the `lang` and `text` keys.

        Example::
            >>> data = [{'lang': 'en', 'text': 'english content'}]
            >>> client.update_fingerprint_from_content('user', 'bgFtu5rkR1STpx1xR2u1UQ', 'default', data)
            {}
        """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/fingerprint/%(type)s/%(type_id)s/%(name)s/content'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'type': type, 'type_id': type_id,
            'name': name})

        headers = {'Content-Type': 'application/json'}

        res = self._perform_request(
            'post', url, data=json.dumps(content), headers=headers)
        return self._process_response(res, [202])

    def adhoc_fingerprint_from_content(self, type, type_id, content,
                                       title=None):
        """Create adhoc fingerprint for the provided parameters from content
        data.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type identifier.
        :param content: Content data which is a list of dicts which contain
            the `text` and optional `lang` keys.

        Example::
            >>> data = [{'text': 'english content'}]
            >>> client.update_fingerprint_from_content('user', 'bgFtu5rkR1STpx1xR2u1UQ', data)
            {}
        """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/fingerprint/%(type)s/%(type_id)s/content'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'type': type, 'type_id': type_id})

        params = {}
        if title is not None:
            params['title'] = title

        headers = {'Content-Type': 'application/json'}

        res = self._perform_request(
            'post', url, params=params, data=json.dumps(content),
            headers=headers)
        return self._process_response(res, [201])

    def update_fingerprint_from_baseobject(self, type, type_id, name,
                                          baseobject):
        """Updates the fingerprint for the provided parameters from baseobject
        data.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type identifier.
        :param name: Fingerprint name.
        :param baseobject: List of baseobject identifiers.

        Example::
            >>> data = ['tK0W2Q8SR9uvSn3AlB9DLg']
            >>> client.update_fingerprint_from_baseobject('user', 'bgFtu5rkR1STpx1xR2u1UQ', 'default', data)
            {}
        """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/fingerprint/%(type)s/%(type_id)s/%(name)s/baseobject'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'type': type, 'type_id': type_id,
            'name': name})

        headers = {'Content-Type': 'application/json'}

        res = self._perform_request(
            'post', url, data=json.dumps(baseobject), headers=headers)
        return self._process_response(res, [202])

    def update_fingerprint_from_items(self, type, type_id, name, items):
        """Updates the fingerprint for the provided parameters from items
        data.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type identifier.
        :param name: Fingerprint name.
        :param items: List of item identifiers.

        Example::
            >>> data = ['tfoOHGEZRAqFURaEE2cPWA']
            >>> client.update_fingerprint_from_items('user', 'bgFtu5rkR1STpx1xR2u1UQ', 'default', data)
            {}
        """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/fingerprint/%(type)s/%(type_id)s/%(name)s/items'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'type': type, 'type_id': type_id,
            'name': name})

        headers = {'Content-Type': 'application/json'}

        res = self._perform_request(
            'post', url, data=json.dumps(items), headers=headers)
        return self._process_response(res, [202])

    def update_fingerprint_attributes(self, type, type_id, name, data):
        """Updates the fingerprint key-value attributes for the provided
        parameters.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type identifier.
        :param name: Fingerprint name.
        :param data: Fingerprint attributes.

        Example::
            >>> data = {'title': 'Earnings Call'}
            >>> client.update_fingerprint_attributes('user', 'bgFtu5rkR1STpx1xR2u1UQ', 'default', data)
        """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/fingerprint/%(type)s/%(type_id)s/%(name)s'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'type': type, 'type_id': type_id,
            'name': name})

        headers = {'Content-Type': 'application/json'}

        res = self._perform_request(
            'put', url, data=json.dumps(data), headers=headers)
        self._process_response(res, [204])

    def delete_fingerprint(self, type, type_id, name):
        """Deletes the fingerprint for the provided parameters.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type identifier.
        :param name: Fingerprint name.

        Example::
            >>> client.delete_fingerprint('user', 'bgFtu5rkR1STpx1xR2u1UQ', 'default')
        """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/fingerprint/%(type)s/%(type_id)s/%(name)s'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'type': type, 'type_id': type_id,
            'name': name})

        res = self._perform_request('delete', url)
        self._process_response(res, [204])

    def reset_fingerprint(self, type, type_id, name):
        """Resets the fingerprint for the provided parameters.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type identifier.
        :param name: Fingerprint name.

        Example::
            >>> client.reset_fingerprint('user', 'bgFtu5rkR1STpx1xR2u1UQ', 'default')
        """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/fingerprint/%(type)s/%(type_id)s/%(name)s/reset'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'type': type, 'type_id': type_id,
            'name': name})

        res = self._perform_request('post', url)
        self._process_response(res, [204])

    def delete_contributing_content_record(self, type, type_id, name,
                                           record_id, created_at=None):
        """Deletes a contributing content record and recalculates the
        fingerprint for the provided parameters.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type identifier.
        :param name: Fingerprint name.
        :param record_id: Contributing record identifier.
        :param created_at: Contributing record creation timestamp.

        Example::
            >>> client.delete_contributing_content_record('user', 'bgFtu5rkR1STpx1xR2u1UQ', 'default', 'M2uyX6aUQVG2J2zcblSFHg')
            {}
        """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/fingerprint/%(type)s/%(type_id)s/%(name)s/content/%(record_id)s'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'type': type, 'type_id': type_id,
            'name': name, 'record_id': record_id})

        params = {}
        if created_at is not None:
            params['created_at'] = created_at

        res = self._perform_request('delete', url, params=params)
        return self._process_response(res, [202])

    def update_contributing_content_record(self, type, type_id, name,
                                           record_id, content,
                                           created_at=None):
        """Updates a contributing content record and recalculates the
        fingerprint for the provided parameters.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type identifier.
        :param name: Fingerprint name.
        :param record_id: Contributing record identifier.
        :param content: Content data which is a dict which contains the `lang`
            and `text` keys.
        :param created_at: Contributing record creation timestamp.

        Example::
            >>> data = {'lang': 'en', 'text': 'updated english content'}
            >>> client.update_fingerprint_from_content('user', 'bgFtu5rkR1STpx1xR2u1UQ', 'default', 'M2uyX6aUQVG2J2zcblSFHg', data, created_at='2013-07-01T14:08:23')
            {}
         """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/fingerprint/%(type)s/%(type_id)s/%(name)s/content/%(record_id)s'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'type': type, 'type_id': type_id,
            'name': name, 'record_id': record_id})

        headers = {'Content-Type': 'application/json'}

        params = {}
        if created_at is not None:
            params['created_at'] = created_at

        res = self._perform_request(
            'put', url, params=params, data=json.dumps(content),
            headers=headers)
        return self._process_response(res, [202])

    def delete_contributing_baseobject_record(self, type, type_id, name,
                                             record_id, created_at=None):
        """Deletes a contributing baseobject record and recalculates the
        fingerprint for the provided parameters.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type identifier.
        :param name: Fingerprint name.
        :param record_id: Contributing record identifier.
        :param created_at: Contributing record creation timestamp.

        Example::
            >>> client.delete_contributing_baseobject_record('user', 'bgFtu5rkR1STpx1xR2u1UQ', 'default', 'sPOUuXqgSXqSllVkzheLvw')
            {}
        """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/fingerprint/%(type)s/%(type_id)s/%(name)s'\
              '/baseobject/%(record_id)s'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'type': type, 'type_id': type_id,
            'name': name, 'record_id': record_id})

        params = {}
        if created_at is not None:
            params['created_at'] = created_at

        res = self._perform_request('delete', url, params=params)
        return self._process_response(res, [202])

    def delete_contributing_items_record(self, type, type_id, name,
                                         record_id, created_at=None):
        """Deletes a contributing items record and recalculates the
        fingerprint for the provided parameters.

        :param type: Fingerprint type.
        :param type_id: Fingerprint type identifier.
        :param name: Fingerprint name.
        :param record_id: Contributing record identifier.
        :param created_at: Contributing record creation timestamp.

        Example::
            >>> client.delete_contributing_items_record('user', 'bgFtu5rkR1STpx1xR2u1UQ', 'default', '0L5jwLdfTJWRcTFMtBzhGg')
            {}
        """
        url = '%(ep)s/%(version)s/%(tenant)s'\
              '/fingerprint/%(type)s/%(type_id)s/%(name)s/items/%(record_id)s'
        url = url % ({
            'ep': self.topic_api_url, 'version': self.version,
            'tenant': self.tenant, 'type': type, 'type_id': type_id,
            'name': name, 'record_id': record_id})

        params = {}
        if created_at is not None:
            params['created_at'] = created_at

        res = self._perform_request('delete', url, params=params)
        return self._process_response(res, [202])

    #
    # Tasks
    #

    def get_tasks(self):
        """Return a list of all tasks for the current user."""
        # Build URL
        url = '%(ep)s/v0/%(tenant)s/tasks' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
        })
        res = self._perform_request('get', url)
        return self._process_response(res)

    def get_task(self, task_id):
        """Return details for a task.
        """
        # Build URL
        url = '%(ep)s/v0/%(tenant)s/tasks/%(task_id)s' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'task_id': task_id,
        })
        res = self._perform_request('get', url)
        return self._process_response(res)

    def create_task(self, **params):
        """Create a task. All parameters are passed on as attributes to update.
        """
        # Build URL
        url = '%(ep)s/v0/%(tenant)s/tasks' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
        })
        res = self._perform_request('post', url, data=json.dumps(params),
                                    headers={'Content-Type': 'application/json'})
        return self._process_response(res, [201])

    def update_task(self, task_id, **params):
        """Update a task. All parameters are passed on as attributes to update.
        """
        # Build URL
        url = '%(ep)s/v0/%(tenant)s/tasks/%(task_id)s' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'task_id': task_id,
        })
        res = self._perform_request('put', url, data=json.dumps(params),
                                    headers={'Content-Type': 'application/json'})
        return self._process_response(res)

    def delete_task(self, task_id, **params):
        """Delete a task.
        """
        # Build URL
        url = '%(ep)s/v0/%(tenant)s/tasks/%(task_id)s' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant,
            'task_id': task_id,
        })
        res = self._perform_request('delete', url)
        self._process_response(res, [204])

    #
    # Tasks
    #

    def get_projects(self):
        """Return all projects.
        """
        # Build URL
        url = '%(ep)s/v0/%(tenant)s/projects' % ({
            'ep': self.topic_api_url,
            'tenant': self.tenant
        })
        res = self._perform_request('get', url)
        return self._process_response(res)
