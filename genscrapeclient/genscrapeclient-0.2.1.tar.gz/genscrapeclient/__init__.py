from .rest import JSONRequests,JSONRequestError, ResourceManager, BaseAPI

from requests_oauthlib import OAuth1Session


__version__ = '0.2.1'


class Scrapers(ResourceManager):
    __resourcename__ = 'scrapers'

    def get(self, id_or_name):
        """Gets the scraper by it's id or name

        :param id_or_name: id or name of scraper for identification
        :type id_or_name: int or str
        :returns: the scraper data
        :rtype: dict

        """
        return self.client.get('/scrapers/{}'.format(id_or_name))

    def exists(self, id_or_name):
        """Check where the scraper with given id or name exists

        :param id_or_name: id or name of the scraper
        :type id_or_name: int or str
        :returns: whether the scraper exists
        :rtype: bool
        
        """
        try:
            return bool(self.get(id_or_name))
        except JSONRequestError:
            return False


    def all(self):
        """Gets all the scrapers

        :returns: list of scrapers
        :rtype: list of dicts

        """
        return self.client.get('/scrapers')

    def create(self, name, config):
        """Creates a new scraper with given name and config

        :param str name: name of the scraper
        :param dict config: the scraper config or spec
        :returns: the newly created scaper
        :rtype: dict

        """
        data = {'name': name, 'config': config}
        return self.client.post('/scrapers', data)

    def delete(self, id_or_name):
        """Deletes a scraper by it's id or name

        :param id_or_name: id or name of scraper for identification
        :type id_or_name: int or str
        :returns: None
        :rtype: NoneType

        """
        return self.client.delete('/scrapers/{}'.format(id_or_name))

    def update(self, id_or_name, name, config):
        """Update the scraper config and name by sending PUT request.

        :param id_or_name: id or name of scraper for identification
        :type id_or_name: int or str
        :param str name: new name of the scraper to set
        :param dict config: new config to set
        :returns: the updated scraper data
        :rtype: dict

        """
        data = {'name': name, 'config': config}
        return self.client.put('/scrapers/{}'.format(id_or_name), data)


class Crawls(ResourceManager):
    __resourcename__ = 'crawls'

    def get(self, crawl_id):
        """Gets a particular crawl by crawl_id

        :param int crawl_id: Id of the crawl
        :returns: the crawl data
        :rtype: dict

        """
        return self.client.get('/crawls/{}'.format(crawl_id))

    def all(self):
        """Gets all crawls for an account

        :returns: all crawls
        :rtype: list of dicts

        """
        return self.client.get('/crawls')

    def start(self, id_or_name):
        """Create a new crawl and begins crawling of sites

        Note that it just triggers the crawling which will take some
        time to fetch all the items. In this state, the status of the
        crawl will be 'crawling' (it can be checked by calling the
        `get` method with the respective crawl_id). Once the crawling
        is complete, the status will be set to 'complete' after which
        it's ok to send request to get the items.

        :param id_or_name: id or name of scraper for identification
        :type id_or_name: int or str
        :returns: the newly created crawl
        :rtype: dict

        """
        data = {'scraper_id': id_or_name}
        return self.client.post('/crawls', data)


class CrawledItems(ResourceManager):
    __resourcename__ = 'crawled_items'

    def get_paginated(self, crawl_id, page, per_page):
        """Gets paginated list of crawled items

        :param int crawl_id: id of the crawl
        :param int page: the page to obtain
        :param int per_page: number of items to get per page
        :returns: list of items for the page
        :rtype: list of dicts

        """
        url = '/crawls/{}/items?page={}&per_page={}'.format(crawl_id, page, per_page)
        return self.client.get(url)

    def all(self, crawl_id):
        """Gets all the crawled items by handling pagination internally

        Note that this method will return a lazy generator object so
        it cannot be reused after it's consumed once.

        :param int crawl_id: id of the crawl
        :returns: a lazy generator that can be iterated to get items
        :rtype: generator

        """
        # Here we are dropping down to the actual underlying client
        # object (In this case the OAuth1Session instance)
        c = self.client._client
        r = c.get(self.client.url('/crawls/{}/items'.format(crawl_id)))
        assert r.status_code == 200
        for item in r.json():
            yield item
        next_page = None if 'next' not in r.links else r.links['next']['url']
        while next_page:
            r = c.get(next_page)
            assert r.status_code == 200
            for item in r.json():
                yield item
            next_page = None if 'next' not in r.links else r.links['next']['url']

    def delete(self, crawl_id):
        """Deletes all items for a crawl

        Irreversible!! Use with caution

        :param int crawl_id: id of the crawl
        :returns: None
        :rtype: NoneType

        """
        return self.client.delete('/crawls/{}/items'.format(crawl_id))


class GenscrapeAPI(BaseAPI):

    def __init__(self, base_url, api_key, api_secret):
        """Initialize the genscrape api object

        :param str base_url: the base url of genscrape api
        :param str api_key: your API key
        :param str api_secret: your API secret

        """
        super(GenscrapeAPI, self).__init__()
        session = OAuth1Session(api_key, api_secret, None, None)
        self.client = JSONRequests(base_url, client=session)

    def for_resource(self, resource):
        """Gets a resource manager by the resource name

        To see all resource names, use the attribute `resources` of
        the genscrape api object.

        Usage:

          >>> api = GenscrapeAPI(.., .., ..)
          >>> api.resources
          ['scrapers', 'crawls', 'crawled_items']
          >>> scrapers = api.for_resource('scrapers')
          >>> scrapers.get(9)

        :param str resource: the name of the resource
        :returns: the resource manager for the resource
        :rtype: ResourceManager

        """
        ResourceManagerCls = self.resource_factory(resource)
        return ResourceManagerCls(self.client)
