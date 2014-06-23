from flask import render_template
from flask.views import View
from flask.ext.login import login_required, current_user
from .. import db
from ..models import Request
from ..auth.models import User, Group, Permission, Division, Pilot


class RequestListing(View):
    """Abstract class for lists of :py:class:`~evesrp.models.Request`\s.
    """

    #: The template to use for listing requests
    template = 'list_requests.html'

    decorators = [login_required]

    def requests(self, division_id=None):
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

    def dispatch_request(self, division_id=None, page=1):
        """Returns the response to requests.

        Part of the :py:class:`flask.views.View` interface.
        """
        pager = self.requests(division_id).paginate(page, per_page=20)
        return render_template(self.template,
                pager=pager)

    @property
    def _load_options(self):
        """Returns a sequence of
        :py:class:`~sqlalchemy.orm.strategy_options.Load` objects specifying
        which attributes to load (or really any load options necessary).
        """
        return (
                db.Load(Request).load_only('id', 'pilot_id', 'division_id',
                    'system', 'ship_type', 'status', 'timestamp',
                    'base_payout'),
                db.Load(Division).joinedload('name'),
                db.Load(Pilot).joinedload('name'),
        )


class PersonalRequests(RequestListing):
    """Shows a list of all personally submitted requests and divisions they
    have permissions in.

    It will show all requests the current user has submitted.
    """

    template = 'personal.html'

    def requests(self, division_id=None):
        requests = Request.query\
                .join(User)\
                .filter(User.id==current_user.id)\
                .options(*self._load_options)
        if division_id is not None:
            requests = requests.filter(Request.division_id==division_id)
        requests = requests.order_by(Request.timestamp.desc())
        return requests


class PermissionRequestListing(RequestListing):
    """Show all requests that the current user has permissions to access.

    This is used for the various permission-specific views.
    """

    def __init__(self, permissions, statuses):
        """Create a :py:class:`PermissionRequestListing` for the given
        permissions and statuses.

        :param tuple permissions: The permissions to filter by
        :param tuple statuses: A tuple of valid statuses for requests to be in
        """
        self.permissions = permissions
        self.statuses = statuses

    def dispatch_request(self, division_id=None, page=1):
        if not current_user.has_permission(self.permissions):
            abort(403)
        else:
            return super(PermissionRequestListing, self).dispatch_request(
                    division_id, page)

    def requests(self, division_id=None):
        user_perms = db.session.query(Permission.id.label('permission_id'),
                Permission.division_id.label('division_id'),
                Permission.permission.label('permission'))\
                .filter(Permission.entity==current_user)
        group_perms = db.session.query(Permission.id.label('permission_id'),
                Permission.division_id.label('division_id'),
                Permission.permission.label('permission'))\
                .join(Group)\
                .filter(Group.users.contains(current_user))
        perms = user_perms.union(group_perms)\
                .filter(Permission.permission.in_(self.permissions))
        if division_id is not None:
            perms = perms.filter(Permission.division_id==division_id)
        perms = perms.subquery()
        requests = Request.query\
                .join(perms, Request.division_id==perms.c.division_id)\
                .filter(Request.status.in_(self.statuses))\
                .order_by(Request.timestamp.desc())\
                .options(*self._load_options)
        return requests
