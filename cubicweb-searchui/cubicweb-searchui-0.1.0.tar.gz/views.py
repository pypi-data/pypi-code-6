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

"""cubicweb-searchui views/forms/actions/components for web ui"""

__docformat__ = "restructuredtext en"
_ = unicode

from logilab.mtconverter import xml_escape

from logilab.common.decorators import cachedproperty

from rql import nodes

from cubicweb.schema import META_RTYPES, VIRTUAL_RTYPES, display_name
from cubicweb.predicates import match_context_prop, is_instance
from cubicweb.utils import json_dumps, make_uid
from cubicweb.uilib import domid
from cubicweb.web import facet as facetbase
from cubicweb.web.views.ajaxcontroller import ajaxfunc


@ajaxfunc(output_type='json')
def reload_switchfacet(self, rql):
    select = self._cw.vreg.parse(self._cw, rql).children[0]
    filtered_variable = facetbase.get_filtered_variable(select)
    facetbase.prepare_select(select, filtered_variable)
    fobj = facetbase.get_facet(self._cw, 'relation-switch',
                               select, filtered_variable)
    widget = fobj.get_widget()
    return widget.render() if widget else u''


class RelationSwitchWidget(facetbase.FacetVocabularyWidget):
    option_template = u'<option value="{url}">{label} ({rowcount})</option>'
    widget_template = u"""\
<div id="{facetid}" class="facet">
  <div class="{cssclass}" cubicweb:facetName="{facetname}">{title}</div>
  <select id="cwRelationSwitch" onchange="cw.cubes.searchui.onSwitchFacetChange($(this))">
    <option value="" selected="selected"></option>
    {options}
  </select>
</div>
    """

    def template_parameters(self):
        return {
            'facetid': domid(make_uid(self.facet.__regid__)),
            'cssclass': 'facetTitle hideFacetBody',
            'facetname': xml_escape(self.facet.__regid__),
            'title': xml_escape(self.facet.title),
            'options': u'\n'.join(self.build_options()),
        }

    def build_options(self):
        vid = self.facet._cw.form.get('vid')
        kwargs = {'vid': vid} if vid else {}
        options = []
        for label, rql, rowcount in self.items:
            options.append(self.build_option(label, rql, rowcount, **kwargs))
        return options

    def build_option(self, label, rql, rowcount, **kwargs):
        build_url = self.facet._cw.build_url
        url = xml_escape(build_url('view', rql=rql, **kwargs))
        return self.option_template.format(url=xml_escape(url),
                                           label=xml_escape(label),
                                           rowcount=rowcount)

    def _render(self):
        self.facet._cw.add_js('cubes.searchui.facets.js')
        self.facet._cw.add_css('cubes.searchui.css')
        self.w(self.widget_template.format(**self.template_parameters()))


class RelationSwitchFacet(facetbase.VocabularyFacet):
    """
    Allow to switch current RQL selection to the other
    end of an accessible relation.

    * `skip_rtypes`,  the list of relations to skip
    * `skip_meta`, boolean to skip or not meta relations
    * `skip_virtual`, boolean to skip or not virtual relations
    * `dysplay_rtypes`,  if specified, only relations in this list will be
      considered as candidates for relation switches
    * `rqlpaths`, a list of 3-tuples (label, rqlpath, targetvar)
      where ``rqlpath`` is a list as for the standard RQLPathFacet
    """
    __regid__ = 'relation-switch'
    __select__ = match_context_prop() & is_instance('Any')

    needs_update = False # explain to standard facet mechanism that
                         # it should not try to update this facet itself.
    wdgclass = RelationSwitchWidget
    skip_rtypes = ()     # skip all relations in this list
    display_rtypes = ()  # only consider relations specified in this list
    skip_meta = True
    skip_virtual = True
    rqlpaths = None

    ## facet standard API #####################################################
    @property
    def title(self):
        return self._cw._('relation switch')

    def _support_and_compat(self):
        return False

    def get_widget(self):
        """Return the widget instance to use to display this facet.

        This implementation expects a .vocabulary method on the facet and
        return a combobox displaying this vocabulary.
        """
        vocab = self.vocabulary()
        if not vocab:
            return None
        wdg = self.wdgclass(self)
        selected = self.get_selected()
        for label, rql, rowcount in vocab:
            wdg.items.append((label, rql, rowcount))
        return wdg

    def vocabulary(self):
        values = []
        mainvar = self.filtered_variable
        args = self.cw_rset.args if self.cw_rset else None
        for rtype, role, targetetype, select in self.switch_rql_queries():
            rset = self.rqlexec(select.as_string(), args)
            if rset:
                label = self.item_label(rtype, role, targetetype, len(rset))
                values.append((label,
                               select.as_string(kwargs=args),
                               rset.rowcount))
        # add possible rpathes
        for label, select in self.rqlpath_switch_rql_queries():
            rset = self.rqlexec(select.as_string(), args)
            if rset:
                values.append((self._cw._(label),
                               select.as_string(kwargs=args),
                               rset.rowcount))
        return values

    def _valid_solutions(self):
        mainvar_idx = 0 # XXX check if always True
        if self.cw_rset:
            mainvar_etypes = self.cw_rset.column_types(mainvar_idx)
        else:
            mainvar_etypes = set(sol[self.filtered_variable.name]
                                 for sol in self.select.solutions)
        return [sol for sol in self.select.solutions
                if sol[self.filtered_variable.name] in mainvar_etypes]

    def possible_values(self):
        # required by facet protocol when another facet is used
        # but it shouldn't have any effect on relswitch facet
        pass

    def add_rql_restrictions(self):
        # required by facet protocol when another facet is used
        # but it shouldn't have any effect on relswitch facet
        pass

    ## custom RelationSwitchFacet API #########################################
    @staticmethod
    def build_var_relmap(var, select):
        rels = {}
        # check for existing relations and keep the used variable
        for rel in select.where.get_nodes(nodes.Relation):
            lhs, rhs = rel.get_variable_parts()
            if not isinstance(rhs, nodes.VariableRef): # e.g Constant
                continue
            if lhs.name == var.name:
                # left variable "is" mainvar
                if rel.r_type not in ('is', 'is_instance_of'):
                    rels[(rel.r_type, 'subject')] = rhs
            elif rhs.name == var.name:
                # right variable "is" mainvar
                rels[(rel.r_type, 'object')] = lhs
            else: # relation doesn't involve mainvar, ignore it
                continue
        return rels

    @cachedproperty
    def skipped_rtypes(self):
        """return the list of unconditionally skipped rtypes"""
        skipped = set()
        for rschema in self._cw.vreg.schema.relations():
            if self.display_rtypes: # explicit list of relations specified
                if rschema not in self.display_rtypes:
                    skipped.add(rschema.type)
            elif rschema.meta and self.skip_meta:
                skipped.add(rschema.type)
            elif rschema in VIRTUAL_RTYPES and self.skip_virtual:
                skipped.add(rschema.type)
            elif rschema in self.skip_rtypes:
                skipped.add(rschema.type)
        return skipped

    def possible_switches(self):
        """return the list of possible relation switches for current selection

        Return:
            a list of triples (rtype, role, targetetype)
        """
        select = self.select
        mainvar = self.filtered_variable
        rels = self.build_var_relmap(mainvar, select)
        switches = set()
        args = self.cw_rset.args if self.cw_rset else None
        for solution in self._valid_solutions():
            eschema = self._cw.vreg.schema.eschema(solution[mainvar.name])
            # add possible relations
            for rschema, ttypes, role in eschema.relation_definitions():
                rtype = rschema.type
                if rtype in self.skipped_rtypes:
                    continue
                # if the relation is already used in the rql query, reuse
                # the target variable
                targetvar = rels.get((rtype, role), None)
                if targetvar:
                    targetetype = solution[targetvar.name]
                    if (rtype, role, targetetype) not in switches:
                        switches.add((rtype, role, targetetype))
                else:
                    # try all possible targets
                    for targetetype in ttypes:
                        if (rtype, role, targetetype) not in switches:
                            switches.add((rtype, role, targetetype))
        return sorted(switches)

    def switch_rql_queries(self):
        """for each possible switch, yield corresponding rql syntax tree

        This method iterates through ``possible_switches()`` results,
        builds the corresponding syntax tree and yields it.

        When the relation to "switch on" is already present in the
        syntax tree, the target variable is reused and it only switches
        the selected variable. Otherwise, a new variable is added, the relation
        is added and the selected variable is switched to the new variables.

        Yield:
            a 4-tuple (rtype, role, targetetype, corresponding-syntax-tree)
        """
        select = self.select
        mainvar = self.filtered_variable
        rels = self.build_var_relmap(mainvar, select)
        for rtype, role, targetetype in self.possible_switches():
            select.save_state()
            try:
                # if the relation is already used in the rql query, reuse
                # the target variable
                targetvar = rels.get((rtype, role), None)
                if targetvar is None:
                    # else, add a variable and corresponding relation
                    targetvar, _ = facetbase._add_rtype_relation(select, mainvar,
                                                                 rtype, role)
                    select.add_constant_restriction(targetvar, 'is', targetetype, 'etype')
                select.add_selected(targetvar)
                yield (rtype, role, targetetype, select)
            finally:
                select.recover()

    def rqlpath_switch_rql_queries(self):
        select = self.select
        mainvar = self.filtered_variable
        etype = select.solutions[0][mainvar.name]
        if self.rqlpaths:
            for label, rqlpath, targetvar in self.rqlpaths:
                select.save_state()
                try:
                    self._add_rqlpath_to_select(rqlpath, targetvar, skiplabel=True)
                    yield label, select
                finally:
                    select.recover()

    def _add_rqlpath_to_select(self, rqlpath, targetvar, skiplabel=False):
        select = self.select
        mainvar = self.filtered_variable
        varmap = {'X': mainvar}
        for part in rqlpath:
            if isinstance(part, basestring):
                part = part.split()
            subject, rtype, object = part
            if skiplabel and object == mainvar:
                continue
            if object == targetvar:
                rschema = self._cw.vreg.schema.rschema(rtype)
                if rschema.final:
                    raise Exception('the filter variable must not be of final type')
            subjvar = facetbase._get_var(select, subject, varmap)
            objvar = facetbase._get_var(select, object, varmap)
            rel = nodes.make_relation(subjvar, rtype, (objvar,),
                                      nodes.VariableRef)
            select.add_restriction(rel)
        restrvar = varmap[targetvar]
        select.append_selected(nodes.VariableRef(restrvar))

    def item_label(self, rtype, role, targetetype, count):
        """format item label for the given relation

        Parameters:
            rtype: traversed relation
            role: role of currently selected variable in the relation
            targetetype: target type of the relation
            count: number of ``targetetype`` entities accessible trough ``rtype``

        Return:
            the label that will be displayed in the facet for this ``rtype``
        """
        return u'%s %s' % (display_name(self._cw, rtype),
                           display_name(self._cw, targetetype))
