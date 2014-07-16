"""cubicweb-collaboration application package

Cube for providing facilities for cooperative entity handling
"""
from warnings import warn
from itertools import chain
import logging

from rql.utils import is_keyword
from yams.schema import PermissionMixIn, EntitySchema, RelationDefinitionSchema
from yams.buildobjs import RelationDefinition, RelationType, DEFAULT_RELPERMS

# Until https://www.logilab.org/ticket/245548
from yams.buildobjs import EntityType
DEFAULT_ETYPEPERMS = EntityType.__permissions__

from cubicweb.predicates import relation_possible, is_in_state
from cubicweb.schema import (RQLConstraint, ERQLExpression, RRQLExpression,
                             WORKFLOW_RTYPES, WORKFLOW_TYPES,
                             split_expression)

from cubes.container import ContainerConfiguration


LOGGER = logging.getLogger('cubes.collaboration')


# Additionnal methods to yams.schema classes (EntitySchema and
# RelationDefinitionSchema).

# rql.utils.KEYWORDS misses a comma, fix it here temporarily.
# see https://www.logilab.org/ticket/245563
from rql.utils import KEYWORDS
if 'NOTIN' in KEYWORDS:
    KEYWORDS.remove('NOTIN')
    KEYWORDS.update(['NOT', 'IN'])


def get_rqlexpr_vars(expression, mainvars=()):
    return set(w.rstrip('?') for w in split_expression(expression)
               if w.isupper() and not is_keyword(w) and w not in mainvars)


def _add_mandatory_rqlexpression(perms, expression, mainvars, expr_cls):
    """Combine `expression` with existing RQL expressions in `perms`"""
    has_rqlexpr = False
    for idx, perm in enumerate(perms):
        if isinstance(perm, expr_cls):
            has_rqlexpr = True
            defined = get_rqlexpr_vars(expression, mainvars=mainvars)
            expr = perm.expression
            for var in get_rqlexpr_vars(expr, mainvars=mainvars):
                if var in defined:
                    # Maybe just issue a warning there.
                    raise Exception('Variable `%(v)s` already used in RQL '
                                    'expression `%(expr)s`' %
                                    {'v': var, 'expr': expr})
                defined.add(var)
            perms[idx] = expr_cls(', '.join([expression, expr]))
    if not has_rqlexpr:
        perms.append(expr_cls(expression))
    return perms


def schema_add_mandatory_erqlexpression(self, action, expression):
    """Overload permissions of `action` with `expression` ERQLExpression."""
    perms = list(self.permissions[action])
    perms = _add_mandatory_rqlexpression(
        perms, expression, mainvars=('X', 'U'), expr_cls=ERQLExpression)
    self.set_action_permissions(action, tuple(perms))
EntitySchema.permissions_add_mandatory_rqlexpression = schema_add_mandatory_erqlexpression


def schema_add_mandatory_rrqlexpression(self, action, expression):
    """Overload permissions of `action` with `expression` RRQLExpression."""
    perms = list(self.permissions[action])
    perms = _add_mandatory_rqlexpression(
        perms, expression, mainvars=('S', 'O', 'U'), expr_cls=RRQLExpression)
    self.set_action_permissions(action, tuple(perms))
RelationDefinitionSchema.permissions_add_mandatory_rqlexpression = schema_add_mandatory_rrqlexpression


def schema_set_permissions_groups(self, action, groups):
    """Set `groups` for `action` permissions. """
    rqlexprs = tuple(p for p in self.permissions[action]
                     if not isinstance(p, basestring))
    self.set_action_permissions(action, tuple(groups + rqlexprs))
PermissionMixIn.set_permissions_groups = schema_set_permissions_groups


# Collaboration configuration.

class CollaborationConfiguration(object):
    """Configuration object to make an entity type collaborative.

    Main methods are ``setup_schema``, ``build_hooks``,
    ``build_adapters``, ``setup_ui`` to be respectively in
    post-build/registration callbacks of schema, hooks,
    entities, views respectively.

    Notes about migration:

        *   the method ``rtypes_to_add`` returns collaboration-specific
            relation types to be added.
        *   the method ``etypes_to_sync`` returns entity types to synchronize
            because collaboration modified them (``sync_schema_props_perms``).
    """

    def __init__(self, container_config,
                 clone_rtype=None, clone_skiprtypes=(), clone_skipetypes=(),
                 clone_compulsory_hooks_categories=(), clone_state='wfs_immutable',
                 **kwargs):
        if not isinstance(container_config, ContainerConfiguration):
            warn('[0.3] CollaborationConfiguration now requires a '
                 'ContainerConfiguration as first argument',
                 DeprecationWarning, stacklevel=2)
            etype = container_config
            if 'rtype' not in kwargs:
                kwargs['rtype'] = 'in_' + etype.lower()
            container_config = ContainerConfiguration(etype, **kwargs)
        elif kwargs:
            # kwargs exists only for bw compatibility.
            raise TypeError("got unexpected keyword arguments '%s'" %
                            ', '.join(kwargs))
        self.container_config = container_config
        container_config.collaboration_config = self
        # XXX Strange to modify the container configuration in user's back...
        self.container_config.skipetypes |= WORKFLOW_TYPES
        self.container_config.skiprtypes |= WORKFLOW_RTYPES
        # For convenience.
        self.etype = self.container_config.etype
        self.rtype = self.container_config.rtype
        if clone_rtype is None:
            clone_rtype = 'clone_of_' + etype.lower()
        self.clone_rtype = clone_rtype
        self.clone_state = clone_state
        # The sets rtypes/etypes to skip for cloning include respective sets
        # for the container configuration.
        self.clone_skiprtypes = frozenset(
            clone_skiprtypes + tuple(self.container_config.skiprtypes))
        self.clone_skipetypes = frozenset(
            clone_skipetypes + tuple(self.container_config.skipetypes))
        self.clone_compulsory_hooks_categories = clone_compulsory_hooks_categories

    def setup_schema(self, schema,
                     container_rtype_permissions=None):
        """ Main setup helper. Inline a modified version of this to customize
        collaboration details to your needs.
        """
        # Setup collaboration container.
        self.container_config.define_container(schema,
                            rtype_permissions=container_rtype_permissions)
        # Ensure collaborative entity is worklowable.
        self._make_workflowable(schema, self.etype)
        # Setup all collaboration attributes and relations.
        self.setup_clone_rdef(schema)
        if schema.has_relation(self.clone_rtype):
            # Cannot remove a collaborator who has a clone.
            delperm = RRQLExpression(
                'O owned_by U, NOT EXISTS(C %s O, C owned_by S)' %
                self.clone_rtype)
        else:
            delperm = RRQLExpression('O owned_by U')
        perms = {'read': ('managers', 'users'),
                 'delete': ('managers', delperm),
                 'add': ('managers', RRQLExpression('O owned_by U'))}
        self.setup_collaborates_on(schema, perms=perms)

    @staticmethod
    def _make_workflowable(schema, etype):
        """Make `etype` workflowable if it is not.
        (Inspired by `cubicweb.schema.make_workflowable`.)
        """
        eschema = schema[etype]
        for rtype, role, tetype, card in [
                ('custom_workflow', 'subject', 'Workflow', '?*'),
                ('in_state', 'subject', 'State', '1*'),
                ('wf_info_for', 'object', 'TrInfo', '1*')]:
            if not eschema.has_relation(rtype, role):
                subj, obj = (etype, tetype) if role == 'subject' else (tetype, etype)
                rdef = RelationDefinition(subj, rtype, obj, cardinality=card)
                schema.add_relation_def(rdef)
                warn('[collaboration] adding %s to make %s entity type made '
                     'workflowable; consider making the declaration explicit '
                     'in respective schema.py' % (rdef, etype),
                     Warning, stacklevel=2)

    def rtypes_to_add(self):
        """Return the relation types to be added in migration."""
        return [self.rtype, self.clone_rtype, 'collaborates_on']

    def setup_clone_rdef(self, schema):
        if not schema.has_relation(self.clone_rtype):
            rtype = RelationType(self.clone_rtype)
            schema.add_relation_type(rtype)
        cstr = RQLConstraint('O in_state ST, ST name "%s"' % self.clone_state)
        rdef = RelationDefinition(self.etype, self.clone_rtype, self.etype,
                                  cardinality='?*', constraints=[cstr])
        schema.add_relation_def(rdef)

    def build_collaboration_workflow(self, session, default=True):
        """Build a workflow for the collaborative entity.

        The Workflow will have two states `wfs_mutable` and `wfs_immutable` and two
        transitions `wft_make_immutable` and `wft_make_mutable`.

        Set `default=True` will make this new workflow the default for the
        collaborative entity type.
        """
        rset = session.execute('Any X WHERE X is CWEType, X name %(et)s',
                               {'et': self.etype})
        assert rset, 'cannot find an entity type named %s' % self.etype
        eid = rset[0][0]
        wf = session.create_entity(
            'Workflow', name=u'collaboration workflow for ' + self.etype,
            workflow_of=eid, reverse_default_workflow=eid if default else None)
        wfs_mutable = wf.add_state(_('wfs_mutable'), initial=True)
        wfs_immutable = wf.add_state(_('wfs_immutable'))
        wf.add_transition(_('wft_make_immutable'), (wfs_mutable, ), tostate=wfs_immutable,
                          requiredgroups=('managers', 'owners'))
        wf.add_transition(_('wft_make_mutable'), (wfs_immutable, ), tostate=wfs_mutable,
                          requiredgroups=('managers', ),
                          conditions=(
                              {'expr': u'X owned_by U, NOT EXISTS(C %s X)' %
                               self.clone_rtype,
                               'mainvars': u'X,U'}, ),
                         )
        return wf

    def setup_collaborates_on(self, schema, perms):
        rdef = RelationDefinition('CWUser', 'collaborates_on', self.etype,
                                  cardinality='**', __permissions__=perms.copy())
        schema.add_relation_def(rdef)


    def setup_can_read(self, schema, perms):
        rdef = RelationDefinition('CWUser', 'can_read', self.etype,
                                  cardinality='**', __permissions__=perms.copy())
        schema.add_relation_def(rdef)


    def setup_can_write(self, schema, perms):
        rdef = RelationDefinition('CWUser', 'can_write', self.etype,
                                  cardinality='**', __permissions__=perms.copy())
        schema.add_relation_def(rdef)


    def _wfperms(self, mainvar):
        """Permissions snippet concerning workflow and the clonable state."""
        return ('NOT EXISTS(%(x)s in_state ST, ST name "%(st)s")' %
                {'x': mainvar, 'st': self.clone_state})

    def setup_security(self, schema, ignore_rdefs=(), extend_perms=False):
        """Main security setup helper.

        :param schema: schema instance
        :param ignore_rdefs: sequence of relation definitions for which not to
        apply specified container_rperms / near_container_rperms.
        :param extend_perms: if True, pre-existing permissions on entity types
        and relation definitions in the scope of the collaboration container
        will be extended to include collaboration specific permissions instead
        of being overridden.
        """
        # can_read/can_write relations.
        perms = {'read': ('managers', 'users'),
                 'delete': ('managers',),
                 'add': ('managers',)}
        self.setup_can_read(schema, perms=perms)
        self.setup_can_write(schema, perms=perms)
        self.setup_container_etype_security(schema, extend_perms=extend_perms)
        self.setup_container_rtypes_security(schema, ignore_rdefs=ignore_rdefs,
                                             extend_perms=extend_perms)

    def setup_container_etype_security(self, schema, extend_perms=False):
        # Permissions for the collaborative entity (container).
        eschema = schema[self.etype]
        read_perm = 'U can_read X'
        update_perm = 'U can_write X, ' + self._wfperms('X')
        if extend_perms:
            eschema.set_permissions_groups('read', ('managers',))
            eschema.permissions_add_mandatory_rqlexpression('read', read_perm)
            for action in ('update', 'delete'):
                eschema.set_permissions_groups(action, ('managers',))
                eschema.permissions_add_mandatory_rqlexpression(
                    action, update_perm)
        else:
            if eschema.permissions != DEFAULT_ETYPEPERMS:
                warn('overriding permissions of %s entity type for '
                     'collaboration' % eschema.type)
            eschema.permissions = {
                'add': ('managers', 'users'),
                'read': ('managers', ERQLExpression(read_perm)),
                'update': ('managers', ERQLExpression(update_perm)),
                'delete': ('managers', ERQLExpression(update_perm))
            }
        # Permissions for entity types in the container.
        for etype in self.container_config.structure(schema, strict=True)[1]:
            eschema = schema[etype]
            if extend_perms:
                eschema.set_permissions_groups('read', ('managers',))
                eschema.permissions_add_mandatory_rqlexpression(
                    'read', self._etype_read_perm)
                for action in ('update', 'delete'):
                    eschema.set_permissions_groups(action, ('managers',))
                    eschema.permissions_add_mandatory_rqlexpression(
                        action, self._etype_update_perm)
            else:
                if eschema.permissions != DEFAULT_ETYPEPERMS:
                    warn('overriding permissions of %s entity type for '
                         'collaboration' % eschema.type)
                schema[etype].permissions = self.etype_permissions()
        orphans = self._orphan_etypes(schema)
        if orphans:
            LOGGER.warning('no collaboration permissions set on entity types '
                           '(%s) which may exist without a container' %
                           ', '.join(orphans))

    def _orphan_etypes(self, schema):
        """Return entity types which are not strictly in the container (i.e.
        which entities can live without being related to a container).
        """
        return (self.container_config.structure(schema)[1] -
                self.container_config.structure(schema, strict=True)[1])

    @property
    def _etype_read_perm(self):
        return 'U can_read C, X %s C' % self.rtype

    @property
    def _etype_update_perm(self):
        return ('U can_write C, X %s C, %s' %
                (self.rtype, self._wfperms('C')))

    def etype_permissions(self):
        """Return the permissions dict of entity types in the container"""
        rqlexprs ={'read': self._etype_read_perm,
                   'update': self._etype_update_perm}
        return {'add': ('managers', 'users'),
                'read': ('managers', ERQLExpression(rqlexprs['read'])),
                'update': ('managers', ERQLExpression(rqlexprs['update'])),
                'delete': ('managers', ERQLExpression(rqlexprs['update']))}

    def setup_container_rtypes_security(self, schema, ignore_rdefs=(),
                                        extend_perms=False):
        """Setup permissions on relations."""
        orphans = self._orphan_etypes(schema)
        # Structural relations pointing directly to container root.
        for rschema, role in self.container_config.structural_relations_to_container(schema):
            var = role[0].upper()
            update_perm = ', '.join(['U can_write ' + var, self._wfperms(var)])
            for rdef in rschema.rdefs.itervalues():
                if rdef not in ignore_rdefs:
                    self._set_rdef_permissions(rdef, role=role,
                                               update_perm=update_perm,
                                               extend_perms=extend_perms)
        # Other structural relations.
        for rschema, role in chain(
                self.container_config.structural_relations_to_parent(schema),
                self.container_config.border_relations(schema)):
            var = role[0].upper()
            for rdef in rschema.rdefs.itervalues():
                if getattr(rdef, role).type in orphans:
                    LOGGER.warning(
                        'no collaboration permissions set on %s as its %s '
                        'may exist without its container' % (rdef, role))
                    continue
                if rdef not in ignore_rdefs:
                    self._set_rdef_permissions(rdef, role=role,
                                               extend_perms=extend_perms)
        # Non-structural relations.
        for rschema in self.container_config.inner_relations(schema):
            for rdef in rschema.rdefs.itervalues():
                if rdef.subject.type in orphans:
                    LOGGER.warning(
                        'no collaboration permissions set on %s as its subject '
                        'may exist without its container' % rdef)
                    continue
                if rdef not in ignore_rdefs:
                    self._set_rdef_permissions(rdef, extend_perms=extend_perms)

    def _set_rdef_permissions(self, rdef, role='subject', update_perm=None,
                              extend_perms=False):
        update_perm = update_perm or self._rdef_update_perm(role[0].upper())
        if extend_perms:
            for action in ('add', 'delete'):
                rdef.set_permissions_groups(action, ('managers',))
                rdef.permissions_add_mandatory_rqlexpression(
                    action, update_perm)
        else:
            if rdef.permissions != DEFAULT_RELPERMS:
                warn('overriding permissions of `%s` for collaboration' % rdef)
            rdef.permissions = self.rdef_permissions(role)

    def _rql_to_container(self, var):
        return '%s %s C' % (var, self.container_config.rtype)

    def _rdef_update_perm(self, var):
        return ', '.join([self._rql_to_container(var),
                          'U can_write C',
                          self._wfperms('C')])

    def rdef_permissions(self, parent_role):
        """Return the permissions dict of a relation definition in the
        container. `parent_role` is the role of the parent to container
        in the relation.
        """
        var = parent_role[0].upper()
        rqlexpr = self._rdef_update_perm(var)
        return {'read':   ('managers', 'users'),
                'add':    ('managers', RRQLExpression(rqlexpr)),
                'delete': ('managers', RRQLExpression(rqlexpr))}

    def build_hooks(self, schema):
        """Return configured container hooks for collaboration."""
        self.setup_on_commit_rtypes_permissions(schema)
        container_hooks = self.container_config.build_container_hooks(schema)
        return container_hooks + (self.build_clone_hook(), )

    def build_clone_hook(self):
        """Build the clone container hook."""
        from cubes.container.hooks import CloneContainer
        from cubicweb.server.hook import Hook, match_rtype
        return type(
            self.etype + 'CloneContainer', (CloneContainer, ),
            {'__select__': Hook.__select__ & match_rtype(self.clone_rtype)})

    def build_adapters(self, schema):
        """Return configured container adapters for collaboration."""
        from cubes.collaboration.entities import (ClonableAdapter,
                                                  CollaborativeITreeAdapter)
        container_protocol = self.container_config.build_container_protocol(schema)
        clone_select = relation_possible(self.clone_rtype,
                                         target_etype=self.etype)
        clone_adapter = type(self.etype + 'CloneAdapter', (ClonableAdapter, ),
                             {'__select__': clone_select,
                              'rtypes_to_skip': self.clone_skiprtypes,
                              'etypes_to_skip': self.clone_skipetypes,
                              'clone_rtype_role': (self.clone_rtype, 'subject'),
                              'compulsory_hooks_categories':
                                self.clone_compulsory_hooks_categories,
                             })
        itree_adapter = type(self.etype + 'ITreeAdapter', (CollaborativeITreeAdapter, ),
                             {'__select__': clone_select,
                              'tree_relation': self.clone_rtype})
        return container_protocol, clone_adapter, itree_adapter

    def setup_on_commit_rtypes_permissions(self, schema):
        """Extend security setup: need to check relations using relation to
        container in their perms on commit.
        """
        from cubicweb.server import ON_COMMIT_ADD_RELATIONS
        for rschema, _ in chain(
                self.container_config.structural_relations_to_container(schema),
                self.container_config.structural_relations_to_parent(schema),
                self.container_config.border_relations(schema)):
            ON_COMMIT_ADD_RELATIONS.add(rschema.type)
        for rschema in self.container_config.inner_relations(schema):
            ON_COMMIT_ADD_RELATIONS.add(rschema.type)

    def setup_ui(self):
        from cubicweb.web.views import uicfg
        _pvs = uicfg.primaryview_section
        _pvs.tag_subject_of(('*', self.rtype, '*'), 'hidden')
        _pvs.tag_object_of(('*', self.rtype, '*'), 'hidden')
        _afs = uicfg.autoform_section
        _afs.tag_subject_of(('*', self.rtype, self.etype), 'main', 'hidden')
        _afs.tag_object_of(('*', self.rtype, self.etype), 'main', 'hidden')
        _afs.tag_subject_of((self.etype, self.clone_rtype, self.etype),
                            'main', 'hidden')
        _afs.tag_object_of((self.etype, self.clone_rtype, self.etype),
                           'main', 'hidden')
