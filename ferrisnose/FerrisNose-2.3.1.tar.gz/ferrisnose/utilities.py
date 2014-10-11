import unittest
import webtest
import os


class AppEngineTest(unittest.TestCase):
    """
    Basic class from which all app engine test cases can inherit from.
    Handles setting up the testbed and provides utilities to log in
    users and run deferred tasks.
    """

    def setUp(self):
        from .testbed import FullTestBed
        self.testbed = FullTestBed()
        self.testbed.activate()

    def tearDown(self):
        self.testbed.deactivate()

    def loginUser(self, email='test@example.com', admin=False):
        self.testbed.login_user(email, admin)

    login_user = loginUser

    def runDeferredTasks(self, queue='default'):
        self.testbed.run_deferred_tasks(queue)

    run_deferred_tasks = runDeferredTasks


class AppEngineWebTest(AppEngineTest):
    """
    Provides a complete app engine testbed as well as a webtest instance
    available at ``self.testapp``. You can add routes using ``self.add_route``
    or add a ferris controller using ``self.add_controller``.
    """
    def setUp(self):
        from webapp2 import WSGIApplication
        super(AppEngineWebTest, self).setUp()
        app = WSGIApplication(debug=True, config={
            'webapp2_extras.sessions': {'secret_key': 'notasecret'}
        })
        self.testapp = webtest.TestApp(app)

    def add_controller(self, c):
        c._build_routes(self.testapp.app.router)

    addController = add_controller

    def add_route(self, r):
        self.testapp.app.router.add(r)

    def add_routes(self, rs):
        for n in rs:
            self.add_route(n)

    addRoute = add_route
    addRoutes = add_routes


class FerrisAppTest(AppEngineTest):
    """
    Provides a complete App Engine test environment and also automatically routes
    all application and plugin handlers to ``testapp``.
    """
    def setUp(self):
        super(FerrisAppTest, self).setUp()

        import main
        reload(main)
        self.testapp = webtest.TestApp(main.main_app)


class EndpointsTest(AppEngineTest):
    """
    Provides an environment for testing Google Cloud Endpoints Services.
    """
    def setUp(self):
        super(EndpointsTest, self).setUp()
        self._services = []
        self._testapp = None

    def add_service(self, *args):
        """
        Add the given service(s) to the testbed.

        .. note::
            No additional services can be added after getting the testapp
        """
        if self._testapp:
            raise ValueError("Can not add a service after the testapp has been created.")
        self._services.extend(args)

    addService = add_service

    @property
    def testapp(self):
        """
        Get the testapp created from the added endpoint services. Typically it's not necessary
        to access this directly, instead, you would use :func:`invoke`.
        """
        if not self._testapp:
            import endpoints
            api_server = endpoints.api_server(self._services, restricted=False)
            self._testapp = webtest.TestApp(api_server)
        return self._testapp

    def invoke(self, service_and_method, data=None, **kwargs):
        """
        Call an endpoint service method with the provided data. This will return the result
        of the method as a dictionary. This accepts additional parameters as
        post_json method from webtest.

        Example::
            result = self.invoke('GuestbookService.insert', {'content': 'Hello!'})
            assert result['content'] == 'Hello!'
        """

        if not data:
            data = {}
        return self.testapp.post_json(
            '/_ah/spi/' + service_and_method, data, **kwargs
        ).json

    def login(self, email):
        os.environ['ENDPOINTS_AUTH_EMAIL'] = email
        os.environ['ENDPOINTS_AUTH_DOMAIN'] = 'gmail'
