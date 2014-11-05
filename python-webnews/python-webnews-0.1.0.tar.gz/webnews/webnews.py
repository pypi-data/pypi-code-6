from webnews import api

class WebnewsObject(object):
    """
    This object is the parent object for all webnews objects
    """
    def __init__(self, api_val):
        """
        init
        :param api_val: The api key or api object to use
        :return:
        """
        if type(api) == api.APINonSingle or type(api) == api.API:
            self._api = api_val
        else:
            self._api = api.API(api_val)

    def populate(self, ng):
        """
        Populate the object with values from a dictionary

        Useful for building objects from JSON
        :param ng: object to populate
        :return: None
        """
        for k in ng:
            setattr(self, k, ng[k])

class Newsgroup(WebnewsObject):

    #For autocomplete in IDE mostly.  Not needed to compile
    unread_class, status, updated_at, created_at, name, newest_date, unread_count = ([None for i in range(7)])

    def __init__(self, api_val, name):
        super(Newsgroup, self).__init__(api_val)
        ng = self._api.newsgroups_search(name)
        self.populate(ng['newsgroup'])
        #print([i for i in ng['newsgroup'].keys()])


    def list(self, limit = 20, callLimit=20):
        """
        List posts
        :param limit: Max number of posts to list
        :param callLimit: Number of posts to fetch on a single call
        :return: Each post;  This is a generator
        """
        more_older = True
        oldest = [None]
        while more_older and limit > 0:
            params = {}
            if oldest[0] != None:
                params['from_older'] = oldest[0]
            params['limit'] = callLimit
            data = self._api.newsgroup_posts(self.name, params=params)
            more_older = data['more_older']
            if not 'posts_older' in data:
                raise KeyError("Missing key in api response")
            for p in data['posts_older']:
                oldest[0] = p['post']['date']
                yield p
                limit -= 1
                if limit == 0:
                    break
