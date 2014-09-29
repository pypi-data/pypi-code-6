# -*- coding: utf-8 -*-
# copyright 2014 UNLISH S.A.S. (Montpellier, FRANCE), all rights reserved.
# contact http://www.unlish.com -- mailto:contact@unlish.com
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
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-tagsinput views/forms/actions/components for web ui"""

import json

from cubicweb import tags

from cubicweb.web import formwidgets, INTERNAL_FIELD_VALUE
from cubicweb.web.views.ajaxcontroller import ajaxfunc
from cubicweb.web.formfields import RelationField


class TagsInputBase(formwidgets.TextInput):
    needs_css = formwidgets.Select.needs_css + ('bootstrap-tagsinput.css',)
    needs_js = formwidgets.Select.needs_js + (
        'bootstrap-tagsinput.min.js', 'typeahead.bundle.js')

    itemhtml_view_regid = 'tagsinput.itemhtml'

    options = {
        'itemValue': 'value',
        'itemText': 'text',
        'itemHtml': 'html'
    }

    def __init__(self, options=None, **kw):
        super(TagsInputBase, self).__init__(**kw)
        if options is not None:
            self.options = self.options.copy()
            self.options.update(options)

    def get_itemhtml(self, form, field, value, label, oattrs=None):
        if isinstance(field, RelationField):
            html = []
            view = form._cw.vreg['views'].select(
                self.itemhtml_view_regid,
                form._cw,
                rset=form._cw.entity_from_eid(value).as_rset())
            view.render(w=html.append)
            return u''.join(unicode(x) for x in html)
        else:
            return label

    def make_datum(self, form, field, value, label=None, oattrs=None):
        return {'value': value, 'text': label,
                'html': self.get_itemhtml(form, field, value, label, oattrs)}

    def process_field_data(self, form, field):
        value = form._cw.form.get(field.input_name(form, self.suffix))
        if isinstance(value, basestring):
            value = value.strip().split(',')
        return value


class ObjectTagsInput(TagsInputBase):
    vocabulary_widget = True

    def _render(self, form, field, renderer):
        curvalues, attrs = self.values_and_attributes(form, field)

        vocab = field.vocabulary(form)
        datasource_values = []
        selected_options = []

        for option in vocab:
            if len(option) == 3:
                label, value, oattrs = option
            elif len(option) == 2:
                (label, value), oattrs = option, {}
            if value == INTERNAL_FIELD_VALUE:
                continue
            datum = self.make_datum(form, field, value, label, oattrs)
            if value in curvalues:
                selected_options.append(datum)
            datasource_values.append(datum)

        select = '#' + attrs['id'].replace(':', '\\\\:')
        js = """
            $("%(select)s").tagsinput(%(options)s);

            $("%(select)s").tagsinput('input').attr(
                'tabindex', $("%(select)s").attr('tabindex'));

            %(injectvalues)s

            // instantiate the bloodhound suggestion engine
            var input_values = new Bloodhound({
                    datumTokenizer: function(d) { return Bloodhound.tokenizers.whitespace(d.text); },
                    queryTokenizer: Bloodhound.tokenizers.whitespace,
                    local: %(datasource_values)s,
                    limit: 10
                });

            input_values.initialize();
            $("%(select)s").tagsinput('input').typeahead({hint: false}, {
                displayKey: 'text',
                source: input_values.ttAdapter(),
                templates: {
                    suggestion: function (datum) { return datum.html; }
                }
            }).bind('typeahead:selected', $.proxy(function (obj, datum) {
                this.tagsinput('add', datum);
                this.tagsinput('input').typeahead('val', '');
            }, $('%(select)s')));

            """ % {
            'id': attrs['id'],
            'select': select,
            'options': json.dumps(self.options),
            'datasource_values': json.dumps(datasource_values),
            'injectvalues': "\n".join(
                "$('%s').tagsinput('add', %s);" %
                (select, json.dumps(o)) for o in selected_options)
        }

        form._cw.add_onload(js)

        return tags.input(name=field.input_name(form, self.suffix), **attrs)


@ajaxfunc(output_type='json')
def relwidget_query_relation(self, rtype, role, q):
    itemhtml_view_regid = 'tagsinput.itemhtml'

    rschema = self._cw.vreg.schema.rschema(rtype)
    if role == 'object':
        etypes = rschema.subjects()
    elif role == 'subject':
        etypes = rschema.objects()
    else:
        raise ValueError('invalid role: %s' % role)
    rql = "Any X ORDERBY FTIRANK(X) LIMIT 10 WHERE X has_text %(q)s, "
    rql += " OR ".join("X is " + etype.type for etype in etypes)

    rset = self._cw.execute(rql, {
        'q': ' '.join('%s*' % t for t in q.split(' '))
    })

    result = []
    for e in rset.entities():
        html = []
        view = self._cw.vreg['views'].select(
            itemhtml_view_regid,
            self._cw,
            rset=self._cw.entity_from_eid(e.eid).as_rset())
        view.render(w=html.append)
        html_string = u''.join(unicode(x) for x in html)
        result.append({
            'value': e.eid, 'text': e.dc_long_title(),
            'html': html_string})

    return result


class LazyRelationWidget(TagsInputBase):
    """Widget to edit a relation. Assumes to be used with a RelationField."""

    ajax_function = 'relwidget_query_relation'
    extra_args = '""'

    def __init__(self, ajax_function=None, extra_args=None, **kw):
        super(LazyRelationWidget, self).__init__(**kw)
        if ajax_function:
            self.ajax_function = ajax_function
        if extra_args:
            self.extra_args = extra_args

    def _render(self, form, field, renderer):
        curvalues, attrs = self.values_and_attributes(form, field)

        #rschema = form._cw.vreg.schema.rschema(field.name)

        values = []

        for eid in curvalues:
            if not eid:
                continue
            e = form._cw.entity_from_eid(eid)
            datum = self.make_datum(form, field, eid, e.dc_long_title())
            values.append(datum)

        select = '#' + attrs['id'].replace(':', '\\\\:')
        js = """
        var input = $("%(select)s");
        input.tagsinput(%(options)s);

        %(injectvalues)s

        var url_replace = function (url, query) {
              url = url + '&arg="' + query + '"' + %(extra_args)s;
              return url;
            };

        var source = new Bloodhound({
          name: '%(id)s',
          // local: [{ val: 'dog' }, { val: 'pig' }, { val: 'moose' }], XXX
          // inject the current values ?
          remote: {
            'url': AJAX_BASE_URL
              + 'fname=%(ajax_function)s&pageid='
              + pageid + '&arg="%(name)s"&arg="%(role)s"',
            'replace': url_replace
          },
          datumTokenizer: function(d) {
            return Bloodhound.tokenizers.whitespace(d.text);
          },
          queryTokenizer: Bloodhound.tokenizers.whitespace,
          limit: 10
        });

        $("%(select)s").tagsinput('input').attr(
            'tabindex', $("%(select)s").attr('tabindex'));

        $("%(select)s").tagsinput('input').typeahead({hint: false}, {
            displayKey: 'text',
            source: source.ttAdapter(),
            templates: {
                suggestion: function (datum) { return datum.html; }
            }
        }).bind('typeahead:selected', $.proxy(function (obj, datum) {
            this.tagsinput('add', datum);
            this.tagsinput('input').typeahead('val', '');
        }, $('%(select)s')));

        source.initialize();


        """ % {
            'id': attrs['id'],
            'select': select,
            'name': field.name,
            'role': field.role,
            'injectvalues': "\n".join(
                "$('%s').tagsinput('add', %s);" %
                (select, json.dumps(v)) for v in values),
            'options': json.dumps(self.options),
            'ajax_function': self.ajax_function,
            'extra_args': self.extra_args,
        }

        if 'additional_js' in self.options:
            js += self.options.get('additional_js')
        form._cw.add_onload(js)
        return tags.input(name=field.input_name(form, self.suffix), **attrs)
