# -*- coding: utf-8 -*-
# copyright 2014 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.


from cubicweb import ValidationError, Unauthorized, NoSelectableObject
from cubicweb.schema import ERQLExpression, RRQLExpression
from cubicweb.devtools.testlib import CubicWebTC

from cubes.container.testutils import ContainerMixinTC

from cubes.collaboration.views import CloneAction
from cubes.collaboration.testutils import CollaborationMixin


class CollaborationTC(ContainerMixinTC, CollaborationMixin, CubicWebTC):
    child_entities = True
    other_entities = True
    clone_rtype = 'clone_of_collaborative_entity'

    def setup_database(self):
        self.prepare_entities('CollaborativeEntity',
                              subetypes=('ChildEntity',),
                              otheretypes=('OtherEntity',))

    def make_clonable(self, entity):
        wf_entity = entity.cw_adapt_to('IWorkflowable')
        if wf_entity.state == 'wfs_immutable':
            return
        wf_entity.fire_transition('wft_make_immutable')
        self.commit()
        entity.cw_clear_all_caches()
        assert wf_entity.state == 'wfs_immutable', wf_entity.state


class CollaborationSchemaTC(ContainerMixinTC, CubicWebTC):

    def test_collaborative_static_structure(self):
        from config import COLLAB_CONTAINER
        container_cfg = COLLAB_CONTAINER.container_config
        rtypes, etypes = container_cfg.structure(self.schema)
        self.set_description('container static structure: rtypes')
        yield self.assertCountEqual, rtypes, ['child_entities', 'sub_children']
        self.set_description('container static structure: etypes')
        struct_etypes = ('ChildEntity', 'SubChildEntity')
        yield self.assertCountEqual, etypes, struct_etypes
        strict_etypes = container_cfg.structure(self.schema, strict=True)[1]
        self.set_description('container static structure: strict etypes')
        yield self.assertCountEqual, strict_etypes, struct_etypes

    def test_container_permissions_overwrite(self):
        etype = self.schema['CollaborativeEntity']
        rqlexprs = 'U can_read X, X name != "secret"'
        self.assertEqual(etype.permissions['read'],
                         ('managers', ERQLExpression(rqlexprs)))

    def test_etype_in_container_permissions_overwrite(self):
        self.skipTest('permissions overridding of entity type not strictly in '
                      'container not implemented')
        etype = self.schema['ChildEntity']
        update_rqlexpr = ('U can_write C, X in_collaborativeentity C, '
                          'NOT EXISTS(C in_state ST, ST name "wfs_immutable"), '
                          'X name != "don\'t touch"')
        self.assertEqual(etype.permissions['update'],
                         ('managers', ERQLExpression(update_rqlexpr)))
        read_rqlexpr = ('EXISTS(U can_read C, X in_collaborativeentity C) OR '
                        'NOT EXISTS(X in_collaborativeentity C, X owned_by U)')
        self.assertEqual(etype.permissions['read'],
                         ('managers', ERQLExpression(read_rqlexpr)))

    def test_near_container_rdef_permissions_overwrite(self):
        rdef = self.schema['child_entities'].rdefs['CollaborativeEntity', 'ChildEntity']
        add_rqlexpr = ('U can_write S, '
                       'NOT EXISTS(S in_state ST, ST name "wfs_immutable"), '
                       'S name != "I don\'t like kids"')
        self.set_description('near container rdef: rql expr')
        yield (self.assertEqual, rdef.permissions['add'],
               ('managers', RRQLExpression(add_rqlexpr)))
        # Also checks that 'users' has been removed from groups.
        self.set_description('near container rdef: groups')
        del_rqlexpr = ('U can_write S, '
                       'NOT EXISTS(S in_state ST, ST name "wfs_immutable"), '
                       'O name != "keep me"')
        yield (self.assertEqual, rdef.permissions['delete'],
               ('managers', RRQLExpression(del_rqlexpr)))

    def test_inner_rdef_permissions_overwrite(self):
        self.skipTest('permissions overridding of rdef not strictly in '
                      'container not implemented')
        rdef = self.schema['sub_children'].rdefs['ChildEntity', 'SubChildEntity']
        del_rqlexpr = (u'(NOT EXISTS(S in_collaborativeentity C1)) OR '
                       u'EXISTS(S in_collaborativeentity C, U can_write C, '
                       u'       NOT EXISTS(C in_state ST, ST name "wfs_immutable")), '
                       u'S name != "keep me"')
        self.set_description('in container rdef: rql expr')
        yield (self.assertEqual, rdef.permissions['delete'],
               ('managers', RRQLExpression(del_rqlexpr)))
        # Also check that 'users' has been removed from groups.
        self.set_description('in container rdef: groups')
        add_rqlexpr = ('(NOT EXISTS(S in_collaborativeentity C1)) OR '
                       'EXISTS(S in_collaborativeentity C, U can_write C, '
                       '       C in_state ST, NOT ST name "wfs_immutable")')
        yield (self.assertEqual, rdef.permissions['add'],
               ('managers', RRQLExpression(add_rqlexpr)))


class CollaborationWorkflowSetupTC(ContainerMixinTC, CubicWebTC):
    """Tests for collaboration workflow setup"""

    def get_etype_workflow(self, req=None):
        req = req or self.request()
        rset = self.request().execute(
            'Any ET WHERE ET is CWEType, ET name "CollaborativeEntity"')
        etype = rset.get_entity(0, 0)
        assert etype.reverse_workflow_of
        return etype, etype.reverse_workflow_of[0]

    def test_workflow_exists(self):
        etype, wf = self.get_etype_workflow(self.request())
        self.assertEqual(wf.name,
                         'collaboration workflow for CollaborativeEntity')
        self.assertEqual(etype.default_workflow[0].eid, wf.eid)

    def assertTransitionsEqual(self, wfadapter, transitions):
        self.assertEqual(
            set(transitions),
            set([t.name for t in wfadapter.possible_transitions()]))

    def test_workflow_setup(self):
        self.create_user(self.request(), u'bob')
        etype, wf = self.get_etype_workflow(self.request())
        with self.login('bob'):
            req = self.request()
            entity = req.create_entity('CollaborativeEntity', name=u'zorg',
                                       description=u'gni')
            self.commit()
            wfa = entity.cw_adapt_to('IWorkflowable')
            self.assertIsNotNone(wfa)
            self.assertEqual(wfa.current_workflow.eid, wf.eid)
            self.assertEqual(wfa.state, 'wfs_mutable')
            self.assertTransitionsEqual(wfa, ['wft_make_immutable'])
            wfa.fire_transition('wft_make_immutable')
            self.commit()
            entity.cw_clear_all_caches()
            self.assertEqual(wfa.state, 'wfs_immutable')
            self.assertTransitionsEqual(wfa, ['wft_make_mutable'])
            clone = req.create_entity('CollaborativeEntity', name=u'glub',
                                      description=u'gna',
                                      clone_of_collaborative_entity=entity)
            self.commit()
            entity.cw_clear_all_caches()
            # XXX Damned caches...
            # (see _check method of RQLExpression in cubicweb.schema)
            req.local_perm_cache.clear()
            # Not possible to make the entity mutable if it has clones.
            self.assertTransitionsEqual(wfa, [])
            with self.assertRaises(ValidationError):
                wfa.fire_transition('wft_make_mutable')
            self.rollback()


class ICollaborativeTC(CollaborationTC):

    def test_set_collaborators(self):
        req = self.request()
        entity = req.entity_from_eid(self.ce_eid)
        entity.cw_adapt_to('ICollaborative').set_collaborators(self.users())
        self.assertCountEqual(
            (user.eid for user in entity.reverse_collaborates_on),
            self.users())


class ICollaborationSecurityTC(ContainerMixinTC, CubicWebTC):

    def setup_database(self):
        self.author_eid = self.create_user(
            self.request(), 'author', groups=('users',)).eid
        with self.login('author'):
            self.entity_eid = self.request().create_entity(
                'CollaborativeEntity', name=u'My test entity',
                description=u'My description').eid

    def test_security_adapter_methods(self):
        admin_req = self.request()
        entity = admin_req.entity_from_eid(self.entity_eid)
        adapted = entity.cw_adapt_to('ICollaborationSecurity')
        # revoke read
        self.assertEqual(entity.reverse_can_read[0].eid, self.author_eid)
        adapted.revoke_permission(self.author_eid, 'read')
        entity.cw_clear_all_caches()
        self.assertEqual(len(entity.reverse_can_read), 0)
        # revoke write
        self.assertEqual(entity.reverse_can_write[0].eid, self.author_eid)
        adapted.revoke_permission(self.author_eid, 'write')
        entity.cw_clear_all_caches()
        self.assertEqual(len(entity.reverse_can_write), 0)
        # grant read
        self.assertEqual(len(entity.reverse_can_read), 0)
        adapted.grant_permission(self.author_eid, 'read')
        entity.cw_clear_all_caches()
        self.assertEqual(entity.reverse_can_read[0].eid, self.author_eid)
        # grant write; test write implies read (hence, revoke read first)
        adapted.revoke_permission(self.author_eid, 'read')
        entity.cw_clear_all_caches()
        self.assertEqual(len(entity.reverse_can_read), 0)
        adapted.grant_permission(self.author_eid, 'write')
        entity.cw_clear_all_caches()
        self.assertEqual(entity.reverse_can_write[0].eid, self.author_eid)
        self.assertEqual(entity.reverse_can_read[0].eid, self.author_eid)


class CollaborationIBreadCrumbsTC(CollaborationTC):

    def test_collaborative_breadcrumbs_for_collaborative_entities(self):
        req = self.request()
        entity = req.entity_from_eid(self.ce_eid)
        ibread_entity = entity.cw_adapt_to('IBreadCrumbs')
        self.assertEqual([entity], ibread_entity.breadcrumbs())
        one_child = entity.child_entities[0]
        ibread_child = one_child.cw_adapt_to('IBreadCrumbs')
        self.assertEqual([one_child], ibread_child.breadcrumbs())


class CollaborationActionsTC(CollaborationTC):

    def test_clone(self):
        with self.login('author'):
            req = self.request()
            entity = req.entity_from_eid(self.ce_eid)
            self.set_description('clone action not available if not public')
            yield self.check_no_clone_action, req, entity
            self.make_clonable(entity)
            self.set_description('clone action available if public')
            yield self.check_clone_action, req, entity
            self.set_description('clone edit form')
            assert entity.cw_adapt_to('Container.clone')
            yield self.check_clone_edit_form, req, entity

    def check_no_clone_action(self, req, entity):
        with self.assertRaises(NoSelectableObject):
            self.vreg['actions'].select('copy', req, rset=entity.as_rset())

    def check_clone_action(self, req, entity):
        action = self.vreg['actions'].select('copy', req,
                                             rset=entity.as_rset())
        self.assertIsInstance(action, CloneAction)

    def check_clone_edit_form(self, req, entity):
        clone_name = entity.name + ' (my clone)'
        req.form = {
            '__maineid' : 'X',
            'eid': 'X',
            '__cloned_eid:X': self.ce_eid,
            '__type:X': 'CollaborativeEntity',
            '_cw_entity_fields:X': ('name-subject,'
                                    'description-subject,'
                                    'clone_of_collaborative_entity-subject'),
            'name-subject:X': clone_name,
            'description-subject:X': entity.description,
            'clone_of_collaborative_entity-subject:X': self.ce_eid,
        }
        self.expect_redirect_handle_request(req, 'edit')
        # Ensure the clone now exists.
        clone = req.find('CollaborativeEntity', name=clone_name,
                         clone_of_collaborative_entity=entity.eid).one()
        user_eid = self.users('author')[0]
        self.check_clone(clone.eid, user_eid,
                         clone_rtype = self.clone_rtype,
                         child_entities=self.child_entities,
                         other_entities=self.other_entities,
                         clone_name=clone_name)


class CollaborationPolicyTC(CollaborationTC):

    def test_author_can_clone_if_container_clonable(self):
        # XXX To put into container
        entity = self.request().entity_from_eid(self.ce_eid)
        self.make_clonable(entity)
        clone_eid = self.clone_ce('author', clone_rtype=self.clone_rtype)
        self.check_clone(clone_eid, self.users('author')[0],
                         clone_rtype=self.clone_rtype,
                         child_entities=self.child_entities,
                         other_entities=self.other_entities)

    def test_collaborators_can_clone_if_container_clonable(self):
        entity = self.request().entity_from_eid(self.ce_eid)
        self.make_clonable(entity)
        self.setup_ce(collaborators=self.users())
        for i, collaborator_eid in enumerate(self.users()):
            clone_eid = self.clone_ce(collaborator_eid, clone_rtype=self.clone_rtype,
                                      clone_name=u'My cloned entity_%s' % i)
            self.check_clone(clone_eid,
                             collaborator_eid,
                             clone_rtype=self.clone_rtype,
                             clone_name=u'My cloned entity_%s' % i,
                             child_entities=self.child_entities,
                             other_entities=self.other_entities)

    def test_cannot_clone_unless_collaborator_or_author(self):
        entity = self.request().entity_from_eid(self.ce_eid)
        self.make_clonable(entity)
        self.setup_ce(collaborators=self.users(u'0'))
        other_user_eids = self.users(u'[^0]')
        for i, user_eid in enumerate(other_user_eids):
            self.assert_clone_ce_raises(Unauthorized, user_eid, clone_rtype=self.clone_rtype,
                                        clone_name=u'My cloned entity_%s' % i)

    def test_cannot_clone_if_in_wrong_state(self):
        entity = self.request().entity_from_eid(self.ce_eid)
        assert entity.cw_adapt_to('IWorkflowable').state == 'wfs_mutable'
        self.assert_clone_ce_raises(ValidationError, self.users('author')[0], clone_rtype=self.clone_rtype)

    def test_cannot_edit_composite_rels_if_container_cloned(self):
        req = self.request()
        entity = req.entity_from_eid(self.ce_eid)
        self.make_clonable(entity)
        clone = req.create_entity(entity.cw_etype, name=u'blah',
                                  description=entity.description,
                                  **{self.clone_rtype: entity})
        self.commit()
        with self.login('author'):
            req = self.request()
            req.create_entity('ChildEntity', name=u'New child',
                              description=u'new description',
                              reverse_child_entities=self.ce_eid)
            with self.assertRaises(Unauthorized):
                self.commit()
            self.rollback()

    def test_can_edit_composite_rels_if_container_not_cloned(self):
        with self.login('author'):
            req = self.request()
            req.create_entity('ChildEntity', name=u'New child',
                              description=u'new description',
                              reverse_child_entities=self.ce_eid)
            self.commit()

    def test_cannot_edit_sub_children_if_container_immutable(self):
        entity = self.request().entity_from_eid(self.ce_eid)
        entity.cw_adapt_to('IWorkflowable').fire_transition('wft_make_immutable')
        self.commit()
        entity.cw_clear_all_caches()
        with self.login('author'):
            req = self.request()
            one_child = req.entity_from_eid(self.ce_eid).child_entities[0]
            with self.assertRaises(Unauthorized):
                req.create_entity('SubChildEntity',
                                  name=u'New sub-child',
                                  description=u'new sub-description',
                                  reverse_sub_children=one_child)
                self.commit()
            self.rollback()

    def test_can_edit_sub_children_if_container_not_cloned(self):
        with self.login('author'):
            req = self.request()
            one_child = req.entity_from_eid(self.ce_eid).child_entities[0]
            req.create_entity('SubChildEntity',
                              name=u'New sub-child',
                              description=u'new sub-description',
                              reverse_sub_children=one_child)

    def test_can_still_edit_non_composite_rels_if_container_immutable(self):
        #self.skipTest('to be continued, not sure what this is supposed to do')
        entity = self.request().entity_from_eid(self.ce_eid)
        entity.cw_adapt_to('IWorkflowable').fire_transition('wft_make_immutable')
        self.commit()
        # XXX Is this the right behavior?
        with self.login('author'):
            req = self.request()
            new_other = req.create_entity(
                'OtherEntity',
                name=u'New child',
                other_description=u'new description',
                reverse_other_entities=self.ce_eid,
            )
            self.commit()

    def test_cannot_edit_container_if_immutable(self):
        entity = self.request().entity_from_eid(self.ce_eid)
        entity.cw_adapt_to('IWorkflowable').fire_transition('wft_make_immutable')
        self.commit()
        with self.login('author'):
            req = self.request()
            entity = req.entity_from_eid(self.ce_eid)
            yield self.check_cannot_edit_attr, entity
            yield self.check_cannot_edit_sub_entities, entity

    def check_cannot_edit_attr(self, entity):
        self.set_description('cannot edit container attributes')
        entity.cw_set(name=u'Another, new name')
        with self.assertRaises(Unauthorized):
            self.commit()
        self.rollback()

    def check_cannot_edit_sub_entities(self, entity):
        self.set_description('cannot edit entities in container')
        child = entity.child_entities[0]
        child.cw_set(description=u'New child description')
        with self.assertRaises(Unauthorized):
            self.commit()
        self.rollback()

    def test_can_edit_collaborators_even_if_container_in_clonable_state(self):
        req = self.request()
        user_1 = self.users(u'1')
        entity = req.entity_from_eid(self.ce_eid)
        entity.cw_adapt_to('IWorkflowable').fire_transition('wft_make_immutable')
        self.commit()
        # Add a collaborator
        self.setup_ce(collaborators=user_1)
        adapter = entity.cw_adapt_to('ICollaborative')
        # Check the collaborator is the only collaborator
        self.assertEqual([adapter.collaborators[0].eid], user_1)
        user_2 = self.users(u'2')
        # Add another collaborator
        self.setup_ce(collaborators=user_2)
        entity.cw_clear_all_caches()
        # Check this other collaborator is now the only collaborator
        self.assertEqual([adapter.collaborators[0].eid], user_2)
        entity.cw_clear_all_caches()
        # Pick up two collaborators
        users_1_2 = self.users(u'[12]')
        # Check that we really have two collaborators
        self.assertEqual([user for user in users_1_2],
                         [user_1[0], user_2[0]])
        # Add these two collaborators
        self.setup_ce(collaborators=users_1_2)
        # Check that these two collaborators are now the only collaborators
        self.assertEqual(frozenset(col.eid for col in adapter.collaborators),
                         frozenset(users_1_2))

    def test_collaborates_on_perms(self):
        collaborator_eid = self.create_user(self.request(), 'coll').eid
        with self.login('author'):
            req = self.request()
            entity = req.entity_from_eid(self.ce_eid)
            entity.cw_adapt_to('IWorkflowable').fire_transition('wft_make_immutable')
            self.commit()
            entity.cw_set(reverse_collaborates_on=collaborator_eid)
            self.commit()
        with self.login('coll'):
            req = self.request()
            clone_eid = req.create_entity(
                'CollaborativeEntity', name=u'my clone',
                description=u'same here',
                **{self.clone_rtype: self.ce_eid}).eid
            self.commit()
        with self.login('author'):
            req = self.request()
            entity = req.entity_from_eid(self.ce_eid)
            with self.assertRaises(Unauthorized):
                # Cannot remove collaborator if she has a clone.
                entity.cw_set(reverse_collaborates_on=None)
                self.commit()
            self.rollback()
        with self.login('coll'):
            req = self.request()
            clone = req.entity_from_eid(clone_eid)
            clone.cw_delete()
            self.commit()
        with self.login('author'):
            req = self.request()
            entity = req.entity_from_eid(self.ce_eid)
            # No more clone, can remove collaborator.
            entity.cw_set(reverse_collaborates_on=None)
            self.commit()

    def test_cannot_read_unless_author_or_collaborator(self):
        self.setup_ce(collaborators=self.users(u'0'))
        other_user_eids = self.users(u'[^0]')
        for user_eid in other_user_eids:
            login = self.request().entity_from_eid(user_eid).login
            with self.userlogin(login) as cnx:
                req = cnx.request()
                with self.assertRaises(Unauthorized):
                    # req.entity_from_eid uses req.eid_rset that does not
                    # perform a real request and thus never raises Unauthorized
                    req.execute('Any X WHERE X eid %(eid)s',
                                {'eid': self.ce_eid})
                cnx.rollback()

    def test_author_can_edit_clone(self):
        author_eid = self.users('author')[0]
        self.make_clonable(self.request().entity_from_eid(self.ce_eid))
        clone_eid = self.clone_ce(author_eid, clone_rtype=self.clone_rtype)
        with self.do_as_user('author') as req:
            clone = req.entity_from_eid(clone_eid)
            clone.cw_set(name=u'New clone name')

    def test_collaborators_can_edit_clone(self):
        entity = self.request().entity_from_eid(self.ce_eid)
        self.make_clonable(entity)
        collaborator_eids = self.users()
        self.setup_ce(collaborators=collaborator_eids)
        for i, collaborator_eid in enumerate(collaborator_eids):
            clone_eid = self.clone_ce(collaborator_eid, clone_rtype=self.clone_rtype)
            with self.do_as_user(collaborator_eid) as req:
                clone = req.entity_from_eid(clone_eid)
                clone.cw_set(name=u'New clone name %s' % i)

    def test_collaborators_cannot_edit_container(self):
        collaborator_eids = self.users()
        self.setup_ce(collaborators=collaborator_eids)
        for i, collaborator_eid in enumerate(collaborator_eids):
            login = self.request().entity_from_eid(collaborator_eid).login
            with self.userlogin(login) as cnx:
                req = cnx.request()
                original_ent = req.entity_from_eid(self.ce_eid)
                with self.assertRaises(Unauthorized):
                    original_ent.cw_set(name=u'New name %s for the original' % i)
                    cnx.commit()
                cnx.rollback()

    def test_mutable_transitions_clone_workflow(self):
        req = self.request()
        user = self.create_user(req, u'toto')
        entity = req.entity_from_eid(self.ce_eid)
        entity.cw_set(owned_by=user)
        self.commit()
        with self.login('toto'):
            req = self.request()
            entity = req.entity_from_eid(self.ce_eid)
            # Not immutable, can modify.
            entity.cw_set(name=u'toto here')
            wfa = entity.cw_adapt_to('IWorkflowable')
            self.commit()
            # Make immutable, cannot modify.
            wfa.fire_transition('wft_make_immutable')
            self.commit()
            with self.assertRaises(Unauthorized):
                entity.cw_set(name=u'toto again')
                self.commit()
            self.rollback()
            # Make mutable, and modify.
            wfa.fire_transition('wft_make_mutable')
            self.commit()
            entity.cw_set(name=u'toto again')
            self.commit()
            # Make immutable and clone.
            wfa.fire_transition('wft_make_immutable')
            self.commit()
            clone = req.create_entity('CollaborativeEntity', name=u'un clone',
                                      description=u'tout pareil',
                                      clone_of_collaborative_entity=entity)
            self.commit()
            # Cannot make the original mutable.
            with self.assertRaises(ValidationError) as err:
                wfa.fire_transition('wft_make_mutable')
            self.rollback()
            self.assertIn('transition may not be fired', str(err.exception))
            # No more clone, can make mutable.
            clone.cw_delete()
            self.commit()
            wfa.fire_transition('wft_make_mutable')
            self.commit()

    def test_owners_cannot_delete_others_clones(self):
        owners = self.users(u'[0-2]')
        self.setup_ce_owners(owners)
        admin_req = self.request()
        entity = admin_req.entity_from_eid(self.ce_eid)
        self.make_clonable(entity)
        for owner_eid in owners:
            clone_eid = self.clone_ce(owner_eid, clone_rtype=self.clone_rtype,
                                      clone_name=u'%s\'s new name' % owner_eid)
            with self.login(admin_req.entity_from_eid(owner_eid).login):
                req = self.request()
                clone_etype = req.describe(clone_eid)[0]
                # get clones not owned by current owner
                rql = ('Any E WHERE X is %(cetype)s, X eid E, '
                       'EXISTS(X %(clone_rtype)s Y), '
                       'NOT X owned_by U, U eid %%(ueid)s'
                       % {'cetype': clone_etype,
                          'clone_rtype': self.clone_rtype})
                other_clones = admin_req.execute(rql, {'ueid': owner_eid}).rows
                for other_clone in (oc[0] for oc in other_clones):
                    with self.assertRaises(Unauthorized):
                        req.execute('DELETE %(cetype)s X WHERE X eid %%(ceid)s'
                                    % {'cetype': clone_etype},
                                    {'ceid': other_clone})
                        self.commit()
                    self.rollback()

    def test_former_owners_cannot_read_unless_collaborators(self):
        owners = self.users(u'[0-2]')
        self.setup_ce_owners(owners)
        admin_req = self.request()
        entity = admin_req.entity_from_eid(self.ce_eid)
        self.setup_ce(collaborators=owners[0])
        for owner_eid in owners:
            admin_req.execute('DELETE X owned_by U WHERE X eid %(eeid)s, U eid %(ueid)s',
                              {'eeid': self.ce_eid, 'ueid': owner_eid})
            self.commit()
            self.assert_setup_ce_raises(Unauthorized, as_user=owner_eid, name=u'my other_name')
            with self.userlogin(admin_req.entity_from_eid(owner_eid).login) as cnx:
                req = cnx.request()
                if owner_eid == owners[0]:
                    my_entity = req.execute('Any X WHERE X eid %(eeid)s',
                                            {'eeid': self.ce_eid}).get_entity(0, 0)
                    self.assertEqual(my_entity.cw_etype, entity.cw_etype)
                    self.assertEqual(frozenset(ch.eid for ch in my_entity.child_entities),
                                     frozenset(ch.eid for ch in  entity.child_entities))
                else:
                    with self.assertRaises(Unauthorized):
                        req.execute('Any X WHERE X eid %(eeid)s', {'eeid': self.ce_eid})

    def test_owners_can_edit_collaborators(self):
        owners = self.users(u'[0-2]')
        self.setup_ce_owners(owners)
        entity = self.request().entity_from_eid(self.ce_eid)
        adapted = entity.cw_adapt_to('ICollaborative')
        for owner_eid in owners:
            self.setup_ce(as_user=owner_eid, collaborators=())
            entity.cw_clear_all_caches()
            self.assertEqual(len(adapted.collaborators), 0)
            self.setup_ce(as_user=owner_eid, collaborators=owners[:2])
            entity.cw_clear_all_caches()
            self.assertEqual(frozenset(c.eid for c in adapted.collaborators),
                             frozenset(owners[:2]))




if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
