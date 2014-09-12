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

from logilab.common.decorators import monkeypatch

from cubicweb.__pkginfo__ import numversion

if numversion < (3, 19):
    # Add cw_linkable_rql for relationwidget with CW < 3.19.

    from rql.stmts import Select
    from rql.nodes import Not, VariableRef, Constant, make_relation

    from cubicweb import neg_role
    from cubicweb.schema import RQLVocabularyConstraint, RQLConstraint
    from cubicweb.rqlrewrite import RQLRewriter
    from cubicweb.entity import (Entity, pruned_lt_info,
                                 build_cstr_with_linkto_infos)

    @monkeypatch(Entity)
    def cw_linkable_rql(self, rtype, targettype, role, ordermethod=None,
                        vocabconstraints=True, lt_infos={}, limit=None):
        """build a rql to fetch targettype entities either related or unrelated
        to this entity using (rtype, role) relation.

        Consider relation permissions so that returned entities may be actually
        linked by `rtype`.

        `lt_infos` are supplementary informations, usually coming from __linkto
        parameter, that can help further restricting the results in case current
        entity is not yet created. It is a dict describing entities the current
        entity will be linked to, which keys are (rtype, role) tuples and values
        are a list of eids.
        """
        return self._cw_compute_linkable_rql(rtype, targettype, role, ordermethod=None,
                                             vocabconstraints=vocabconstraints,
                                             lt_infos=lt_infos, limit=limit,
                                             unrelated_only=False)

    @monkeypatch(Entity)
    def cw_unrelated_rql(self, rtype, targettype, role, ordermethod=None,
                         vocabconstraints=True, lt_infos={}, limit=None):
        """build a rql to fetch `targettype` entities unrelated to this entity
        using (rtype, role) relation.

        Consider relation permissions so that returned entities may be actually
        linked by `rtype`.

        `lt_infos` are supplementary informations, usually coming from __linkto
        parameter, that can help further restricting the results in case current
        entity is not yet created. It is a dict describing entities the current
        entity will be linked to, which keys are (rtype, role) tuples and values
        are a list of eids.
        """
        return self._cw_compute_linkable_rql(rtype, targettype, role, ordermethod=None,
                                             vocabconstraints=vocabconstraints,
                                             lt_infos=lt_infos, limit=limit,
                                             unrelated_only=True)

    @monkeypatch(Entity)
    def _cw_compute_linkable_rql(self, rtype, targettype, role, ordermethod=None,
                                 vocabconstraints=True, lt_infos={}, limit=None,
                                 unrelated_only=False):
        """build a rql to fetch `targettype` entities that may be related to
        this entity using the (rtype, role) relation.

        By default (unrelated_only=False), this includes the already linked
        entities as well as the unrelated ones. If `unrelated_only` is True, the
        rql filters out the already related entities.
        """
        ordermethod = ordermethod or 'fetch_unrelated_order'
        rschema = self._cw.vreg.schema.rschema(rtype)
        rdef = rschema.role_rdef(self.e_schema, targettype, role)
        rewriter = RQLRewriter(self._cw)
        select = Select()
        # initialize some variables according to the `role` of `self` in the
        # relation (variable names must respect constraints conventions):
        # * variable for myself (`evar`)
        # * variable for searched entities (`searchvedvar`)
        if role == 'subject':
            evar = subjvar = select.get_variable('S')
            searchedvar = objvar = select.get_variable('O')
        else:
            searchedvar = subjvar = select.get_variable('S')
            evar = objvar = select.get_variable('O')
        select.add_selected(searchedvar)
        if limit is not None:
            select.set_limit(limit)
        # initialize some variables according to `self` existence
        if rdef.role_cardinality(neg_role(role)) in '?1':
            # if cardinality in '1?', we want a target entity which isn't
            # already linked using this relation
            variable = select.make_variable()
            if role == 'subject':
                rel = make_relation(variable, rtype, (searchedvar,), VariableRef)
            else:
                rel = make_relation(searchedvar, rtype, (variable,), VariableRef)
            select.add_restriction(Not(rel))
        elif self.has_eid() and unrelated_only:
            # elif we have an eid, we don't want a target entity which is
            # already linked to ourself through this relation
            rel = make_relation(subjvar, rtype, (objvar,), VariableRef)
            select.add_restriction(Not(rel))
        if self.has_eid():
            rel = make_relation(evar, 'eid', ('x', 'Substitute'), Constant)
            select.add_restriction(rel)
            args = {'x': self.eid}
            if role == 'subject':
                sec_check_args = {'fromeid': self.eid}
            else:
                sec_check_args = {'toeid': self.eid}
            existant = None # instead of 'SO', improve perfs
        else:
            args = {}
            sec_check_args = {}
            existant = searchedvar.name
            # undefine unused evar, or the type resolver will consider it
            select.undefine_variable(evar)
        # retrieve entity class for targettype to compute base rql
        etypecls = self._cw.vreg['etypes'].etype_class(targettype)
        etypecls.fetch_rqlst(self._cw.user, select, searchedvar,
                             ordermethod=ordermethod)
        # from now on, we need variable type resolving
        self._cw.vreg.solutions(self._cw, select, args)
        # insert RQL expressions for schema constraints into the rql syntax tree
        if vocabconstraints:
            # RQLConstraint is a subclass for RQLVocabularyConstraint, so they
            # will be included as well
            cstrcls = RQLVocabularyConstraint
        else:
            cstrcls = RQLConstraint
        lt_infos = pruned_lt_info(self.e_schema, lt_infos or {})
        # if there are still lt_infos, use set to keep track of added eid
        # relations (adding twice the same eid relation is incorrect RQL)
        eidvars = set()
        for cstr in rdef.constraints:
            # consider constraint.mainvars to check if constraint apply
            if isinstance(cstr, cstrcls) and searchedvar.name in cstr.mainvars:
                if not self.has_eid():
                    if lt_infos:
                        # we can perhaps further restrict with linkto infos using
                        # a custom constraint built from cstr and lt_infos
                        cstr = build_cstr_with_linkto_infos(
                            cstr, args, searchedvar, evar, lt_infos, eidvars)
                        if cstr is None:
                            continue # could not build constraint -> discard
                    elif evar.name in cstr.mainvars:
                        continue
                # compute a varmap suitable to RQLRewriter.rewrite argument
                varmap = dict((v, v) for v in (searchedvar.name, evar.name)
                              if v in select.defined_vars and v in cstr.mainvars)
                # rewrite constraint by constraint since we want a AND between
                # expressions.
                rewriter.rewrite(select, [(varmap, (cstr,))], args, existant)
        # insert security RQL expressions granting the permission to 'add' the
        # relation into the rql syntax tree, if necessary
        rqlexprs = rdef.get_rqlexprs('add')
        if not self.has_eid():
            rqlexprs = [rqlexpr for rqlexpr in rqlexprs
                        if searchedvar.name in rqlexpr.mainvars]
        if rqlexprs and not rdef.has_perm(self._cw, 'add', **sec_check_args):
            # compute a varmap suitable to RQLRewriter.rewrite argument
            varmap = dict((v, v) for v in (searchedvar.name, evar.name)
                          if v in select.defined_vars)
            # rewrite all expressions at once since we want a OR between them.
            rewriter.rewrite(select, [(varmap, rqlexprs)], args, existant)
        # ensure we have an order defined
        if not select.orderby:
            select.add_sort_var(select.defined_vars[searchedvar.name])
        # we're done, turn the rql syntax tree as a string
        rql = select.as_string()
        return rql, args
