from flask import Flask

from flask.ext.routes.router import Router, route


def test_endpoint_mask():
    app = Flask(__name__)
    router = Router(app)

    class PageView:
        endpoint = 'pages'
        url = '/pages'

        @route('/<path:path>', endpoint='{view}:{func}') # same as default
        def detail_by_path(self, path):
            pass

    for view in [PageView()]:
        router.apply(view)

    rules = app.url_map._rules_by_endpoint # endpoint -> [Rule()]
    assert len(rules.keys()) == 2 # 1 + 1 (default static)
    assert 'pages:detail_by_path' in rules.keys()
    assert str(rules['pages:detail_by_path'][0]) == '/pages/<path:path>'


def test_url_mask():
    app = Flask(__name__)
    router = Router(app)

    class PageView:
        endpoint = 'pages'
        url = '/pages'

        @route('/', rulemask='/{rule}')
        def index(self, path):
            pass

    for view in [PageView()]:
        router.apply(view)

    rules = app.url_map._rules_by_endpoint # endpoint -> [Rule()]
    assert len(rules.keys()) == 2 # 1 + 1 (default static)
    assert 'pages:index' in rules.keys()
    assert str(rules['pages:index'][0]) == '/'


def test_slash_noise():
    app = Flask(__name__)
    router = Router(app)

    class PageView:
        endpoint = 'pages'
        url = 'pages/'

        @route('/index')
        def index(self, path):
            pass

    for view in [PageView()]:
        router.apply(view)

    rules = app.url_map._rules_by_endpoint # endpoint -> [Rule()]
    assert len(rules.keys()) == 2 # 1 + 1 (default static)
    assert 'pages:index' in rules.keys()
    assert str(rules['pages:index'][0]) == '/pages/index'


def test_inheritance():
    app = Flask(__name__)
    router = Router(app)

    class UserView:
        endpoint = 'users'
        url = '/users'

        @route('/login')
        def login(self):
            pass

        @route('/logout')
        def logout(self):
            pass

    class ClientView(UserView):
        endpoint = 'clients'
        url = '/clients'

        @route('/ulogin')
        def ulogin(self):
            pass

        @route('/fblogin')
        def fblogin(self):
            pass

    for view in [UserView(), ClientView()]:
        router.apply(view)

    rules = app.url_map._rules_by_endpoint # endpoint -> [Rule()]
    assert len(rules.keys()) == 7 # 2 (UserView) + 4 (ClientView) + 1 (default static)
    assert 'users:login' in rules.keys()
    assert 'clients:login' in rules.keys()
    assert str(rules['users:login'][0]) == '/users/login'
    assert str(rules['clients:login'][0]) == '/clients/login'


def test_multiple_rules():
    app = Flask(__name__)
    router = Router(app)

    class PageView:
        endpoint = 'pages'
        url = '/pages'

        @route('/index', endpoint='{view}:index', methods=('GET', 'POST'))
        @route('/index.json', endpoint='{view}:index_json', methods=('GET', 'POST'))
        @route('/index.html', endpoint='{view}:index_html', methods=('GET', 'POST'))
        def index(self, path):
            pass

    class DocumentView(PageView):
        endpoint = 'documents'
        url = '/documents'

    for view in [PageView(), DocumentView()]:
        router.apply(view)

    rules = app.url_map._rules_by_endpoint # endpoint -> [Rule()]
    from pprint import pprint
    pprint(rules)
    assert len(rules.keys()) == 7 # 6 + 1 (default static)
    assert 'pages:index' in rules.keys()
    assert 'pages:index_json' in rules.keys()
    assert 'pages:index_html' in rules.keys()
    assert 'documents:index' in rules.keys()
    assert 'documents:index_json' in rules.keys()
    assert 'documents:index_html' in rules.keys()
    assert str(rules['pages:index'][0]) == '/pages/index'
    assert str(rules['pages:index_json'][0]) == '/pages/index.json'
    assert str(rules['pages:index_html'][0]) == '/pages/index.html'
    assert str(rules['documents:index'][0]) == '/documents/index'
    assert str(rules['documents:index_json'][0]) == '/documents/index.json'
    assert str(rules['documents:index_html'][0]) == '/documents/index.html'
