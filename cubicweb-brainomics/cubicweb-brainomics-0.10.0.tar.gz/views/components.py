# -*- coding: utf-8 -*-
# copyright 2013 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# copyright 2013 CEA (Saclay, FRANCE), all rights reserved.
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

from logilab.mtconverter import xml_escape

from cubicweb import tags
from cubicweb.predicates import (none_rset, one_line_rset, is_instance, nonempty_rset,
                                 has_related_entities, match_view, match_user_groups,
                                 anonymous_user, relation_possible)
from cubicweb.web import component
from cubicweb.web.views import facets
from cubicweb.web.views.boxes import EditBox
from cubicweb.web.views.bookmark import BookmarksBox
from cubicweb.web.views.basecomponents import ApplicationName, HeaderComponent

from cubes.brainomics.views.download import ALL_DOWNLOADABLE

LINKED_ENTITIES = ('Subject',)

_ = unicode


###############################################################################
### NAVIGATION BOXES ##########################################################
###############################################################################
class BrainomicsLinksCtx(component.EntityCtxComponent):
    """ Component used to display related informations and links,
    referenced by the registry 'ctx-related-links'.
    """
    context = 'left'
    __regid__ = 'links-ctx'
    order = 1
    __select__ = component.EntityCtxComponent.__select__ & is_instance(*LINKED_ENTITIES)

    def render(self, w, **kwargs):
        links = list(self._cw.vreg['ctx-related-links'].possible_objects(self._cw, rset=self.cw_rset))
        if not links:
            return
        w(u'<div class="well">')
        w(u'<h4>%s</h4>' % self._cw._('Related entities'))
        w(u'<div class="btn-toolbar">')
        # Render links
        for link in links:
            infos = link.related_infos(self.cw_rset)
            if infos:
                w(u'<div class="btn-group-vertical btn-block">')
                w(u'<div class="btn-group">')
                w(u'<a class="btn btn-primary dropdown-toggle" '
                  u'data-toggle="dropdown" href="#">')
                w(u'%s <span class="caret"></span></a>' % link.get_title())
                w(u'<ul class="dropdown-menu">')
                for ahref, title in infos:
                    w(u'<li><a href="%s">%s</a></li>' % (ahref, title))
                w(u'</ul>')
                w(u'</div>')
                w(u'</div>')
        w(u'</div>')
        w(u'</div>')


class BrainomicsLinksDropdown(component.EntityCtxComponent):
    """ Component used to display related informations and links,
    referenced by the registry 'ctx-links'.
    """
    __abstract__ = True
    __registry__ = 'ctx-related-links'

    def get_title(self):
        return

    def related_infos(self, rset):
        return []


class BrainomicsLinksStudies(BrainomicsLinksDropdown):
    """ Component used to display related studies
    """
    __select__ = BrainomicsLinksDropdown.__select__ & is_instance('Subject')
    __regid__ = 'navtoolbar-studies-ctx'

    def get_title(self):
        return self._cw._('Related studies')

    def related_infos(self, rset):
        studies = set()
        for entity in self.cw_rset.entities():
            for study in entity.related_studies:
                studies.add((study.absolute_url(), study.dc_title()))
        return studies


class BrainomicsLinksGroups(BrainomicsLinksDropdown):
    """ Component used to display related groups
    """
    __select__ = BrainomicsLinksDropdown.__select__ & is_instance('Subject')
    __regid__ = 'navtoolbar-groups-ctx'

    def get_title(self):
        return self._cw._('Related groups')

    def related_infos(self, rset):
        groups = set()
        for entity in self.cw_rset.entities():
            for study in entity.related_groups:
                groups.add((study.absolute_url(), study.dc_title()))
        return groups


class BrainomicsLinksCenters(BrainomicsLinksDropdown):
    """ Component used to display related centers
    """
    __select__ = BrainomicsLinksDropdown.__select__ & is_instance('Subject')
    __regid__ = 'navtoolbar-centers-ctx'

    def get_title(self):
        return self._cw._('Related centers')

    def related_infos(self, rset):
        centers = set()
        for entity in self.cw_rset.entities():
            for study in entity.related_centers:
                centers.add((study.absolute_url(), study.dc_title()))
        return centers


class BrainomicsLinksBrowse(BrainomicsLinksDropdown):
    """ Component used to display browser
    """
    __select__ = BrainomicsLinksDropdown.__select__ & is_instance('Subject')
    __regid__ = 'navtoolbar-browse-ctx'

    def get_title(self):
        return self._cw._('Browse')

    def related_infos(self, rset):
        possible_actions = self._cw.vreg['actions'].possible_actions(self._cw, self.cw_rset)
        links = set()
        for link in list(possible_actions.get('browse-links', [])):
            print link.url()
            links.add((link.url(), link.title))
        return links


###############################################################################
### ADMIN ACTION/BOX ##########################################################
###############################################################################
class BrainomicsEditBox(EditBox):
    context = 'left'
    order = -10
    __select__ = EditBox.__select__ & match_user_groups('users', 'managers')

    def init_rendering(self):
        pass

    def get_actions(self):
        actions = self._cw.vreg['actions'].possible_actions(self._cw, self.cw_rset)
        all_actions = []
        for category in ('mainactions', 'moreactions', 'action-admin'):
            for action in actions.get(category, ()):
                all_actions.append(action)
        return all_actions

    def render(self, w, **kwargs):
        actions = self.get_actions()
        if actions:
            w(u'<div class="well admintools">')
            w(u'<h4>%s</h4>' % self._cw._('Administration tools'))
            for action in actions:
                if hasattr(action, 'title'):
                    icon = getattr(action, 'icon', 'edit')
                    title = self._cw._(action.title)
                    w(u'<a class="btn btn-primary btn-block" href="%s">' % action.url())
                    w(u'<i class="glyphicon glyphicon-%s"></i> %s</a>' % (icon, title))
            w(u'</div>')


###############################################################################
### DOWNLOAD BOX ##############################################################
###############################################################################
class BrainomicsDownloadBox(component.CtxComponent):
    __select__ = component.CtxComponent.__select__ & nonempty_rset() & is_instance(*ALL_DOWNLOADABLE)
    context = 'left'
    order = 1
    __regid__ = 'ctx-download-box'

    def render(self, w, **kwargs):
        possible_actions = self._cw.vreg['actions'].possible_actions(self._cw, self.cw_rset)
        links = list(possible_actions.get('download-links', []))
        if links:
            w(u'<div class="well admintools">')
            w(u'<h4>%s</h4>' % self._cw._('Download tools'))
            for link in links:
                url = self._cw.build_url(rql=self.cw_rset.printable_rql(), vid=link.download_vid)
                _id = link.__regid__
                w(u'<a class="btn btn-primary btn-block download-ctx" id="%s" href="%s">'
                  % (_id, url))
                w(u'<i class="glyphicon glyphicon-download"></i> %s</a>' % self._cw._(link.title))
            w(u'</div>')
            # Add on load the rql facet change
            self._cw.add_onload("""$(cw).bind('facets-content-loaded',
            cw.cubes.brainomics.changeDownloadUrls);""")


###############################################################################
### DATA BOXES ################################################################
###############################################################################
class BrainomicsResultsFileBox(component.CtxComponent):
    __select__ = (component.CtxComponent.__select__ & nonempty_rset() & one_line_rset()
                  & relation_possible('results_files'))
    context = 'left'
    __regid__ = 'ctx-results-files-box'
    order = 2
    rtype = 'results_files'
    title = _('Results files')

    def render(self, w, **kwargs):
        entity = self.cw_rset.get_entity(0, 0)
        _files = getattr(entity, self.rtype)
        if not _files:
            return
        w(u'<div class="well">')
        w(u'<h4>%s</h4>' % self._cw._(self.title))
        w(u'<ul>')
        for _file in _files:
            title = _file.dc_title().rsplit('/')[-1]
            w(u'<li>%s<a href="%s" title="%s">%s</a></li>'
              % (_file.view('icon'), _file.absolute_url(),
                 xml_escape(title), xml_escape(title[:15]+'...')))
        w(u'</ul>')
        w(u'</div>')


class BrainomicsConfigurationFileBox(BrainomicsResultsFileBox):
    __select__ = (component.CtxComponent.__select__ & nonempty_rset() & one_line_rset()
                  & relation_possible('configuration_files'))
    __regid__ = 'ctx-configuration-files-box'
    rtype = 'configuration_files'
    title = _('Configuration files')
    order = 3


###############################################################################
### FACETS/FORMWIDGETS ########################################################
###############################################################################
facets.FilterBox.bk_linkbox_template = u'<p class="btn btn-primary btn-facet">%s</p>'


def registration_callback(vreg):
    vreg.register_all(globals().values(), __name__, (BrainomicsEditBox,))
    vreg.register_and_replace(BrainomicsEditBox, EditBox)
    # Unregister breadcrumbs
    from cubicweb.web.views.ibreadcrumbs import (BreadCrumbEntityVComponent,
                                                 BreadCrumbLinkToVComponent,
                                                 BreadCrumbAnyRSetVComponent,
                                                 BreadCrumbETypeVComponent)
    vreg.unregister(BreadCrumbEntityVComponent)
    vreg.unregister(BreadCrumbAnyRSetVComponent)
    vreg.unregister(BreadCrumbETypeVComponent)
    vreg.unregister(BreadCrumbLinkToVComponent)
    # Unregister logo for now...
    # Unregister anon status component
    from cubicweb.web.views.basecomponents import ApplLogo, AnonUserStatusLink
    vreg.unregister(ApplLogo)
    vreg.unregister(AnonUserStatusLink)
