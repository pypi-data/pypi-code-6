import re
import string
import simplejson as json

from jinja2 import TemplateNotFound
from flask import request, Response, abort
from flask.ext.routes import route

from .view import View


class ModelView(View):
    # BASE
    model_name = None
    public_index = 'index'
    private_index = 'own'
    perpage = 20
    filterform = None
    sortform = None
    get_filters = None
    get_sorts = None
    create_form_class = None
    edit_form_class = None

    # TEMPLATES
    templates = {
        'index_or_detail': 'model/index-or-detail.html',
        'index': 'model/index.html',
        'own': 'model/index.html',
        'favs': 'model/index.html',
        'search': 'model/search.html',
        'tab_filters': 'model/tab.filters.html',
        'tab_sorts': 'model/tab.sorts.html',
        'tab_perpage': 'model/tab.perpage.html',
        'tab_create': 'model/tab.create.html',
        'filters': 'model/filters.html',
        'loop': 'model/loop.html',
        'pagination': 'model/pagination.html',
        'card': '{model}/card.html',
        'create': '{model}/form.html',
        'edit': '{model}/form.html',
        'detail': '{model}/detail.html',
        'pdf': '{model}/pdf.html',
        'txt': '{model}/txt.html',
    }


    def __init__(self, bp):
        View.__init__(self, bp)

        self.model_name = dashify(self.model_name or re.sub('View$', '', self.__class__.__name__))

        self.coreattrs = dict(
            endpoint = self.endpoint,
            model = self.model_name
        )
        self.coreattrs['bp'] = self.bp.name

        self.templates = {
            key: value.format(**self.coreattrs)
            if value else value for (key, value)
            in self.templates.items()
        }


    # ROUTES -------------------------------------------------------------------
    @route('/search/', endpoint='{view}:search', methods=('GET', 'POST'))
    @route('/search.json', endpoint='{view}:search_json', methods=('GET', 'POST'))
    @route('/search.html', endpoint='{view}:search_html', methods=('GET', 'POST'))
    def search(self):
        return self.do_index('search')


    @route('/', endpoint='{view}:index', methods=('GET', 'POST'))
    @route('/index.json', endpoint='{view}:index_json', methods=('GET', 'POST'))
    @route('/index.html', endpoint='{view}:index_html', methods=('GET', 'POST'))
    def index(self):
        return self.do_index('index')


    @route('/own/', endpoint='{view}:own', methods=('GET', 'POST'))
    @route('/own/index.json', endpoint='{view}:own_json', methods=('GET', 'POST'))
    @route('/own/index.html', endpoint='{view}:own_html', methods=('GET', 'POST'))
    def own(self):
        return self.do_index('own')


    @route('/favs/', endpoint='{view}:favs', methods=('GET', 'POST'))
    @route('/favs/index.json', endpoint='{view}:favs_json', methods=('GET', 'POST'))
    @route('/favs/index.html', endpoint='{view}:favs_html', methods=('GET', 'POST'))
    def favs(self):
        return self.do_index('favs')


    @route('/<id:id>/detail', endpoint='{view}:detail')
    @route('/<id:id>/detail.json', endpoint='{view}:detail_json')
    @route('/<id:id>/detail.pdf', endpoint='{view}:detail_pdf')
    @route('/<id:id>/detail.txt', endpoint='{view}:detail_txt')
    @route('/<id:id>/detail.html', endpoint='{view}:detail_html')
    @route('/<id:id>/card.html', endpoint='{view}:card_html')
    def detail(self, id):
        return self.do_detail(id)


    @route('/create', methods=('GET', 'POST'))
    def create(self):
        return self.do_create()


    @route('/<id:id>/edit', methods=('GET', 'POST'))
    def edit(self, id):
        return self.do_edit(id)


    @route('/delete', methods=('POST',))
    @route('/<id:id>/delete', methods=('POST',))
    def delete(self, id=None):
        return self.do_delete(id)


    @route('/archive', methods=('POST',))
    @route('/<id:id>/archive', methods=('POST',))
    def archive(self, id):
        return self.do_archive(id)


    # IMPLEMENTATIONS ----------------------------------------------------------
    def do_index(self, index):
        if not self.allows(index):
            raise abort(403)

        filters, filterform = self.do_filter(self.filterform, index)
        sorts, sortform = self.do_sort(self.sortform, index)

        cursor = self.do_cursor(filters, sorts)
        self.after_cursor(cursor)
        paginator, redirect = self.do_paginate(cursor, index)
        if redirect:
            return redirect
        data = self.after_index(index, paginator)

        try:
            if request.path.endswith('.json'):
                models = [model for model in paginator.models if self.allows('detail', model)]
                return self.jsonify(
                    models = models,
                    total = paginator.total,
                    **data
                )
            elif request.path.endswith('.html'):
                return self.jsonify(
                    total = paginator.total,
                    tab_html = self.render('tab_sorts',
                        index = index,
                        sortform = sortform,
                        **data
                    ),
                    data_html = self.render('loop',
                        index = index,
                        filterform = filterform,
                        sortform = sortform,
                        paginator = paginator,
                        **data
                    ),
                    flash_html = '',
                    redirect = None,
                )
            else:
                return self.render(index,
                    index = index,
                    filterform = filterform,
                    sortform = sortform,
                    paginator = paginator,
                    **data
                )
        except TemplateNotFound as e:
            self.bp.logger.warn(
                '[{method} {path}]: template {template!r} is not found'.format(
                    method=request.method, path=request.path, template=str(e)
                )
            )
            raise abort(404)


    def do_detail(self, id):
        model, data = self.detail_model(id)
        if not self.allows('detail', model):
            raise abort(403)

        try:
            if request.path.endswith('.json'):
                return self.jsonify(
                    model = model
                )
            elif request.path.endswith('.pdf'):
                    return self.render('pdf',
                        model = model,
                        **data
                    )
            elif request.path.endswith('.txt'):
                return self.render('txt',
                    model = model,
                    **data
                )
            elif request.path.endswith('.html'):
                data_html = self.render('card',
                    model = model,
                    **data
                )
                return self.jsonify(
                    data_html = data_html,
                    flash_html = '',
                    redirect = None
                )
            else:
                return self.render('detail',
                    model = model,
                    **data
                )
        except TemplateNotFound as e:
            self.bp.logger.warn(
                '[{method} {path}]: template {template!r} is not found'.format(
                    method=request.method, path=request.path, template=str(e)
                )
            )
            raise abort(404)


    def do_create(self):
        model, data = self.create_model()
        if not self.allows('create', model):
            raise abort(403)

        form = self.create_form_class(model, request.form)
        if form.ok:
            self.before_create(model, form)
            self.do_save(model)
            self.rebind_files(model)
            self.after_create(model, form)
            return self.autoredirect(model.id)

        return self.render('create',
            model = model,
            form = form,
            **data
        )


    def do_edit(self, id):
        model, data = self.edit_model(id)
        if not self.allows('edit', model):
            raise abort(403)

        form = self.edit_form_class(model, request.form)
        if form.ok:
            self.before_edit(model, form)
            model.edited_on = utcnow()
            self.do_save(model)
            self.after_edit(model, form)
            return self.autoredirect(model.id)

        return self.render('edit',
            model = model,
            form = form,
            **data
        )


    @route('/set-continue', methods=('POST',))
    def set_continue(self):
        self.session['continue'] = request.form.get('value', 'edit')
        return Response(status=204)


    # HELPERS ------------------------------------------------------------------
    def autoredirect(self, model_id):
        _continue = self.session.get('continue', 'edit')
        if _continue == 'edit':
            return self.redirect('edit', id=model_id)
        elif _continue == 'create':
            return self.redirect('create')
        elif _continue == 'index':
            index = self.private_index or self.public_index or 'home'
            return self.redirect(index)
        else:
            raise RuntimeError('Unknown `continue` value {!r}'.format(_continue))


    def jsonify(self, *args, **kwargs):
        return Response(
            json.dumps(dict(*args, **kwargs)), mimetype='application/json'
        )



def dashify(text):
    result = text[0].lower()
    for c in text[1:]:
        if c in string.ascii_lowercase:
            result = result + c
        else:
            result = result + '-' + c.lower()
    return result



