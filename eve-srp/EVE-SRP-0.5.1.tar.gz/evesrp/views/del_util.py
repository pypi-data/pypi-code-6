from flask import View

from flask.ext.login import login_required, current_user
from .. import db
from ..models import Request, Modifier, Action
from ..auth import SubmitRequestsPermission, ReviewRequestsPermission, \
        PayoutRequestsPermission, admin_permission
from ..auth.models import Division, Pilot


class RequestListing(View):
    """Abstract class for lists of :py:class:`~evesrp.models.Request`\s.
    """

    #: The template to use for listing requests
    template = 'list_requests.html'

    decorators = [login_required]

    def requests(self, division_id=None, page=None):
        """Returns a list :py:class:`~.Request`\s belonging to
        the specified :py:class:`~.Division`, or all divisions if
        ``None``. Must be implemented by subclasses, as this is an abstract
        method.

        :param int division_id: ID number of a :py:class:`~.Division`, or
            ``None``.
        :returns: :py:class:`~.models.Request`\s
        :rtype: iterable
        """
        raise NotImplementedError()

    def dispatch_request(self, division_id=None, page=None):
        """Returns the response to requests.

        Part of the :py:class:`flask.views.View` interface.
        """
        return render_template(self.template,
                requests=self.requests(division_id, page))


class SubmittedRequestListing(RequestListing):

    def request_query(self, division_id=None):
        query = db.session.query(Request)\
                .filter(Request.submitter_id == current_user.id)
        if division_id is not None:
            query = query.filter(Request.division == division_id)
        return query


    def requests(self, division_id=None, page=None):
        if division_id is not None:
            division = Division.query.get_or_404(division_id)
            return filter(lambda r: r.division == division,
                    current_user.requests)
        else:
            return current_user.requests


class PermissionRequestListing(RequestListing):
    """Show all requests that the current user has permissions to access.

    This is used for the various permission-specific views.
    """

    def __init__(self, permissions, filter_func):
        """Create a :py:class:`PermissionRequestListing` for the given
        permissions.

        The requests can be further filtered by providing a callable via
        ``filter_func``.

        :param tuple permissions: The permissions to filter by
        :param callable filter_func: A callable taking a request as an argument
            and returning ``True`` or ``False`` if it should be included.
        """
        self.permissions = permissions
        self.filter_func = filter_func

    def request_query(self, division_id=None):
        pass

    def requests(self, division_id=None, page=None):
        if division_id is not None:
            division = Division.query.get_or_404(division_id)
            if not current_user.has_permission(self.permissions, division):
                abort(403)
            else:
                divisions = [division]
        else:
            perms = filter(lambda p: p.permission in self.permissions,
                    current_user.permissions)
            divisions = map(lambda p: p.division, perms)
        requests = OrderedDict()
        for division in divisions:
            filtered = filter(self.filter_func, division.requests)
            requests.update(map(lambda r: (r, object), filtered))
        return requests.keys()


class PermissionStatusRequests(RequestListing):
    def __init__(self, permissions, statuses):
        self.permissions = permissions
        self.statuses = statuses

    def requests(self, division_id):
        if division_id is not None:
            division = Division.query.get_or_404(division_id)
            if not current_user.has_permission(self.permissions, division):
                abort(403)
            else:
                divisions = [division]
        else:
            perms = filter(lambda p: p.permission in self.permissions,
                    current_user.permissions)
            divisions = map(lambda p: p.division, perms)
        queries = []
        for division in divisions:
            query = db.session.query(Request)\
                    .filter(Request.division_id == division.id)
            sub_queries = []
            for status in self.statuses:
                sub_query = query.filter(Request.status == status)
                sub_queries.append(sub_query)
            if len(sub_queries) > 1:
                query = sub_queries[0].union(*sub_queries[1:])
            else:
                query = sub_queries[0]
            queries.append(query)
        if len(queries) > 1:
            return queries[0].union(queries[1:])
        else:
            return queries[0]





