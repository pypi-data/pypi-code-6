# -*- coding: utf-8 -*-

import time
import urllib
import sys
import transaction
from App.special_dtml import DTMLFile
from Products.CMFPlone.CatalogTool import CatalogTool
from Products.ZCatalog.Catalog import Catalog
from Products.ZCatalog.Catalog import CatalogError
from Products.ZCatalog.ProgressHandler import ZLogHandler
from Products.ZCatalog.ZCatalog import LOG
from Products.ZCatalog.ZCatalog import ZCatalog
from ZODB.POSException import ConflictError
from plone.indexer.interfaces import IIndexableObject
from rt.friendlyzcatalog import logger
from zope.component import queryMultiAdapter

SLOW_INDEXES = ('ZCTextIndex',)


logger.warning('Patching ZCatalog "Catalog" view')
ZCatalog.manage_catalogView = DTMLFile('dtml/catalogView', globals())

logger.warning('Patching ZCatalog "Advanced" view')
ZCatalog.manage_catalogAdvanced = DTMLFile('dtml/base_catalogAdvanced', globals())
logger.warning('Patching PloneTool "Advanced" view')
CatalogTool.manage_catalogAdvanced = DTMLFile('dtml/plone_catalogAdvanced', globals())


def manage_catalogQuickReindex(self, REQUEST, RESPONSE, URL1):
    """ re-index everything """

    elapse = time.time()
    c_elapse = time.clock()

    pgthreshold = self._getProgressThreshold()
    handler = (pgthreshold > 0) and ZLogHandler(pgthreshold) or None
    self.refreshCatalog(clear=0, pghandler=handler, quick=True)

    elapse = time.time() - elapse
    c_elapse = time.clock() - c_elapse

    RESPONSE.redirect(
        URL1 +
        '/manage_catalogAdvanced?manage_tabs_message=' +
        urllib.quote('Catalog Updated \n'
                     'Total time: %s\n'
                     'Total CPU time: %s' % (`elapse`, `c_elapse`)))

logger.warning('Adding ZCatalog "manage_catalogQuickReindex" method')
ZCatalog.manage_catalogQuickReindex = manage_catalogQuickReindex


def refreshCatalog(self, clear=0, pghandler=None, quick=False):
    """ re-index everything we can find """

    cat = self._catalog
    paths = cat.paths.values()
    if clear:
        paths = tuple(paths)
        cat.clear()

    num_objects = len(paths)
    if pghandler:
        pghandler.init('Refreshing catalog: %s' % self.absolute_url(1),
                       num_objects)

    for i in xrange(num_objects):
        if pghandler:
            pghandler.report(i)

        p = paths[i]
        obj = self.resolve_path(p)
        if obj is None:
            obj = self.resolve_url(p, self.REQUEST)
        if obj is not None:
            try:
                self.catalog_object(obj, p, pghandler=pghandler, quick=quick)
            except ConflictError:
                raise
            except Exception:
                LOG.error('Recataloging object at %s failed' % p,
                          exc_info=sys.exc_info())

    if pghandler:
        pghandler.finish()

logger.warning('Patching ZCatalog "refreshCatalog" method')
ZCatalog.refreshCatalog = refreshCatalog


def zcatalog_catalog_object(self, obj, uid=None, idxs=None, update_metadata=1,
                            pghandler=None, quick=False):
    if uid is None:
        try:
            uid = obj.getPhysicalPath
        except AttributeError:
            raise CatalogError(
                "A cataloged object must support the 'getPhysicalPath' "
                "method if no unique id is provided when cataloging")
        else:
            uid = '/'.join(uid())
    elif not isinstance(uid, str):
        raise CatalogError('The object unique id must be a string.')

    self._catalog.catalogObject(obj, uid, None, idxs,
                                update_metadata=update_metadata, quick=quick)
    # None passed in to catalogObject as third argument indicates
    # that we shouldn't try to commit subtransactions within any
    # indexing code.  We throw away the result of the call to
    # catalogObject (which is a word count), because it's
    # worthless to us here.

    if self.threshold is not None:
        # figure out whether or not to commit a subtransaction.
        t = id(transaction.get())
        if t != self._v_transaction:
            self._v_total = 0
        self._v_transaction = t
        self._v_total = self._v_total + 1
        # increment the _v_total counter for this thread only and get
        # a reference to the current transaction.
        # the _v_total counter is zeroed if we notice that we're in
        # a different transaction than the last one that came by.
        # self.threshold represents the number of times that
        # catalog_object needs to be called in order for the catalog
        # to commit a subtransaction.  The semantics here mean that
        # we should commit a subtransaction if our threshhold is
        # exceeded within the boundaries of the current transaction.
        if self._v_total > self.threshold:
            transaction.savepoint(optimistic=True)
            self._p_jar.cacheGC()
            self._v_total = 0
            if pghandler:
                pghandler.info('committing subtransaction')

logger.warning('Patching ZCatalog "catalog_object" method')
ZCatalog.catalog_object = zcatalog_catalog_object


def plone_catalog_object(self, object, uid=None, idxs=None,
                         update_metadata=1, pghandler=None, quick=False):
    if idxs is None:
        idxs = []
    self._increment_counter()

    w = object
    if not IIndexableObject.providedBy(object):
        # This is the CMF 2.2 compatible approach, which should be used
        # going forward
        wrapper = queryMultiAdapter((object, self), IIndexableObject)
        if wrapper is not None:
            w = wrapper

    ZCatalog.catalog_object(self, w, uid, idxs,
                            update_metadata, pghandler=pghandler, quick=quick)

logger.warning('Patching CatalogTool "catalog_object" method')
CatalogTool.catalog_object = plone_catalog_object


def catalogObject(self, object, uid, threshold=None, idxs=None,
                  update_metadata=1, quick=False):
    """
    Adds an object to the Catalog by iteratively applying it to
    all indexes.

    'object' is the object to be cataloged

    'uid' is the unique Catalog identifier for this object

    If 'idxs' is specified (as a sequence), apply the object only
    to the named indexes.

    If 'update_metadata' is true (the default), also update metadata for
    the object.  If the object is new to the catalog, this flag has
    no effect (metadata is always created for new objects).

    """

    if idxs is None:
        idxs = []

    index = self.uids.get(uid, None)

    if index is None:  # we are inserting new data
        index = self.updateMetadata(object, uid, None)
        self._length.change(1)
        self.uids[uid] = index
        self.paths[index] = uid

    elif update_metadata:  # we are updating and we need to update metadata
        self.updateMetadata(object, uid, index)

    # do indexing
    total = 0

    if idxs == []:
        use_indexes = self.indexes.keys()
    else:
        use_indexes = idxs

    for name in use_indexes:
        x = self.getIndex(name)
        if quick and x.meta_type in SLOW_INDEXES:
            continue
        if hasattr(x, 'index_object'):
            blah = x.index_object(index, object, threshold)
            total = total + blah
        else:
            LOG.error('catalogObject was passed bad index '
                      'object %s.' % str(x))

    return total

logger.warning('Patching Catalog "catalogObject" method')
Catalog.catalogObject = catalogObject


# Do not stop unindexing if a single catalog entry gives issues
def uncatalogObject(self, uid):
    """
    Uncatalog and object from the Catalog.  and 'uid' is a unique
    Catalog identifier

    Note, the uid must be the same as when the object was
    catalogued, otherwise it will not get removed from the catalog

    This method should not raise an exception if the uid cannot
    be found in the catalog.

    """
    data = self.data
    uids = self.uids
    paths = self.paths
    indexes = self.indexes.keys()
    rid = uids.get(uid, None)

    if rid is not None:
        for name in indexes:
            x = self.getIndex(name)
            if hasattr(x, 'unindex_object'):
                try:
                    x.unindex_object(rid)
                except KeyError:
                    LOG.error('uncatalogObject unsuccessfully '
                              'attempted to unindex uid %s '
                              'for index %s. ' % (str(uid), name))
                    continue
        del data[rid]
        del paths[rid]
        del uids[uid]
        self._length.change(-1)

    else:
        LOG.error('uncatalogObject unsuccessfully '
                  'attempted to uncatalog an object '
                  'with a uid of %s. ' % str(uid))

logger.warning('Patching Catalog "uncatalogObject" method')
Catalog.uncatalogObject = uncatalogObject
