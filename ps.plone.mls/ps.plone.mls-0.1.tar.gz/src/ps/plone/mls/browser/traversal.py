# -*- coding: utf-8 -*-

# zope imports
from ZPublisher.BaseRequest import DefaultPublishTraverse
from zope.component import adapter, queryMultiAdapter
from zope.interface import implementer
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.browser import (
    IBrowserPublisher,
    IBrowserRequest,
)

# local imports
from ps.plone.mls.content import featured
from ps.plone.mls.interfaces import IListingTraversable


@adapter(
    IListingTraversable,
    IBrowserRequest,
)
@implementer(IBrowserPublisher)
class ListingTraverser(DefaultPublishTraverse):
    """Custom Traverser for Listings.

    The traverser looks for a listing id in the traversal stack and
    tries to call the listing details view. But before it does so, it
    tries to call all (currently) known traversers.

    It also does a check on the listing id. By default this one returns
    ``True``. But a subclass can override it to only return listings
    that match a given condition.
    """
    __used_for__ = IListingTraversable

    def check_listing(self, listing_id):
        """Check if the listing ID is available."""
        return True

    def _lookup_add_on_traverser(self):
        """"""
        traverser_class = None
        try:
            from plone.app.imaging.traverse import ImageTraverser
        except ImportError:
            pass
        else:
            traverser_class = ImageTraverser

        try:
            from collective.contentleadimage.extender import LeadImageTraverse
        except ImportError:
            pass
        else:
            if not traverser_class:
                traverser_class = LeadImageTraverse

        return traverser_class

    def publishTraverse(self, request, name):
        """See zope.publisher.interfaces.IPublishTraverse"""

        # Try to deliver the default content views.
        try:
            return super(ListingTraverser, self).publishTraverse(
                request, name,
            )
        except (NotFound, AttributeError):
            pass

        traverser_class = self._lookup_add_on_traverser()
        if traverser_class is not None:
            try:
                traverser = traverser_class(self.context, self.request)
                return traverser.publishTraverse(request, name)
            except (NotFound, AttributeError):
                pass

        if not self.check_listing(name):
            raise NotFound(self.context, name, request)

        # We store the listing_id parameter in the request.
        self.request.listing_id = name
        if len(self.request.path) > 0:
            listing_view = self.request.path.pop()
            if listing_view.startswith('@@'):
                listing_view = listing_view[2:]
        else:
            listing_view = 'listing-detail'
        default_view = self.context.getDefaultLayout()

        # Let's call the listing view.
        view = queryMultiAdapter(
            (self.context, request), name=listing_view,
        )
        if view is not None:
            return view

        # Deliver the default item view as fallback.
        view = queryMultiAdapter(
            (self.context, request), name=default_view,
        )
        if view is not None:
            return view

        raise NotFound(self.context, name, request)


@adapter(
    featured.IFeaturedListings,
    IBrowserRequest,
)
class FeaturedListingsTraverser(ListingTraverser):
    """Traverser for featured listings.

    It only allows listing ids which are defined in the context.
    """
    __used_for__ = featured.IFeaturedListings

    def check_listing(self, listing_id):
        """Check if the listing ID is available."""
        return listing_id in self.context.listing_ids
