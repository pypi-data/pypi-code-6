# -*- coding: utf-8 -*-
import transaction
from Acquisition import aq_inner
from Acquisition import aq_parent
from ZODB.POSException import ConflictError
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import transaction_note
from plone.app.linkintegrity.exceptions import LinkIntegrityNotificationException


def deleteObjectsByPaths(self, paths, handle_errors=True, REQUEST=None):
        failure = {}
        success = []
        # use the portal for traversal in case we have relative paths
        portal = getToolByName(self, 'portal_url').getPortalObject()
        traverse = portal.restrictedTraverse
        for path in paths:
            # Skip and note any errors
            if handle_errors:
                sp = transaction.savepoint(optimistic=True)
            try:
                # To avoid issues with the check for acquisition,
                # relative paths should not be part of the API anymore.
                # Plone core itself does not use relative paths.
                #if not path.startswith(portal.absolute_url_path()):
                if not path.startswith("/".join(portal.getPhysicalPath())):
                    msg = (
                        'Path {} does not start '
                        'with path to portal'.format(path)
                    )
                    raise ValueError(msg)
                obj = traverse(path)
                if list(obj.getPhysicalPath()) != path.split('/'):
                    msg = (
                        'Path {} does not match '
                        'traversed object physical path. '
                        'This is likely an acquisition issue.'.format(path)
                    )
                    raise ValueError(msg)
                obj_parent = aq_parent(aq_inner(obj))
                obj_parent.manage_delObjects([obj.getId()])
                success.append('%s (%s)' % (obj.getId(), path))
            except ConflictError:
                raise
            except LinkIntegrityNotificationException:
                raise
            except Exception, e:
                if handle_errors:
                    sp.rollback()
                    failure[path] = e
                else:
                    raise
        transaction_note('Deleted %s' % (', '.join(success)))
        return success, failure
