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
     option, input, ul, li, label

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
    """ relation widget with facet selection """
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
        req = form._cw
        form._cw.html_headers.define_var('facetLoadingMsg', _('facet-loading-msg'))
        entity = form.edited_entity
        html = []
        w = html.append
        widget_uid = 'widget-%s' % field.input_name(form, self.suffix).replace(':', '-')
        # Partitioning by target entity type provides:
        # * potentially lighter result sets
        # * pertinent facets (mixing everything would shut down all
        #   but the most generic ones)
        rtype = entity._cw.vreg.schema.rschema(field.name)
        targets = rtype.targets(entity.e_schema, field.role)
        # compute the widget opening link
        # Several etypes: a dropdown
        actions = []
        dialog_title = _('search entities to be linked to %(targetetype)s')
        for targetetype in targets:
            can_be_related = self.get_relvoc_unrelated(form, field, targetetype, limit=None)
            if not can_be_related:
                continue
            # title is xml escaped in js
            title = dialog_title % {'targetetype': _(targetetype)}
            actions.append((targetetype, make_action(form, field, targetetype, widget_uid,
                                                     title)))
        if not actions:
            w(div(xml_escape(_('no available "%s" to relate to') % ', '.join("%s" % _(e) for e in targets)),
                  **{'class':'alert alert-warning'}))
        elif len(actions) == 1:
            # Just one: a direct link.
            targetetype, action = actions[0]
            link_title = xml_escape(_('link to %(targetetype)s') % {'targetetype': _(targetetype)})
            w(a(link_title,
                onclick=xml_escape(action),
                href=xml_escape('javascript:$.noop()')))
        else:
            # Several possible target types, provide a combobox
            with div(w, Class='btn-group'):
                w(u'<button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">')
                w(u'%s <span class="caret"></span>' % _('link to ...'))
                w(u'</button>')
                with ul(w, Class='dropdown-menu'):
                    for targetetype, action in actions:
                        w(li(a(xml_escape(_(targetetype.type)),
                               Class="btn-link",
                               onclick=xml_escape(action))))
        # prepare to feed the edit controller
        related = self._compute_related(form, field)
        self._render_post(w, entity, rtype, field.role, related, widget_uid)
        # this is an anchor for the modal dialog
        w(div(id=widget_uid, style='display: none'))
        return u'\n'.join(unicode(node) for node in html)

    def get_relvoc_unrelated(self, form, field, targetetype, limit=None):
        return form.edited_entity.unrelated(field.name, targetetype, field.role, limit,
                                            lt_infos=form.linked_to)


    def _compute_related(self, form, field):
        # generate html to show already linked entity (associated to its eid)
        entity = form.edited_entity
        related = field.relvoc_linkedto(form)
        if entity.has_eid():
            rset = entity.related(field.name, field.role)
            related += [(e.view('oneline'), unicode(e.eid))
                        for e in rset.entities()]
        return related

    def _render_post(self, w, entity, rtype, role, related, widget_uid):
        name = '%s-%s:%s' % (rtype, role, entity.eid)
        with ul(w, id='inputs-for-' + widget_uid, **{'class':'cw-relationwidget-list'}):
            for title, eid in related:
                with li(w):
                    with label(w, **{'for-name':name}):
                        w(input(name=name, type='checkbox',
                                checked='checked',
                                value=eid,
                                **{'data-label': title}))
                        w(title)



class SearchForReleatedEntitiesView(EntityStartupView):
    """view called by the edition view when the user asks to search
    for something to link to the edited eid
    """
    __regid__ = 'search_related_entities'
    add_to_breadcrumbs = False # do not add this modal view in the breadcrumbs history

    def call(self):
        _ = self._cw._
        w = self.w
        entity = self.compute_entity()
        rtype, tetype, role = self._cw.form['relation'].split(':')
        w(h3(_('Selected items')))
        # placeholder divs for deletions & additions
        w(div(**{'id':'cw-relationwidget-alert', 'class':'alert hidden'}))
        # placeholder for linked entities summary
        w(ul(**{'id':'cw-relationwidget-linked-summary',
                'class':'cw-relationwidget-list'}))
        # refreshable part
        w(h3(_('Link/unlink entities')))
        with div(w, id='cw-relationwidget-table'):
            rql, args = entity.cw_linkable_rql(rtype, tetype, role,
                                               ordermethod='fetch_order',
                                               vocabconstraints=False)
            rset = self._cw.execute(rql, args)
            self.wview('select_related_entities_table', rset=rset)

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

class SelectEntitiesTableView(tableview.RsetTableView):
    __regid__ = 'select_related_entities_table'
    layout_id = 'select_related_entities_table_layout'
    column_renderers = {
        0: tableview.RsetTableColRenderer(
            'oneline', header='')
        }

    def build_column_renderers(self):
        renderers = super(SelectEntitiesTableView, self).build_column_renderers()
        selector = SelectEntitiesColRenderer('one', sortable=False)
        selector.bind(self, None)
        renderers.insert(0, selector)
        return renderers

    def page_navigation_url(self, navcomp, _path, params):
        params['divid'] = self.domid
        params['vid'] = self.__regid__
        return navcomp.ajax_page_url(**params)


class SelectEntitiesColRenderer(tableview.RsetTableColRenderer):

    def render_header(self, w):
        # do not add headers
        w(u'')

    def render_cell(self, w, rownum):
        entity = self.cw_rset.get_entity(rownum, 0)
        w(input(type='checkbox', value=entity.eid))

    def sortvalue(self, rownum):
        return None


class SelectReleatedEntitiesView(EntityView):
    """display a facet restricted rset"""
    __regid__ = 'select_related_entities'

    def call(self, **kwargs):
        self.wview('select_related_entities_table', self.cw_rset)
