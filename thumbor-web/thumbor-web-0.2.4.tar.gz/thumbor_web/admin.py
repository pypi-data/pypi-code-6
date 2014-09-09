#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, redirect, request
import flask.ext.login as login
from flask.ext.admin import helpers, AdminIndexView, Admin, expose
from flask.ext.admin.contrib import sqla
from wtforms import form, fields, validators
from werkzeug.security import check_password_hash

from thumbor_web import models

mod = Blueprint('admin', __name__)

login_manager = login.LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.filter_by(id=user_id).first()


class AdminView(AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated():
            return redirect(url_for('.login_view'))
        return super(AdminView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated():
            return redirect(url_for('.index'))

        self._template_args['form'] = form
        return super(AdminView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))


class ModelView(sqla.ModelView):

    def is_accessible(self):
        return login.current_user.is_authenticated()


class LoginForm(form.Form):
    login = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        if not check_password_hash(user.password, self.password.data):
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return models.User.query.filter_by(username=self.login.data).first()


def init_app(app):
    login_manager.init_app(app)
    admin = Admin(app, 'Auth', index_view=AdminView(), base_template='admin/master_layout.html')
    admin.add_view(ModelView(models.User, models.db.session))
    admin.add_view(ModelView(models.Testimonial, models.db.session))
