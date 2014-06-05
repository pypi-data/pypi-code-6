from Acquisition import aq_inner
from Products.CMFPlone.browser.navigation import CatalogNavigationTree
from Products.CMFPlone.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from navtree import  buildFolderTree
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.memoize import ram
from zope.component import getMultiAdapter

# TODO: implements the treeportlet persistent
# import simplejson as json
# from ftw.dictstorage.interfaces import IDictStorage


def get_hostname(request):
    """Extract hostname in virtual-host-safe manner

    @param request: HTTPRequest object, assumed contains environ dictionary

    @return: Host DNS name, as requested by client. Lowercased, no port part.
             Return None if host name is not present in HTTP request headers
             (e.g. unit testing).
    """

    if "HTTP_X_FORWARDED_HOST" in request.environ:
        # Virtual host
        host = request.environ["HTTP_X_FORWARDED_HOST"]
    elif "HTTP_HOST" in request.environ:
        # Direct client request
        host = request.environ["HTTP_HOST"]
    else:
        return None

    # separate to domain name and port sections
    host = host.split(":")[0].lower()

    return host


def treeview_cachekey(method, self, context, current):
    """A cache key depending on the hash of the current root node, the user ID
    and the server hostname (to make sure we don't break virtual hosting).
    """
    hostname = get_hostname(self.request)
    mtool = getToolByName(context, 'portal_membership')
    member = mtool.getAuthenticatedMember()
    userid = member.getId()

    return '%s.%s:%s:%s:%s' % (
        self.__class__.__module__,
        self.__class__.__name__,
        hash(current),
        userid,
        hostname)


class TreeView(CatalogNavigationTree):

    recurse = ViewPageTemplateFile('recurse.pt')

    def __call__(self):
        self.request.response.setHeader('X-Theme-Disabled', 'True')

        root_path = self.request.get('root_path')
        return self.render(root_path)

    def render(self, root_path=None):
        """return a html tree for treeview
        """
        if root_path:
            portal_url = getToolByName(self.context, 'portal_url')
            current = portal_url.getPortalObject().restrictedTraverse(
                root_path.encode('utf-8'))
            #check if the actual context is in the current repositoryroot
            if root_path in self.context.getPhysicalPath():
                context = aq_inner(self.context)
                return self.get_tree(context, current)
            else:
                return self.get_tree(current, current)
        else:
            current = context = aq_inner(self.context)
            return self.get_tree(context, current)

    @ram.cache(treeview_cachekey)
    def get_tree(self, context, current):
        self.context = context
        # Don't travsere to top-level application obj if TreePortlet
        # was added to the Plone Site Root
        if current.Type() == 'Plone Site':
            return current.Title()
        else:
            while current.Type() != 'RepositoryRoot' \
              and current.Type() != 'Plone Site':
                current = current.aq_parent

        query = {
            'path': dict(query='/'.join(current.getPhysicalPath()), depth=-1),
            'Type': 'RepositoryFolder'}
        strategy = getMultiAdapter((context.aq_inner, self), INavtreeStrategy)

        # # we access configuration in as json under some key
        # configuration = IDictStorage(self)
        # custom = json.loads(configuration.get(
        #     # make sure key is unique as "deep" as you want
        #     'ftw-treeview-opengever-mandat1-username',
        #     # return default settings
        #     '{}'))
        # # now use the to create html
        # raise NotImplemented

        data = buildFolderTree(context.aq_inner,
            obj=context.aq_inner, query=query, strategy=strategy)
        if data.get('children'):
            children = data.get('children')[0].get('children')
            html=self.recurse(children=children, level=1, bottomLevel=999,
                              language=self.get_preferred_language_code())
            return html
        else:
            return ''

    def get_preferred_language_code(self):
        ltool = getToolByName(self.context, 'portal_languages')
        return ltool.getPreferredLanguage()
