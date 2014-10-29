from hamcrest import *
from quaidan.command import UpdateMember
from quaidan.status import Member
import unittest

class UpdateMemberTest(unittest.TestCase):

    def setUp(self):
        member = Member('dummy worker url', 'dummy route',
            'dummy route redirect', 1, 2, False, False, False, False,
            3, 4, 5, 'dummy transferred', 'dummy read')
        self._update_member = UpdateMember('dummy cluster', member)

    def test_uses_cluster_name(self):
        assert_that(self._update_member.cluster_name,
            is_(equal_to('dummy cluster')))

    def test_uses_worker_url(self):
        assert_that(self._update_member.worker_url,
            is_(equal_to('dummy worker url')))

    def test_uses_route(self):
        assert_that(self._update_member.route,
            is_(equal_to('dummy route')))

    def test_create_form_with_route(self):
        self._update_member.route = 'new route'
        form = self.__create_form()
        assert_that(form, has_entry('w_wr', 'new route'))

    def test_uses_route_redirect(self):
        assert_that(self._update_member.route_redirect,
            is_(equal_to('dummy route redirect')))

    def test_create_form_with_route_redirect(self):
        self._update_member.route_redirect = 'new route redirect'
        form = self.__create_form()
        assert_that(form, has_entry('w_rr', 'new route redirect'))

    def test_usese_load_factor(self):
        assert_that(self._update_member.load_factor, is_(1))

    def test_create_form_with_load_factor(self):
        self._update_member.load_factor = 20
        form = self.__create_form()
        assert_that(form, has_entry('w_lf', 20))

    def test_uses_lb_set(self):
        assert_that(self._update_member.lb_set, is_(2))

    def test_create_form_with_lb_set(self):
        self._update_member.lb_set = 20
        form = self.__create_form()
        assert_that(form, has_entry('w_ls', 20))

    def test_uses_ignore_errors(self):
        assert_that(self._update_member.ignore_errors, is_(False))

    def test_create_form_with_ignore_errors(self):
        self._update_member.ignore_errors = True
        form = self.__create_form()
        assert_that(form, has_entry('w_status_I', True))

    def test_uses_draining_mode(self):
        assert_that(self._update_member.draining_mode, is_(False))

    def test_create_form_with_draining_mode_on(self):
        self._update_member.draining_mode = True
        form = self.__create_form()
        assert_that(form, has_entry('w_status_N', True))

    def test_uses_enabled(self):
        assert_that(self._update_member.enabled, is_(False))

    def test_create_form_with_enabled(self):
        self._update_member.enabled = True
        form = self.__create_form()
        assert_that(form, has_entry('w_status_D', False))

    def test_uses_hot_standby(self):
        assert_that(self._update_member.hot_standby, is_(False))

    def test_create_form_with_hot_standby(self):
        self._update_member.hot_standby = True
        form = self.__create_form()
        assert_that(form, has_entry('w_status_H', True))

    def test_create_form_with_cluster_name(self):
        self._update_member.cluster_name = 'new cluster name'
        form = self.__create_form()
        assert_that(form, has_entry('b', 'new cluster name'))

    def test_create_form_with_worker_url(self):
        self._update_member.worker_url = 'new worker URL'
        form = self.__create_form()
        assert_that(form, has_entry('w', 'new worker URL'))

    def __create_form(self):
        return self._update_member.to_form()
