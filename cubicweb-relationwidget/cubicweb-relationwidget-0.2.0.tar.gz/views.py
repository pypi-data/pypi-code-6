# -*- coding: utf-8 -*-
# copyright 2013 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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

"""cubicweb-relationwidget views/forms/actions/components for web ui"""
from json import dumps

from cwtags.tag import div, p, a, span, h2, h3, select, \
     option, input, ul, li, label, button

from logilab.mtconverter import xml_escape
from logilab.common.decorators import cachedproperty

from cubicweb.utils import make_uid
from cubicweb.predicates import objectify_predicate
from cubicweb.uilib import js
from cubicweb.view import EntityView, EntityStartupView
from cubicweb.web import formwidgets as fwdg
from cubicweb.web.views import tableview, basetemplates
from cubicweb.web.views.basetemplates import modal_view, ModalMainTemplate

_ = unicode

_('required_error')
_('no selected entities')



def _guess_multiple(form, field):
    """guess cardinality of edited relation"""
    eschema = form._cw.vreg.schema[form.edited_entity.cw_etype]
    rschema = eschema.schema[field.name]
    rdef = eschema.rdef(rschema, field.role)
    card = rdef.role_cardinality(field.role)
    return card in '*+'


def make_action(form, field, targetetype, widgetuid, title):
    kwargs = {'vid': 'search_related_entities',
              '__modal': 1,
              'relation': '%s:%s:%s' % (field.name, targetetype, field.role)}
    entity = form.edited_entity
    if not entity.has_eid():
        # entity is not created yet
        url = form._cw.build_url('view', etype=entity.__regid__, **kwargs)
    else:
        # entity is edited, use its absolute url as base url
        url = entity.absolute_url(**kwargs)
    options = {
        'dialogOptions': {'title': title},
        'editOptions': {
            'required': int(field.required),
            'multiple': _guess_multiple(form, field),
            'searchurl': url,
        },
    }
    return str(js.jQuery('#' + widgetuid).relationwidget(options))


class RelationFacetWidget(fwdg.Select):
    """ Relation widget with facet selection, providing:

    * a list of checkbox-(de-)selectable related entities
    * a mecanism to trigger the display of a pop-up window for each possible
      target entity type of the relation
    * a pop-up window to search (using facets) entities to be linked to the
      edited entity, display (in a paginated table) and select them (using a
      checkbox on each line)

    Partitioning by target entity type provides:

    * potentially lighter result sets
    * pertinent facets (mixing everything would shut down all
      but the most generic ones)
    """
    needs_js = ('jquery.ui.js',
                'cubicweb.ajax.js',
                'cubicweb.widgets.js',
                'cubicweb.facets.js',
                'cubes.relationwidget.js')
    needs_css = ('jquery.ui.css',
                 'cubicweb.facets.css',
                 'cubes.relationwidget.css')

    def _render(self, form, field, renderer):
        _ = form._cw._
        form._cw.html_headers.define_var(
            'facetLoadingMsg', _('facet-loading-msg'))
        entity = form.edited_entity
        html = []
        w = html.append
        domid = ('widget-%s'
                 % field.input_name(form, self.suffix).replace(':', '-'))
        rtype = entity._cw.vreg.schema.rschema(field.name)
        # prepare to feed the edit controller
        related = self._compute_related(form, field)
        self._render_post(w, entity, rtype, field.role, related, domid)
        # compute the pop-up trigger action(s)
        self._render_triggers(w, domid, form, field, rtype)
        # this is an anchor for the modal dialog
        w(div(id=domid, style='display: none'))
        return u'\n'.join(unicode(node) for node in html)

    def _compute_related(self, form, field):
        """ For each already related entity, return a pair with its eid and its
        `incontext` html view """
        entity = form.edited_entity
        related = field.relvoc_linkedto(form)
        if entity.has_eid():
            rset = entity.related(field.name, field.role)
            related += [(e.view('incontext'), unicode(e.eid))
                        for e in rset.entities()]
        return related

    def _render_post(self, w, entity, rtype, role, related, domid):
        name = '%s-%s:%s' % (rtype, role, entity.eid)
        with div(w, id='inputs-for-' + domid,
                 Class='cw-relationwidget-list'):
            for html_label, eid in related:
                with div(w, Class='checkbox'):
                    with label(w, **{'for-name': name}):
                        w(input(name=name, type='checkbox',
                                checked='checked',
                                value=eid,
                                **{'data-html-label': xml_escape(html_label)}))
                        w(html_label)

    def _render_triggers(self, w, domid, form, field, rtype):
        """ According to the number of target entity types for the edited entity
        and considered relation, write the html for:

        * a user message indicating there is no entity that can be linked
        * a button-like link if there is a single possible target etype
        * a drop-down list of possible target etypes if there are more than 1

        In both later cases, actionning them will trigger the dedicated search
        and select pop-up window.
        """
        _ = form._cw._
        dialog_title = _('search entities to be linked to %(targetetype)s')
        actions = []
        target_etypes = rtype.targets(form.edited_entity.e_schema, field.role)
        for target_etype in target_etypes:
            if form.edited_entity.unrelated(
                    field.name, target_etype, field.role, limit=None,
                    lt_infos=form.linked_to):
                title = dialog_title % {'targetetype': _(target_etype)}
                actions.append((target_etype, make_action(
                            form, field, target_etype, domid, title)))
        if not actions:
            w(div(xml_escape(_('no available "%s" to relate to')
                             % ', '.join("%s" % _(e) for e in target_etypes)),
                  **{'class':'alert alert-warning'}))
        elif len(actions) == 1:
            # Just one: a direct link.
            target_etype, action = actions[0]
            link_title = xml_escape(_('link to %(targetetype)s')
                                    % {'targetetype': _(target_etype)})
            w(p(a(link_title, onclick=xml_escape(action),
                  href=xml_escape('javascript:$.noop()'),
                  Class='btn btn-default cw-relationwidget-single-link'),
                Class='form-control-static'))
        else:
            # Several possible target types, provide a combobox
            with div(w, Class='btn-group'):
                with button(w, type="button",
                            Class="btn btn-default dropdown-toggle",
                            **{'data-toggle': "dropdown"}):
                    w(_('link to ...') + ' ')
                    w(span(Class="caret"))
                with ul(w, Class='dropdown-menu'):
                    for target_etype, action in actions:
                        w(li(a(xml_escape(_(target_etype.type)),
                               Class="btn-link",
                               onclick=xml_escape(action))))


class SearchForReleatedEntitiesView(EntityStartupView):
    """view called by the edition view when the user asks to search
    for something to link to the edited eid
    """
    __regid__ = 'search_related_entities'
    # do not add this modal view in the breadcrumbs history:
    add_to_breadcrumbs = False

    def call(self):
        _ = self._cw._
        w = self.w
        entity = self.compute_entity()
        rtype, tetype, role = self._cw.form['relation'].split(':')
        # refreshable part
        w(h3(_('Link/unlink entities')))
        with div(w, id='cw-relationwidget-table'):
            rql, args = entity.cw_linkable_rql(rtype, tetype, role,
                                               ordermethod='fetch_order',
                                               vocabconstraints=False)
            rset = self._cw.execute(rql, args)
            self.wview('select_related_entities_table', rset=rset)
        w(h3(_('Selected items')))
        # placeholder divs for deletions & additions
        w(div(**{'id':'cw-relationwidget-alert',
                 'class':'alert alert-danger hidden'}))
        # placeholder for linked entities summary
        w(ul(**{'id':'cw-relationwidget-linked-summary',
                'class':'cw-relationwidget-list'}))

    def compute_entity(self):
        if self.cw_rset:
            return self.cw_rset.get_entity(0, 0)
        else:
            etype = self._cw.form['etype']
            return self._cw.vreg['etypes'].etype_class(etype)(self._cw)


class SelectEntitiesTableLayout(tableview.TableLayout):
    __regid__ = 'select_related_entities_table_layout'
    display_filter = 'top'
    hide_filter = False


class SelectMainEntityColRenderer(tableview.MainEntityColRenderer):
    """Custom renderer of the main entity in the table of selectable entities
    that includes a DOM attribute to be used for selection on JS side.
    """
    attributes = {'data-label-cell': 'true'}


class SelectEntitiesColRenderer(tableview.RsetTableColRenderer):

    def render_header(self, w):
        # do not add headers
        w(u'')

    def render_cell(self, w, rownum):
        entity = self.cw_rset.get_entity(rownum, 0)
        w(input(type='checkbox', value=entity.eid))

    def sortvalue(self, rownum):
        return None


class SelectEntitiesTableView(tableview.EntityTableView):
    """Table view of the selectable entities in the relation widget

    Selection of columns (and respective renderer) can be overridden by
    updating `columns` and `column_renderers` class attributes.
    """
    __regid__ = 'select_related_entities_table'
    layout_id = 'select_related_entities_table_layout'
    columns = ['select', 'entity']
    column_renderers = {
        'select': SelectEntitiesColRenderer('one', sortable=False),
        'entity': SelectMainEntityColRenderer(),
    }

    def page_navigation_url(self, navcomp, _path, params):
        params['divid'] = self.domid
        params['vid'] = self.__regid__
        return navcomp.ajax_page_url(**params)
